def getPypiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'pypi_config', variable: 'CONFIG_FILE')]) {
            def config = readJSON( file: CONFIG_FILE)
            return config['deployment']['indexes']
        }
    }
}

def get_sonarqube_unresolved_issues(report_task_file){
    script{

        def props = readProperties  file: '.scannerwork/report-task.txt'
        def response = httpRequest url : props['serverUrl'] + '/api/issues/search?componentKeys=' + props['projectKey'] + '&resolved=no'
        def outstandingIssues = readJSON text: response.content
        return outstandingIssues
    }
}

def call(){
    library(
        identifier: 'JenkinsPythonHelperLibrary@2024.12.0',
        retriever: modernSCM(
            [
                $class: 'GitSCMSource',
                remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git',
            ]
        )
    )
    pipeline {
        agent none
        parameters {
            booleanParam(name: 'RUN_CHECKS', defaultValue: true, description: 'Run checks on code')
            booleanParam(name: 'USE_SONARQUBE', defaultValue: true, description: 'Send data test data to SonarQube')
            credentials(name: 'SONARCLOUD_TOKEN', credentialType: 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl', defaultValue: 'sonarcloud_token', required: false)
            booleanParam(name: 'TEST_RUN_TOX', defaultValue: false, description: 'Run Tox Tests')
            booleanParam(name: 'BUILD_PACKAGES', defaultValue: false, description: 'Build Python packages')
            booleanParam(name: 'TEST_PACKAGES', defaultValue: false, description: 'Test packages')
            booleanParam(name: 'INCLUDE_LINUX-ARM64', defaultValue: false, description: 'Include ARM architecture for Linux')
            booleanParam(name: 'INCLUDE_LINUX-X86_64', defaultValue: true, description: 'Include x86_64 architecture for Linux')
            booleanParam(name: 'INCLUDE_MACOS-ARM64', defaultValue: false, description: 'Include ARM(m1) architecture for Mac')
            booleanParam(name: 'INCLUDE_MACOS-X86_64', defaultValue: false, description: 'Include x86_64 architecture for Mac')
            booleanParam(name: 'INCLUDE_WINDOWS-X86_64', defaultValue: false, description: 'Include x86_64 architecture for Windows')
            booleanParam(name: 'DEPLOY_PYPI', defaultValue: false, description: 'Deploy to pypi')
            booleanParam(name: 'DEPLOY_DOCS', defaultValue: false, description: 'Update online documentation')
        }
        stages {
            stage('Building and Testing'){
                when{
                    anyOf{
                        equals expected: true, actual: params.RUN_CHECKS
                        equals expected: true, actual: params.TEST_RUN_TOX
                        equals expected: true, actual: params.DEPLOY_DOCS
                    }
                }
                stages{
                    stage('Building and Running Test Metrics'){
                        stages{
                            stage('Building and Testing'){
                                environment{
                                    UV_PYTHON = '3.12'
                                    PIP_CACHE_DIR='/tmp/pipcache'
                                    UV_INDEX_STRATEGY='unsafe-best-match'
                                    UV_TOOL_DIR='/tmp/uvtools'
                                    UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
                                    UV_CACHE_DIR='/tmp/uvcache'
                                }
                                agent {
                                    docker{
                                        image 'python'
                                        label 'docker && linux && x86_64' // needed for pysonar-scanner which is x86_64 only as of 0.2.0.520
                                        args '--mount source=python-tmp-pyhathiprep,target=/tmp'
                                    }
                                }
                                stages{
                                    stage('Setup Testing Environment'){
                                        steps{
                                            mineRepository()
                                            retry(3){
                                                script{
                                                    try{
                                                        sh(
                                                            label: 'Create virtual environment',
                                                            script: '''python3 -m venv bootstrap_uv
                                                                       bootstrap_uv/bin/pip install --disable-pip-version-check uv
                                                                       bootstrap_uv/bin/uv venv venv
                                                                       . ./venv/bin/activate
                                                                       bootstrap_uv/bin/uv pip install uv
                                                                       rm -rf bootstrap_uv
                                                                       uv pip install -r requirements-dev.txt
                                                                       '''
                                                                   )
                                                        sh(
                                                            label: 'Install package in development mode',
                                                            script: '''. ./venv/bin/activate
                                                                       uv pip install -e .
                                                                    '''
                                                            )
                                                    } catch(e) {
                                                        cleanWs(
                                                            patterns: [
                                                                [pattern: 'venv', type: 'INCLUDE'],
                                                                [pattern: 'bootstrap_uv', type: 'INCLUDE'],
                                                            ]
                                                        )
                                                        throw e
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    stage('Building Sphinx Documentation'){
                                        steps {
                                            timeout(5){
                                                catchError(buildResult: 'SUCCESS', message: 'Building Sphinx found issues', stageResult: 'UNSTABLE') {
                                                    sh(label:"Building docs on ${env.NODE_NAME}",
                                                       script: '''. ./venv/bin/activate
                                                                  mkdir -p logs
                                                                  sphinx-build docs/source build/docs/html -d build/docs/.doctrees -v -w logs/build_sphinx.log -W --keep-going
                                                               '''
                                                       )
                                                   }
                                            }
                                        }
                                        post{
                                            always {
                                                recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log')])
                                                archiveArtifacts artifacts: 'logs/build_sphinx.log'
                                            }
                                            success{
                                                publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                                                script{
                                                    def props = readTOML( file: 'pyproject.toml')['project']
                                                    zip archive: true, dir: 'build/docs/html', glob: '', zipFile: "dist/${props.name}-${props.version}.doc.zip"
                                                    stash includes: "dist/${props.name}-${props.version}.doc.zip,build/docs/html/**", name: 'DOCS_ARCHIVE'
                                                }
                                            }
                                        }
                                    }
                                    stage('Run Tests'){
                                        when{
                                            equals expected: true, actual: params.RUN_CHECKS
                                        }
                                        parallel {
                                            stage('PyTest'){
                                                steps{
                                                    catchError(buildResult: 'UNSTABLE', message: 'Pytest tests failed', stageResult: 'UNSTABLE') {
                                                        sh(label: 'Running pytest',
                                                           script: '''. ./venv/bin/activate
                                                                      mkdir -p reports/pytest/
                                                                      coverage run --parallel-mode --source=pyhathiprep -m pytest --junitxml=reports/pytest/junit-pytest.xml

                                                                      '''

                                                        )
                                                    }
                                                }
                                                post{
                                                    always{
                                                        junit 'reports/pytest/junit-pytest.xml'
                                                    }
                                                }
                                            }
                                            stage('Documentation'){
                                                steps{
                                                    sh '''. ./venv/bin/activate
                                                          coverage run --parallel-mode --source=pyhathiprep -m sphinx docs/source build/docs -b=doctest -W --keep-going
                                                       '''
                                                }
                                            }
                                            stage('MyPy'){
                                                steps{
                                                    catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                        sh (label: 'Running MyPy',
                                                            script: '''. ./venv/bin/activate
                                                                       mkdir -p reports/mypy
                                                                       mkdir -p logs
                                                                       mypy -p pyhathiprep --html-report reports/mypy/mypy_html > logs/mypy.log
                                                                    '''
                                                            )
                                                    }
                                                }
                                                post{
                                                    always {
                                                        recordIssues(tools: [myPy(name: 'MyPy', pattern: 'logs/mypy.log')])
                                                        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                                                    }
                                                }
                                            }
                                            stage('Task Scanner'){
                                                steps{
                                                    recordIssues(tools: [taskScanner(highTags: 'FIXME', includePattern: 'pyhathiprep/**/*.py', normalTags: 'TODO')])
                                                }
                                            }
                                            stage('Run Pylint Static Analysis') {
                                                steps{
                                                    withEnv(['PYLINTHOME=.pylint_cache']) {
                                                        catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                                            sh(label: 'Running pylint',
                                                                script: '''. ./venv/bin/activate
                                                                           pylint pyhathiprep -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt
                                                                        '''

                                                            )
                                                        }
                                                        sh(
                                                            script: '''. ./venv/bin/activate
                                                                       pylint pyhathiprep -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee reports/pylint_issues.txt
                                                                    ''',
                                                            label: 'Running pylint for sonarqube',
                                                            returnStatus: true
                                                        )
                                                    }
                                                }
                                                post{
                                                    always{
                                                        recordIssues(tools: [pyLint(pattern: 'reports/pylint.txt')])
                                                        stash includes: 'reports/pylint_issues.txt,reports/pylint.txt', name: 'PYLINT_REPORT'
                                                    }
                                                }
                                            }
                                            stage('Run Flake8 Static Analysis') {
                                                steps{
                                                    catchError(buildResult: 'SUCCESS', message: 'Flake8 found issues', stageResult: 'UNSTABLE') {
                                                        sh(label: 'Running flake8',
                                                           script: '''. ./venv/bin/activate
                                                                      mkdir -p logs
                                                                      flake8 pyhathiprep --tee --output-file=logs/flake8.log
                                                                   '''
                                                         )
                                                    }
                                                }
                                                post {
                                                    always {
                                                        stash includes: 'logs/flake8.log', name: 'FLAKE8_REPORT'
                                                        recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                                    }
                                                }
                                            }
                                        }
                                        post{
                                            always{
                                                sh(label: 'Combining Coverage data',
                                                   script: '''. ./venv/bin/activate
                                                              coverage combine
                                                              coverage xml -o reports/coverage.xml
                                                              coverage html -d reports/coverage
                                                           '''
                                                )
                                                stash(includes: 'reports/coverage*.xml', name: 'COVERAGE_REPORT_DATA')
                                                recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']])
                                            }
                                        }
                                    }
                                    stage('Run Sonarqube Analysis'){
                                        options{
                                            lock('pyhathiprep-sonarscanner')
                                            retry(3)
                                        }
                                        environment{
                                            VERSION="${readTOML( file: 'pyproject.toml')['project'].version}"
                                            SONAR_USER_HOME='/tmp/sonar'
                                        }
                                        when{
                                            allOf{
                                                equals expected: true, actual: params.USE_SONARQUBE
                                                expression{
                                                    try{
                                                        withCredentials([string(credentialsId: params.SONARCLOUD_TOKEN, variable: 'dddd')]) {
                                                            echo 'Found credentials for sonarqube'
                                                        }
                                                    } catch(e){
                                                        echo 'Skipping due to invalid credentials for sonarqube'
                                                        return false
                                                    }
                                                    return true
                                                }
                                            }
                                        }
                                        steps{
                                            script{
                                                withSonarQubeEnv(installationName:'sonarcloud', credentialsId: params.SONARCLOUD_TOKEN) {
                                                    def sourceInstruction
                                                    if (env.CHANGE_ID){
                                                        sourceInstruction = '-Dsonar.pullrequest.key=$CHANGE_ID -Dsonar.pullrequest.base=$BRANCH_NAME'
                                                    } else{
                                                        sourceInstruction = '-Dsonar.branch.name=$BRANCH_NAME'
                                                    }
                                                    sh(
                                                        label: 'Running Sonar Scanner',
                                                        script: """. ./venv/bin/activate
                                                                    uv tool run pysonar-scanner -Dsonar.projectVersion=$VERSION -Dsonar.buildString=\"$BUILD_TAG\" ${sourceInstruction}
                                                                """
                                                    )
                                                }
                                                timeout(time: 1, unit: 'HOURS') {
                                                    def sonarqube_result = waitForQualityGate(abortPipeline: false)
                                                    if (sonarqube_result.status != 'OK') {
                                                        unstable "SonarQube quality gate: ${sonarqube_result.status}"
                                                    }
                                                    def outstandingIssues = get_sonarqube_unresolved_issues('.scannerwork/report-task.txt')
                                                    writeJSON file: 'reports/sonar-report.json', json: outstandingIssues
                                                }
                                                milestone label: 'sonarcloud'
                                            }
                                        }
                                        post {
                                            always{
                                                recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
                                            }
                                        }
                                    }
                                }
                                post{
                                    cleanup{
                                        cleanWs(
                                            deleteDirs: true,
                                            patterns: [
                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                [pattern: 'build/', type: 'INCLUDE'],
                                                [pattern: 'pyhathiprep.egg-info/', type: 'INCLUDE'],
                                                [pattern: '.scannerwork', type: 'INCLUDE'],
                                                [pattern: '?/', type: 'INCLUDE'],
                                                [pattern: 'reports/', type: 'INCLUDE'],
                                                [pattern: 'logs/', type: 'INCLUDE'],
                                                [pattern: '.mypy_cache/', type: 'INCLUDE'],
                                                [pattern: '.coverage', type: 'INCLUDE'],
                                                [pattern: 'coverage/', type: 'INCLUDE'],
                                                [pattern: 'coverage-sources.zip', type: 'INCLUDE'],
                                                [pattern: '.pytest_cache/', type: 'INCLUDE'],
                                                [pattern: '.pylint_cache/', type: 'INCLUDE'],
                                                [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                ]
                                        )
                                        sh 'ls -la'
                                    }
                                }
                            }
                        }
                    }
                    stage('Run Tox Test') {
                        when{
                            equals expected: true, actual: params.TEST_RUN_TOX
                        }
                         parallel{
                             stage('Linux'){
                                 when{
                                     expression {return nodesByLabel('linux && docker && x86').size() > 0}
                                 }
                                 environment{
                                     PIP_CACHE_DIR='/tmp/pipcache'
                                     UV_INDEX_STRATEGY='unsafe-best-match'
                                     UV_TOOL_DIR='/tmp/uvtools'
                                     UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
                                     UV_CACHE_DIR='/tmp/uvcache'
                                 }
                                 steps{
                                     script{
                                         def envs = []
                                         node('docker && linux'){
                                             checkout scm
                                             try{
                                                 docker.image('python').inside('--mount source=python-tmp-pyhathiprep,target=/tmp'){
                                                     sh(script: 'python3 -m venv venv && venv/bin/pip install --disable-pip-version-check uv')
                                                     envs = sh(
                                                         label: 'Get tox environments',
                                                         script: './venv/bin/uvx --quiet --constraint=requirements-dev.txt --with tox-uv tox list -d --no-desc',
                                                         returnStdout: true,
                                                     ).trim().split('\n')
                                                }
                                             } finally{
                                                 sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                             }
                                         }
                                         parallel(
                                             envs.collectEntries{toxEnv ->
                                                 def version = toxEnv.replaceAll(/py(\d)(\d+)/, '$1.$2')
                                                 [
                                                     "Tox Environment: ${toxEnv}",
                                                     {
                                                         node('docker && linux'){
                                                             retry(3){
                                                                 checkout scm
                                                                 try{
                                                                    docker.image('python').inside('--mount source=python-tmp-pyhathiprep,target=/tmp'){
                                                                         sh( label: 'Running Tox',
                                                                             script: """python3 -m venv venv && venv/bin/pip install --disable-pip-version-check uv
                                                                                        . ./venv/bin/activate
                                                                                        uv python install cpython-${version}
                                                                                        trap "rm -rf venv && rm -rf .tox" EXIT
                                                                                        uvx -p ${version} --constraint=requirements-dev.txt --with tox-uv tox run -e ${toxEnv}
                                                                                     """
                                                                             )
                                                                    }
                                                                 } catch(e) {
                                                                     sh(script: '''. ./venv/bin/activate
                                                                           uv python list
                                                                           '''
                                                                             )
                                                                     throw e
                                                                 } finally{
                                                                     sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                                 }
                                                             }
                                                         }
                                                     }
                                                 ]
                                             }
                                         )
                                     }
                                 }
                             }
                             stage('Windows'){
                                 when{
                                     expression {return nodesByLabel('windows && docker && x86').size() > 0}
                                 }
                                 environment{
                                     UV_INDEX_STRATEGY='unsafe-best-match'
                                     PIP_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\cache\\pipcache'
                                     UV_TOOL_DIR='C:\\Users\\ContainerUser\\Documents\\cache\\uvtools'
                                     UV_PYTHON_INSTALL_DIR='C:\\Users\\ContainerUser\\Documents\\cache\\uvpython'
                                     UV_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\cache\\uvcache'
                                 }
                                 steps{
                                     script{
                                         def envs = []
                                         node('docker && windows'){
                                            retry(3){
                                                checkout scm
                                                try{
                                                    docker.image(env.DEFAULT_PYTHON_DOCKER_IMAGE ? env.DEFAULT_PYTHON_DOCKER_IMAGE: 'python')
                                                        .inside("\
                                                             --mount type=volume,source=uv_python_install_dir,target=${env.UV_PYTHON_INSTALL_DIR} \
                                                             --mount type=volume,source=pipcache,target=${env.PIP_CACHE_DIR} \
                                                             --mount type=volume,source=uv_cache_dir,target=${env.UV_CACHE_DIR}\
                                                             "
                                                         ){
                                                         bat(script: 'python -m venv venv && venv\\Scripts\\pip install --disable-pip-version-check uv')
                                                         envs = bat(
                                                             label: 'Get tox environments',
                                                             script: '@.\\venv\\Scripts\\uvx --quiet --constraint=requirements-dev.txt --with tox-uv tox list -d --no-desc',
                                                             returnStdout: true,
                                                         ).trim().split('\r\n')
                                                    }
                                                } finally{
                                                    bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                }
                                            }
                                         }
                                         parallel(
                                             envs.collectEntries{toxEnv ->
                                                 def version = toxEnv.replaceAll(/py(\d)(\d+)/, '$1.$2')
                                                 [
                                                     "Tox Environment: ${toxEnv}",
                                                     {
                                                         node('docker && windows'){
                                                             retry(3){
                                                                 try{
                                                                     checkout scm
                                                                     docker.image(env.DEFAULT_PYTHON_DOCKER_IMAGE ? env.DEFAULT_PYTHON_DOCKER_IMAGE: 'python')
                                                                         .inside("\
                                                                             --mount type=volume,source=uv_python_install_dir,target=${env.UV_PYTHON_INSTALL_DIR} \
                                                                             --mount type=volume,source=pipcache,target=${env.PIP_CACHE_DIR} \
                                                                             --mount type=volume,source=uv_cache_dir,target=${env.UV_CACHE_DIR}\
                                                                             "
                                                                         ){
                                                                         bat(label: 'Running Tox',
                                                                             script: """python -m venv venv
                                                                                        venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                                        call venv\\Scripts\\activate.bat
                                                                                        uv python install cpython-${version}
                                                                                        uvx -p ${version} --constraint=requirements-dev.txt --with tox-uv tox run -e ${toxEnv}
                                                                                        rmdir /S /Q .tox
                                                                                        rmdir /S /Q venv
                                                                                     """
                                                                         )
                                                                     }
                                                                 } finally{
                                                                     bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                                 }
                                                             }
                                                         }
                                                     }
                                                 ]
                                             }
                                         )
                                     }
                                 }
                             }
                         }
                    }
                }
            }
            stage('Packaging') {
                when{
                    equals expected: true, actual: params.BUILD_PACKAGES
                    beforeAgent true
                }
                stages{
                    stage('Building Source and Wheel formats'){
                        agent {
                            docker{
                                image 'python'
                                label 'linux && docker'
                                args '--mount source=python-tmp-pyhathiprep,target=/tmp'
                              }
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_INDEX_STRATEGY='unsafe-best-match'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        options {
                            retry(2)
                        }
                        steps{
                            timeout(5){
                                sh(
                                    label: 'Package',
                                    script: '''python3 -m venv venv
                                               venv/bin/pip install --disable-pip-version-check uv
                                               trap "rm -rf venv" EXIT
                                               . ./venv/bin/activate
                                               uv build --build-constraints=requirements-dev.txt
                                            '''
                                )
                            }
                        }
                        post{
                            success{
                                archiveArtifacts artifacts: 'dist/*.whl,dist/*.tar.g,dist/*.zip', fingerprint: true
                            }
                            always{
                                stash includes: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', name: 'PYTHON_PACKAGES'
                            }
                            cleanup{
                                cleanWs(
                                    deleteDirs: true,
                                    patterns: [
                                        [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                        [pattern: 'venv/', type: 'INCLUDE'],
                                        [pattern: 'dist/', type: 'INCLUDE']
                                    ]
                                )
                            }
                        }
                    }
                    stage('Testing packages'){
                        when{
                            equals expected: true, actual: params.TEST_PACKAGES
                        }
                        environment{
                            UV_INDEX_STRATEGY='unsafe-best-match'
                        }
                        steps{
                            customMatrix(
                                axes: [
                                    [
                                        name: 'PYTHON_VERSION',
                                        values: ['3.9', '3.10', '3.11', '3.12','3.13']
                                    ],
                                    [
                                        name: 'OS',
                                        values: ['linux','macos','windows']
                                    ],
                                    [
                                        name: 'ARCHITECTURE',
                                        values: ['x86_64', 'arm64']
                                    ],
                                    [
                                        name: 'PACKAGE_TYPE',
                                        values: ['wheel', 'sdist'],
                                    ]
                                ],
                                excludes: [
                                    [
                                        [
                                            name: 'OS',
                                            values: 'windows'
                                        ],
                                        [
                                            name: 'ARCHITECTURE',
                                            values: 'arm64',
                                        ]
                                    ]
                                ],
                                when: {entry -> "INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase() && params["INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()]},
                                stages: [
                                    { entry ->
                                        stage('Test Package') {
                                            node("${entry.OS} && ${entry.ARCHITECTURE} ${['linux', 'windows'].contains(entry.OS) ? '&& docker': ''}"){
                                                try{
                                                    checkout scm
                                                    unstash 'PYTHON_PACKAGES'
                                                    if(['linux', 'windows'].contains(entry.OS) && params.containsKey("INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()) && params["INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()]){
                                                        docker.image(env.DEFAULT_PYTHON_DOCKER_IMAGE ? env.DEFAULT_PYTHON_DOCKER_IMAGE: 'python')
                                                            .inside(
                                                                isUnix() ?
                                                                '--mount source=python-tmp-pyhathiprep,target=/tmp':
                                                                '--mount type=volume,source=uv_python_install_dir,target=C:\\Users\\ContainerUser\\Documents\\cache\\uvpython \
                                                                 --mount type=volume,source=pipcache,target=C:\\Users\\ContainerUser\\Documents\\cache\\pipcache \
                                                                 --mount type=volume,source=uv_cache_dir,target=C:\\Users\\ContainerUser\\Documents\\cache\\uvcache'
                                                            ){
                                                             if(isUnix()){
                                                                withEnv([
                                                                    'PIP_CACHE_DIR=/tmp/pipcache',
                                                                    'UV_TOOL_DIR=/tmp/uvtools',
                                                                    'UV_PYTHON_INSTALL_DIR=/tmp/uvpython',
                                                                    'UV_CACHE_DIR=/tmp/uvcache',
                                                                ]){
                                                                     sh(
                                                                        label: 'Testing with tox',
                                                                        script: """python3 -m venv venv
                                                                                   ./venv/bin/pip install --disable-pip-version-check uv
                                                                                   ./venv/bin/uv python install cpython-${entry.PYTHON_VERSION}
                                                                                   ./venv/bin/uvx --constraint=requirements-dev.txt --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                             } else {
                                                                withEnv([
                                                                    'PIP_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\cache\\pipcache',
                                                                    'UV_TOOL_DIR=C:\\Users\\ContainerUser\\Documents\\cache\\uvtools',
                                                                    'UV_PYTHON_INSTALL_DIR=C:\\Users\\ContainerUser\\Documents\\cache\\uvpython',
                                                                    'UV_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\cache\\uvcache',
                                                                ]){
                                                                    bat(
                                                                        label: 'Testing with tox',
                                                                        script: """python -m venv venv
                                                                                   .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                                   .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                                   .\\venv\\Scripts\\uvx --constraint=requirements-dev.txt --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                             }
                                                        }
                                                    } else {
                                                        if(isUnix()){
                                                            sh(
                                                                label: 'Testing with tox',
                                                                script: """python3 -m venv venv
                                                                           ./venv/bin/pip install --disable-pip-version-check uv
                                                                           ./venv/bin/uvx --constraint=requirements-dev.txt --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                        """
                                                            )
                                                        } else {
                                                            bat(
                                                                label: 'Testing with tox',
                                                                script: """python -m venv venv
                                                                           .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                           .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                           .\\venv\\Scripts\\uvx --constraint=requirements-dev.txt --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                        """
                                                            )
                                                        }
                                                    }
                                                } finally{
                                                    if(isUnix()){
                                                        sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                    } else {
                                                        bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            )
                        }
                    }
                }
            }
            stage('Deploy'){
                parallel{
                    stage('Deploy to pypi') {
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_INDEX_STRATEGY='unsafe-best-match'
                            UV_TOOL_DIR='/tmp/uvtools'
                            UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        agent {
                            docker{
                                image 'python'
                                label 'docker && linux'
                                args '--mount source=python-tmp-pyhathiprep,target=/tmp'
                            }
                        }
                        when{
                            equals expected: true, actual: params.DEPLOY_PYPI
                            beforeAgent true
                            beforeInput true
                        }
                        options{
                            retry(3)
                        }
                        input {
                            message 'Upload to pypi server?'
                            parameters {
                                choice(
                                    choices: getPypiConfig(),
                                    description: 'Url to the pypi index to upload python packages.',
                                    name: 'SERVER_URL'
                                )
                            }
                        }
                        steps{
                            unstash 'PYTHON_PACKAGES'
                            withEnv(
                                [
                                    "TWINE_REPOSITORY_URL=${SERVER_URL}",
                                    'UV_INDEX_STRATEGY=unsafe-best-match'
                                ]
                            ){
                                withCredentials(
                                    [
                                        usernamePassword(
                                            credentialsId: 'jenkins-nexus',
                                            passwordVariable: 'TWINE_PASSWORD',
                                            usernameVariable: 'TWINE_USERNAME'
                                        )
                                    ]){
                                        sh(
                                            label: 'Uploading to pypi',
                                            script: '''python3 -m venv venv
                                                       trap "rm -rf venv" EXIT
                                                       . ./venv/bin/activate
                                                       pip install --disable-pip-version-check uv
                                                       uvx --constraint=requirements-dev.txt twine --installpkg upload --disable-progress-bar --non-interactive dist/*
                                                    '''
                                        )
                                }
                            }
                        }
                        post{
                            cleanup{
                                cleanWs(
                                    deleteDirs: true,
                                    patterns: [
                                            [pattern: 'dist/', type: 'INCLUDE']
                                        ]
                                )
                            }
                        }
                    }
                    stage('Deploy - SCCM'){
                        agent any
                        options {
                            skipDefaultCheckout(true)
                        }
                        when{
                            allOf{
                                equals expected: true, actual: params.DEPLOY_SCCM
                                branch 'master'
                            }
                            beforeAgent true
                        }
                        stages{
                             stage('Deploy - Staging') {
                                steps {
                                    deployStash('msi', "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                                    input('Deploy to production?')
                                }
                            }
                            stage('Deploy - SCCM Upload') {
                                steps {
                                    deployStash('msi', "${env.SCCM_UPLOAD_FOLDER}")
                                }
                                post {
                                    success {
                                        script{
                                            unstash 'Source'
                                            def  deployment_request = requestDeploy this, 'deployment.yml'
                                            echo deployment_request
                                            writeFile file: 'deployment_request.txt', text: deployment_request
                                            archiveArtifacts artifacts: 'deployment_request.txt'
                                        }
                                    }
                                }
                            }
                        }
                    }
                    stage('Deploy Online Documentation') {
                        when{
                            equals expected: true, actual: params.DEPLOY_DOCS
                            beforeAgent true
                            beforeInput true
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_INDEX_STRATEGY='unsafe-best-match'
                            UV_TOOL_DIR='/tmp/uvtools'
                            UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        agent {
                            docker{
                                image 'python'
                                label 'docker && linux'
                                args '--mount source=python-tmp-pyhathiprep,target=/tmp'
                            }
                        }
                        options{
                            timeout(time: 1, unit: 'DAYS')
                        }
                        input {
                            message 'Update project documentation?'
                        }
                        steps{
                            unstash 'DOCS_ARCHIVE'
                            withCredentials([usernamePassword(credentialsId: 'dccdocs-server', passwordVariable: 'docsPassword', usernameVariable: 'docsUsername')]) {
                                sh 'python utils/upload_docs.py --username=$docsUsername --password=$docsPassword --subroute=hathi_zip build/docs/html apache-ns.library.illinois.edu'
                            }
                        }
                        post{
                            cleanup{
                                cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: 'build/', type: 'INCLUDE'],
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            ]
                                    )
                            }
                        }
                    }
                }
            }
        }
    }
}
