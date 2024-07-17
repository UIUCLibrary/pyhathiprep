library identifier: 'JenkinsPythonHelperLibrary@2024.1.2', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git',
   ])


// ============================================================================
// Versions of python that are supported
// ----------------------------------------------------------------------------
SUPPORTED_MAC_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_LINUX_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_WINDOWS_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']

def getPypiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'pypi_config', variable: 'CONFIG_FILE')]) {
            def config = readJSON( file: CONFIG_FILE)
            return config['deployment']['indexes']
        }
    }
}

def getDevpiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'devpi_config', variable: 'CONFIG_FILE')]) {
            def configProperties = readProperties(file: CONFIG_FILE)
            configProperties.stagingIndex = {
                if (env.TAG_NAME?.trim()){
                    return 'tag_staging'
                } else{
                    return "${env.BRANCH_NAME}_staging"
                }
            }()
            return configProperties
        }
    }
}
def DEVPI_CONFIG = getDevpiConfig()
def remove_from_devpi(devpiExecutable, pkgName, pkgVersion, devpiIndex, devpiUsername, devpiPassword){
    script {
                try {
                    bat "${devpiExecutable} login ${devpiUsername} --password ${devpiPassword}"
                    bat "${devpiExecutable} use ${devpiIndex}"
                    bat "${devpiExecutable} remove -y ${pkgName}==${pkgVersion}"
                } catch (Exception ex) {
                    echo "Failed to remove ${pkgName}==${pkgVersion} from ${devpiIndex}"
            }

    }
}

def get_package_version(stashName, metadataFile){
    ws {
        unstash "${stashName}"
        script{
            def props = readProperties interpolate: true, file: "${metadataFile}"
            deleteDir()
            return props.Version
        }
    }
}

def get_package_name(stashName, metadataFile){
    ws {
        unstash "${stashName}"
        script{
            def props = readProperties interpolate: true, file: "${metadataFile}"
            deleteDir()
            return props.Name
        }
    }
}
node(){
    checkout scm//     tox = load('ci/jenkins/scripts/tox.groovy')
    devpi = load('ci/jenkins/scripts/devpi.groovy')
}

def startup(){
    parallel(
        [
            failFast: true,
            'Enable Git Forensics': {
                node(){
                    checkout scm
                    mineRepository()
                }
            },
            'Getting Distribution Info': {
                retry(3){
                    node('linux && docker && x86') {
                        timeout(2){
                            ws{
                                checkout scm
                                try{
                                    docker.image('python').inside {
                                        withEnv(['PIP_NO_CACHE_DIR=off']) {
                                            sh(
                                               label: 'Running setup.py with dist_info',
                                               script: '''python --version
                                                          python setup.py dist_info
                                                       '''
                                            )
                                        }
                                        stash includes: '*.dist-info/**', name: 'DIST-INFO'
                                        archiveArtifacts artifacts: '*.dist-info/**'
                                    }
                                } finally{
                                    deleteDir()
                                }
                            }
                        }
                    }
                }
            }
        ]
    )
}
def get_props(){
    stage('Reading Package Metadata'){
        node() {
            try{
                unstash 'DIST-INFO'
                def metadataFile = findFiles(excludes: '', glob: '*.dist-info/METADATA')[0]
                def package_metadata = readProperties interpolate: true, file: metadataFile.path
                echo """Metadata:

Name      ${package_metadata.Name}
Version   ${package_metadata.Version}
"""
                return package_metadata
            } finally {
                cleanWs(
                    patterns: [
                            [pattern: '*.dist-info/**', type: 'INCLUDE'],
                        ],
                    notFailBuild: true,
                    deleteDirs: true
                )
            }
        }
    }
}


startup()
def props = get_props()


pipeline {
    agent none
    parameters {
        booleanParam(name: 'RUN_CHECKS', defaultValue: true, description: 'Run checks on code')
        booleanParam(name: 'USE_SONARQUBE', defaultValue: true, description: 'Send data test data to SonarQube')
        credentials(name: 'SONARCLOUD_TOKEN', credentialType: 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl', defaultValue: 'sonarcloud_token', required: false)
        booleanParam(name: 'TEST_RUN_TOX', defaultValue: false, description: 'Run Tox Tests')
        booleanParam(name: 'BUILD_PACKAGES', defaultValue: false, description: 'Build Python packages')
        booleanParam(name: 'TEST_PACKAGES', defaultValue: false, description: 'Test packages')
        booleanParam(name: 'INCLUDE_LINUX_ARM', defaultValue: false, description: 'Include ARM architecture for Linux')
        booleanParam(name: 'INCLUDE_LINUX_X86_64', defaultValue: true, description: 'Include x86_64 architecture for Linux')
        booleanParam(name: 'INCLUDE_MACOS_ARM', defaultValue: false, description: 'Include ARM(m1) architecture for Mac')
        booleanParam(name: 'INCLUDE_MACOS_X86_64', defaultValue: false, description: 'Include x86_64 architecture for Mac')
        booleanParam(name: 'INCLUDE_WINDOWS_X86_64', defaultValue: false, description: 'Include x86_64 architecture for Windows')
        booleanParam(name: 'DEPLOY_DEVPI', defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: 'DEPLOY_DEVPI_PRODUCTION', defaultValue: false, description: 'Deploy to https://devpi.library.illinois.edu/production/release')
        booleanParam(name: 'DEPLOY_PYPI', defaultValue: false, description: 'Deploy to pypi')
        booleanParam(name: 'DEPLOY_DOCS', defaultValue: false, description: 'Update online documentation')
    }
    stages {
        stage('Building and Testing'){
            when{
                anyOf{
                    equals expected: true, actual: params.RUN_CHECKS
                    equals expected: true, actual: params.TEST_RUN_TOX
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    equals expected: true, actual: params.DEPLOY_DOCS
                }
            }
            stages{
                stage('Building') {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker && x86'
                        }
                    }
                    options {
                        retry(conditions: [agent()], count: 2)
                    }
                    when{
                        anyOf{
                            equals expected: true, actual: params.RUN_CHECKS
                            equals expected: true, actual: params.DEPLOY_DEVPI
                            equals expected: true, actual: params.DEPLOY_DOCS
                        }
                        beforeAgent true
                    }
                    stages{
                        stage('Building Python Package'){
                            steps {
                                timeout(5){
                                    sh(label: 'Building Python package',
                                        script: '''mkdir -p logs
                                                   python setup.py build -b build  | tee logs/build.log
                                                '''
                                        )
                                }
                            }
                        }
                        stage('Building Sphinx Documentation'){
                            steps {
                                timeout(5){
                                    catchError(buildResult: 'SUCCESS', message: 'Building Sphinx found issues', stageResult: 'UNSTABLE') {
                                        sh(label:"Building docs on ${env.NODE_NAME}",
                                           script: '''mkdir -p logs
                                                      python -m sphinx docs/source build/docs/html -d build/docs/.doctrees -v -w logs/build_sphinx.log -W --keep-going
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
                                        zip archive: true, dir: 'build/docs/html', glob: '', zipFile: "dist/${props.Name}-${props.Version}.doc.zip"
                                        stash includes: "dist/${props.Name}-${props.Version}.doc.zip,build/docs/html/**", name: 'DOCS_ARCHIVE'
                                    }
                                }
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            [pattern: 'build/', type: 'INCLUDE'],
                                            [pattern: 'logs/', type: 'INCLUDE']
                                            ]
                                    )
                                }
                            }
                        }
                    }
                }
                stage('Checks'){
                    when{
                        equals expected: true, actual: params.RUN_CHECKS
                    }
                    stages{
                        stage('Code Quality'){
                            stages{
                                stage('Testing'){
                                    agent {
                                        dockerfile {
                                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                                            label 'linux && docker && x86'
                                            args '--mount source=sonar-cache-pyhathiprep,target=/opt/sonar/.sonar/cache'
                                        }
                                    }
                                    stages{
                                        stage('Setting up Tests'){
                                            steps{
                                                sh('mkdir -p reports/')
                                            }
                                        }
                                        stage('Run Tests'){
                                            parallel {
                                                stage('PyTest'){
                                                    steps{
                                                        catchError(buildResult: 'UNSTABLE', message: 'Pytest tests failed', stageResult: 'UNSTABLE') {
                                                            sh(label: 'Running pytest',
                                                               script: '''mkdir -p reports/pytest/
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
                                                        sh 'coverage run --parallel-mode --source=pyhathiprep -m sphinx docs/source build/docs -b=doctest -W --keep-going'
                                                    }
                                                }
                                                stage('MyPy'){
                                                    steps{
                                                        catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                            sh (label: 'Running MyPy',
                                                                script: '''mkdir -p reports/mypy
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
                                                                    script: '''pylint pyhathiprep -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt
                                                                               '''

                                                                )
                                                            }
                                                            sh(
                                                                script: 'pylint pyhathiprep -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee reports/pylint_issues.txt',
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
                                                               script: '''mkdir -p logs
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
                                                       script: '''coverage combine
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
                                                    def sonarqube = load('ci/jenkins/scripts/sonarqube.groovy')
                                                    def newProps = get_props()
                                                    sonarqube.sonarcloudSubmit(
                                                        credentialsId: params.SONARCLOUD_TOKEN,
                                                        projectVersion: newProps.Version
                                                    )
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
                    }
                }
                stage('Run Tox Test') {
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                     steps {
                        script{
//                            def tox = fileLoader.fromGit(
//                                                    'tox',
//                                                    'https://github.com/UIUCLibrary/jenkins_helper_scripts.git',
//                                                    '8',
//                                                    null,
//                                                    ''
//                                                )
                            def windowsJobs = [:]
                            def linuxJobs = [:]
                            stage('Scanning Tox Environments'){
                                parallel(
                                    'Linux':{
                                        linuxJobs = getToxTestsParallel(
                                                envNamePrefix: 'Tox Linux',
                                                label: 'linux && docker && x86',
                                                dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                dockerRunArgs: '-v pipcache_pyhathiprep:/.cache/pip',
                                                verbosity: 1,
                                                retry: 2
                                            )
                                    },
                                    'Windows':{
                                        windowsJobs = getToxTestsParallel(
                                                envNamePrefix: 'Tox Windows',
                                                label: 'windows && docker && x86',
                                                dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                dockerRunArgs: '-v pipcache_pyhathiprep:c:/users/containeradministrator/appdata/local/pip',
                                                verbosity: 1,
                                                retry: 2
                                            )
                                    },
                                    failFast: true
                                )
                            }
                            parallel(windowsJobs + linuxJobs)
                        }
                    }
                }
            }
        }
        stage('Packaging') {
            when{
                anyOf{
                    equals expected: true, actual: params.BUILD_PACKAGES
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                }
                beforeAgent true
            }
            stages{
                stage('Building Source and Wheel formats'){
                    agent {
                        docker{
                            image 'python'
                            label 'linux && docker'
                          }
                    }
                    steps{
                        timeout(5){
                            withEnv(['PIP_NO_CACHE_DIR=off']) {
                                sh(label: 'Build Python Package',
                                   script: '''python -m venv venv --upgrade-deps
                                              venv/bin/pip install build
                                              venv/bin/python -m build .
                                              '''
                                    )
                            }
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
                stage('Testing Packages'){
                    when{
                        equals expected: true, actual: params.TEST_PACKAGES
                        beforeAgent true
                    }
                    steps{
                        script{
                            def windowsTests = [:]
                            SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                                if(params.INCLUDE_WINDOWS_X86_64 == true){
                                    windowsTests["Windows - Python ${pythonVersion}: sdist"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                    args: '-v pipcache_pyhathiprep:c:/users/containeradministrator/appdata/local/pip'
                                                ]
                                            ],
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.tar.gz,dist/*.zip').each{
                                                    bat(label: 'Running Tox', script: "tox --workdir %TEMP%\\tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')} -v")
                                                }
                                            },
                                            retries: 3
                                        )
                                    }
                                    windowsTests["Windows - Python ${pythonVersion}: wheel"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                    args: '-v pipcache_pyhathiprep:c:/users/containeradministrator/appdata/local/pip'
                                                ]
                                            ],
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                 findFiles(glob: 'dist/*.whl').each{
                                                     powershell(label: 'Running Tox', script: "tox --installpkg ${it.path} --workdir \$env:TEMP\\tox  -e py${pythonVersion.replace('.', '')}")
                                                 }

                                            },
                                            retries: 3
                                        )
                                    }
                                }
                            }
                            def linuxTests = [:]
                            SUPPORTED_LINUX_VERSIONS.each{ pythonVersion ->
                                def architectures = []
                                if(params.INCLUDE_LINUX_X86_64 == true){
                                    architectures.add('x86_64')
                                }
                                if(params.INCLUDE_LINUX_ARM == true){
                                    architectures.add('arm')
                                }
                                architectures.each{ processorArchitecture ->
                                    linuxTests["Linux ${processorArchitecture} - Python ${pythonVersion}: sdist"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: "linux && docker && ${processorArchitecture}",
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                    args: '-v pipcache_pyhathiprep:/.cache/pip'
                                                ]
                                            ],
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.tar.gz').each{
                                                    sh(
                                                        label: 'Running Tox',
                                                        script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                                        )
                                                }
                                            },
                                            retries: 3
                                        )
                                    }
                                    linuxTests["Linux ${processorArchitecture} - Python ${pythonVersion}: wheel"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: "linux && docker && ${processorArchitecture}",
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                    args: '-v pipcache_pyhathiprep:/.cache/pip'
                                                ]
                                            ],
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.whl').each{
                                                    timeout(5){
                                                        sh(
                                                            label: 'Running Tox',
                                                            script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                                            )
                                                    }
                                                }
                                            },
                                            retries: 3
                                        )
                                    }
                                }
                            }

                            def macTests = [:]
                            SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
                                def macArchitectures = []
                                if(params.INCLUDE_MACOS_X86_64 == true){
                                    macArchitectures.add('x86_64')
                                }
                                if(params.INCLUDE_MACOS_ARM == true){
                                    macArchitectures.add('m1')
                                }
                                macArchitectures.each{ processorArchitecture ->
                                    macTests["Mac ${processorArchitecture} - Python ${pythonVersion}: sdist"] = {
                                        testPythonPkg(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && ${processorArchitecture}",
                                                ],
                                                retries: 3,
                                                testSetup: {
                                                    checkout scm
                                                    unstash 'PYTHON_PACKAGES'
                                                    sh(
                                                        label:'Install Tox',
                                                        script: '''python3 -m venv venv
                                                                   venv/bin/pip install pip --upgrade
                                                                   venv/bin/pip install -r requirements/requirements-tox.txt
                                                                   '''
                                                    )
                                                },
                                                testCommand: {
                                                    findFiles(glob: 'dist/*.tar.gz').each{
                                                        sh(label: 'Running Tox',
                                                           script: "./venv/bin/tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}"
                                                        )
                                                    }
                                                },
                                                post:[
                                                    cleanup: {
                                                        sh 'rm -r venv/'
                                                    }
                                                ]
                                            )
                                    }
                                    macTests["Mac ${processorArchitecture} - Python ${pythonVersion}: wheel"] = {
                                        testPythonPkg(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && ${processorArchitecture}",
                                                ],
                                                retries: 3,
                                                testSetup: {
                                                    checkout scm
                                                    unstash 'PYTHON_PACKAGES'
                                                    sh(
                                                        label:'Install Tox',
                                                        script: '''python3 -m venv venv
                                                                   venv/bin/pip install pip --upgrade
                                                                   venv/bin/pip install -r requirements/requirements-tox.txt
                                                                   '''
                                                    )
                                                },
                                                testCommand: {
                                                    findFiles(glob: 'dist/*.whl').each{
                                                        sh(label: 'Running Tox',
                                                           script: "./venv/bin/tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}"
                                                        )
                                                    }
                                                },
                                                post:[
                                                    cleanup: {
                                                        sh 'rm -r venv/'
                                                    }
                                                ]

                                            )
                                    }
                                }
                            }
                            parallel(linuxTests + windowsTests + macTests)
                        }
                    }
                }
            }
        }
        stage('Deploy to Devpi'){
            when {
                allOf{
                    anyOf{
                        equals expected: true, actual: params.DEPLOY_DEVPI
                    }
                    anyOf {
                        equals expected: 'master', actual: env.BRANCH_NAME
                        equals expected: 'dev', actual: env.BRANCH_NAME
                        tag '*'
                    }
                }
                beforeAgent true
                beforeOptions true
            }
            agent none
            options{
                lock('pyhathiprep-devpi')
            }
            stages{
                stage('Uploading to DevPi Staging'){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/tox/Dockerfile'
                            label 'linux && docker && devpi-access'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                        }
                    }
                    steps {
                        timeout(5){
                            unstash 'DOCS_ARCHIVE'
                            unstash 'PYTHON_PACKAGES'
                            script{
                                devpi.upload(
                                        server: DEVPI_CONFIG.server,
                                        credentialsId: DEVPI_CONFIG.credentialsId,
                                        index: DEVPI_CONFIG.stagingIndex,
                                        clientDir: './devpi'
                                    )
                            }
                        }
                    }
                    post{
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                    [pattern: 'dist/', type: 'INCLUDE'],
                                    [pattern: '*.dist-info/', type: 'INCLUDE'],
                                    [pattern: 'build/', type: 'INCLUDE']
                                ]
                            )
                        }
                    }
                }
                stage('Test DevPi packages') {
                    steps{
                        script{
                            def macPackages = [:]
                            SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
                                def macArchitectures = []
                                if(params.INCLUDE_MACOS_X86_64 == true){
                                    macArchitectures.add('x86_64')
                                }
                                if(params.INCLUDE_MACOS_ARM == true){
                                    macArchitectures.add('m1')
                                }
                                macArchitectures.each{ processorArchitecture ->
                                    macPackages["Test Python ${pythonVersion}: wheel Mac ${processorArchitecture}"] = {
                                        withEnv([
                                            'PATH+EXTRA=./venv/bin'

                                        ]) {
                                            devpi.testDevpiPackage(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && devpi-access && ${processorArchitecture}"
                                                ],
                                                devpi: [
                                                    index: DEVPI_CONFIG.stagingIndex,
                                                    server: DEVPI_CONFIG.server,
                                                    credentialsId: DEVPI_CONFIG.credentialsId,
                                                    devpiExec: 'venv/bin/devpi'
                                                ],
                                                package:[
                                                    name: props.Name,
                                                    version: props.Version,
                                                    selector: 'whl'
                                                ],
                                                retries: 2,
                                                test:[
                                                    setup: {
                                                        checkout scm
                                                        sh(
                                                            label:'Installing Devpi client',
                                                            script: '''python3 -m venv venv
                                                                        venv/bin/python -m pip install pip --upgrade
                                                                        venv/bin/python -m pip install 'devpi-client<7.0' -r requirements/requirements-tox.txt
                                                                        '''
                                                        )
                                                    },
                                                    toxEnv: "py${pythonVersion}".replace('.',''),
                                                    teardown: {
                                                        sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                                    }
                                                ]
                                            )
                                        }
                                    }
                                    macPackages["Test Python ${pythonVersion}: sdist Mac ${processorArchitecture}"]= {
                                        withEnv([
                                            'PATH+EXTRA=./venv/bin'
                                        ]) {
                                            devpi.testDevpiPackage(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && devpi-access && ${processorArchitecture}"
                                                ],
                                                devpi: [
                                                    index: DEVPI_CONFIG.stagingIndex,
                                                    server: DEVPI_CONFIG.server,
                                                    credentialsId: DEVPI_CONFIG.credentialsId,
                                                    devpiExec: 'venv/bin/devpi'
                                                ],
                                                package:[
                                                    name: props.Name,
                                                    version: props.Version,
                                                    selector: 'tar.gz'
                                                ],
                                                retries: 2,
                                                test:[
                                                    setup: {
                                                        checkout scm
                                                        sh(
                                                            label:'Installing Devpi client',
                                                            script: '''python3 -m venv venv
                                                                        venv/bin/python -m pip install pip --upgrade
                                                                        venv/bin/python -m pip install 'devpi-client<7.0' -r requirements/requirements-tox.txt
                                                                        '''
                                                        )
                                                    },
                                                    toxEnv: "py${pythonVersion}".replace('.',''),
                                                    teardown: {
                                                        sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                                    }
                                                ]
                                            )
                                        }
                                    }
                                }
                            }
                            def windowsPackages = [:]
                            SUPPORTED_WINDOWS_VERSIONS.each{pythonVersion ->
                                if(params.INCLUDE_WINDOWS_X86_64 == true){
                                    windowsPackages["Test Python ${pythonVersion}: sdist Windows"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                    label: 'windows && docker && x86'
                                                ]
                                            ],
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            retries: 2,
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'tar.gz'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ]
                                        )
                                    }
                                    windowsPackages["Test Python ${pythonVersion}: wheel Windows"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                    label: 'windows && docker && x86 && devpi-access'
                                                ]
                                            ],
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            retries: 2,
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'whl'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ]
                                        )
                                    }
                                }
                            }
                            def linuxPackages = [:]
                            SUPPORTED_LINUX_VERSIONS.each{pythonVersion ->
                                linuxPackages["Test Python ${pythonVersion}: sdist Linux"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                label: 'linux && docker && x86 && devpi-access'
                                            ]
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        retries: 2,
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'tar.gz'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ]
                                    )
                                }
                                linuxPackages["Test Python ${pythonVersion}: wheel Linux"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                label: 'linux && docker && x86 && devpi-access'
                                            ]
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        retries: 2,
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'whl'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ]
                                    )
                                }
                            }
                            parallel(macPackages + windowsPackages + linuxPackages)
                        }
                    }
                }
                stage('Deploy to DevPi Production') {
                    when {
                        allOf{
                            equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                            anyOf {
                                equals expected: 'master', actual: env.BRANCH_NAME
                                tag '*'
                            }
                        }
                        beforeAgent true
                        beforeInput true
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux && docker && devpi-access'
                          }
                    }
                    input {
                        message 'Release to DevPi Production?'
                    }
                    steps {
                        script{
                            devpi.pushPackageToIndex(
                                pkgName: props.Name,
                                pkgVersion: props.Version,
                                server: DEVPI_CONFIG.server,
                                indexSource: DEVPI_CONFIG.stagingIndex,
                                indexDestination: 'production/release',
                                credentialsId: DEVPI_CONFIG.credentialsId
                            )
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker && devpi-access') {
                        checkout scm
                        script{
                            if (!env.TAG_NAME?.trim()){
                                def dockerImage = docker.build('pyhathiprep:devpi','-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL .')
                                dockerImage.inside{
                                    devpi.pushPackageToIndex(
                                        pkgName: props.Name,
                                        pkgVersion: props.Version,
                                        server: DEVPI_CONFIG.server,
                                        indexSource: DEVPI_CONFIG.stagingIndex,
                                        indexDestination: "DS_Jenkins/${env.BRANCH_NAME}",
                                        credentialsId: DEVPI_CONFIG.credentialsId
                                    )
                                }
                                sh script: "docker image rm --no-prune ${dockerImage.imageName()}"
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker && x86 && devpi-access') {
                       script{
                            def dockerImage = docker.build('pyhathiprep:devpi','-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL .')
                            dockerImage.inside{
                                devpi.removePackage(
                                    pkgName: props.Name,
                                    pkgVersion: props.Version,
                                    index: DEVPI_CONFIG.stagingIndex,
                                    server: DEVPI_CONFIG.server,
                                    credentialsId: DEVPI_CONFIG.credentialsId,

                                )
                            }
                            sh script: "docker image rm --no-prune ${dockerImage.imageName()}"
                       }
                    }
                }
            }
        }
        stage('Deploy'){
            parallel{
                stage('Deploy to pypi') {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker && x86'
                        }
                    }
                    when{
                         allOf{
                            equals expected: true, actual: params.DEPLOY_PYPI
                            equals expected: true, actual: params.BUILD_PACKAGES

                        }
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
                        pypiUpload(
                                credentialsId: 'jenkins-nexus',
                                repositoryUrl: SERVER_URL,
                                glob: 'dist/*'
                        )
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
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker && x86'
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
                            sh 'python utils/upload_docs.py --username=$docsUsername --password=$docsPassword --subroute=pyhathiprep build/docs/html apache-ns.library.illinois.edu'
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
