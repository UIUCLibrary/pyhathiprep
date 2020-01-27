#!groovy
@Library("ds-utils@v0.1.0") // Uses library from https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*
@Library(["devpi", "PythonHelpers"]) _


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


pipeline {
    agent none
    options {
        disableConcurrentBuilds()  //each branch has 1 job running at a time
        timeout(60)  // Timeout after 60 minutes. This shouldn't take this long but it hangs for some reason
    }
    triggers {
        cron('@daily')
    }
    environment {
        DEVPI = credentials("DS_devpi")
    }
    parameters {
        booleanParam(name: "FRESH_WORKSPACE", defaultValue: false, description: "Purge workspace before staring and checking out source")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: true, description: "Run Tox Tests")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        string(name: 'URL_SUBFOLDER', defaultValue: "pyhathiprep", description: 'The directory that the docs should be saved under')
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    }
    stages {
        stage("Getting Distribution Info"){
            agent {
                dockerfile {
                    filename 'CI/docker/python37/windows/build/msvc/Dockerfile'
                    label "windows && docker"
                }
            }
            steps{
                bat "python setup.py dist_info"
            }
            post{
                success{
                    stash includes: "pyhathiprep.dist-info/**", name: 'DIST-INFO'
                    archiveArtifacts artifacts: "pyhathiprep.dist-info/**"
                }
                cleanup{
                    cleanWs(
                        deleteDirs: true,
                        patterns: [
                            [pattern: "pyhathiprep.dist-info/", type: 'INCLUDE'],
                            ]
                    )
                }
            }
        }
//         stage("Configure") {
//             environment {
//                 PATH = "${tool 'CPython-3.6'};$PATH"
//             }
//             stages{
//                 stage("Purge All Existing Data in Workspace"){
//                     when{
//                         equals expected: true, actual: params.FRESH_WORKSPACE
//                     }
//                     steps{
//                         deleteDir()
//                         checkout scm
//                     }
//                     post{
//                         success{
//                             bat "dir /s /B"
//                         }
//                     }
//                 }
//                 stage("Installing Required System Level Dependencies"){
//                     steps{
//                         lock("system_python_${NODE_NAME}"){
//                             bat "python -m pip install --upgrade pip --quiet"
//                         }
//                     }
//                     post{
//                         always{
//                             bat "if not exist logs mkdir logs"
//                             lock("system_python_${NODE_NAME}"){
//                                 bat "python -m pip list > logs\\pippackages_system_${NODE_NAME}.log"
//                             }
//                             archiveArtifacts artifacts: "logs/pippackages_system_${NODE_NAME}.log"
//                         }
//                         failure {
//                             deleteDir()
//                         }
//                     }
//                 }
//                 stage("Getting Distribution Info"){
//                     environment{
//                         PATH = "${tool 'CPython-3.7'};$PATH"
//                     }
//                     steps{
//                         bat "python setup.py dist_info"
//                     }
//                     post{
//                         success{
//                             stash includes: "pyhathiprep.dist-info/**", name: 'DIST-INFO'
//                             archiveArtifacts artifacts: "pyhathiprep.dist-info/**"
//                         }
//                     }
//                 }
//                 stage("Creating Virtualenv for Building"){
//                     steps{
//                         bat "python -m venv venv"
//                         script {
//                             try {
//                                 bat "call venv\\Scripts\\python.exe -m pip install -U pip"
//                             }
//                             catch (exc) {
//                                 bat "python -m venv venv"
//                                 bat "call venv\\Scripts\\python.exe -m pip install -U pip --no-cache-dir"
//                             }
//                         }
//                         bat "venv\\Scripts\\pip.exe install -U setuptools"
//                         bat "venv\\Scripts\\pip.exe install pytest pytest-cov coverage lxml -r requirements.txt -r requirements-dev.txt -r requirements-freeze.txt --upgrade-strategy only-if-needed"
//                         bat 'venv\\Scripts\\pip.exe install "tox>=3.7,<3.10"'
//                     }
//                     post{
//                         success{
//                             bat "venv\\Scripts\\pip.exe list > ${WORKSPACE}\\logs\\pippackages_venv_${NODE_NAME}.log"
//                             archiveArtifacts artifacts: "logs/pippackages_venv_${NODE_NAME}.log"
//                         }
//                     }
//                 }
//             }
//         }
        stage("Building") {
            agent {
                dockerfile {
                    filename 'CI/docker/python37/windows/build/msvc/Dockerfile'
                    label "windows && docker"
                }
            }
            stages{
                stage("Building Python Package"){
                    steps {
                        bat "if not exist logs mkdir logs"
                        powershell "& python setup.py build -b ${WORKSPACE}\\build  | tee ${WORKSPACE}\\logs\\build.log"
                    }
                    post{
                        always{
                            recordIssues(tools: [
                                    pyLint(name: 'Setuptools Build: PyLint', pattern: 'logs/build.log'),
                                ]
                            )
                            archiveArtifacts artifacts: "logs/build.log"
                        }
                        failure{
                            echo "Failed to build Python package"
                        }
                    }
                }
                stage("Building Sphinx Documentation"){
                    environment{
                        PKG_NAME = get_package_name("DIST-INFO", "pyhathiprep.dist-info/METADATA")
                        PKG_VERSION = get_package_version("DIST-INFO", "pyhathiprep.dist-info/METADATA")
                    }
                    steps {
                        echo "Building docs on ${env.NODE_NAME}"
                        bat "python -m sphinx docs/source build/docs/html -d build/docs/.doctrees -v -w ${WORKSPACE}\\logs\\build_sphinx.log"
                    }
                    post{
                        always {
                            recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log')])
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            script{
                                def DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
                                zip archive: true, dir: "build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                                stash includes: "dist/${DOC_ZIP_FILENAME},build/docs/html/**", name: 'DOCS_ARCHIVE'
                            }
                        }
                        failure{
                            echo "Failed to build Python package"
                        }
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                    [pattern: "dist/", type: 'INCLUDE'],
                                    [pattern: 'build/', type: 'INCLUDE'],
                                    [pattern: 'logs/', type: 'INCLUDE']
                                    ]
                            )
                        }
                    }
                }
            }
        }
        stage("Tests") {
            agent {
                dockerfile {
                    filename 'CI/docker/python37/windows/build/msvc/Dockerfile'
                    label "windows && docker"
                }
            }
            stages{
                stage("Setting up Tests"){
                    steps{
                        bat "if not exist reports mkdir reports"
                        bat "if not exist logs mkdir logs"
                    }
                }
                stage("Run Tests"){
                    parallel {
                        stage("PyTest"){
                            steps{
                                catchError(buildResult: 'UNSTABLE', message: 'Pytest tests failed', stageResult: 'UNSTABLE') {
                                    bat "coverage run --parallel-mode --source=pyhathiprep -m pytest --junitxml=${WORKSPACE}/reports/pytest/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest" //  --basetemp={envtmpdir}"
                                }
                            }
                            post{
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: '.pytest_cache/', type: 'INCLUDE'],
                                        ]
                                    )
                                }
                            }
                        }
                        stage("Run Tox Test") {
                            when{
                                equals expected: true, actual: params.TEST_RUN_TOX
                            }
                            steps {
                                bat "tox --version"
                                catchError(buildResult: 'UNSTABLE', message: 'Tox Failed', stageResult: 'UNSTABLE') {
                                    bat "tox  --workdir ${WORKSPACE}\\.tox -v -e py"
                                }
                            }
                            post{
                                always{
                                    archiveArtifacts(
                                        allowEmptyArchive: true,
                                        artifacts: '.tox/py*/log/*.log,.tox/log/*.log'
                                    )
                                }
                                cleanup{
                                    cleanWs deleteDirs: true, patterns: [
                                        [pattern: '.tox/', type: 'INCLUDE'],
                                    ]
                                }
                            }
                        }
                        stage("Documentation"){
                            steps{
                                bat "coverage run --parallel-mode --source=pyhathiprep setup.py build_sphinx --source-dir=docs/source --build-dir=${WORKSPACE}\\build\\docs --builder=doctest"
                            }
                        }
                        stage("MyPy"){
                            steps{
                                catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                    bat returnStatus: true, script: "mypy.exe -p pyhathiprep --junit-xml=${WORKSPACE}/reports/mypy/junit-${env.NODE_NAME}-mypy.xml --html-report ${WORKSPACE}/reports/mypy/mypy_html > ${WORKSPACE}\\logs\\mypy.log"
                                }
                            }
                            post{
                                always {
                                    junit "reports/mypy/junit-${env.NODE_NAME}-mypy.xml"
                                    recordIssues(tools: [myPy(name: 'MyPy', pattern: 'logs/mypy.log')])
                                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                                }
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: 'reports/mypy/', type: 'INCLUDE'],
                                            [pattern: '.mypy_cache/', type: 'INCLUDE'],
                                        ]
                                    )
                                }
                            }
                        }
                        stage("Run Flake8 Static Analysis") {
                            steps{
                                catchError(buildResult: 'SUCCESS', message: 'Flake8 found issues', stageResult: 'UNSTABLE') {
                                    bat "flake8 pyhathiprep --tee --output-file=${WORKSPACE}/logs/flake8.log"
                                }
                            }
                            post {
                                always {
                                    stash includes: "logs/flake8.log", name: 'FLAKE8_LOGS'
                                    unstash "FLAKE8_LOGS"
                                    recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                }
                                cleanup{
                                    cleanWs(patterns: [[pattern: 'logs/flake8.log', type: 'INCLUDE']])
                                }
                            }
                        }
                    }
                    post{
                        always{
                            bat "coverage combine"
                            bat "coverage xml -o reports\\coverage.xml"
                            bat "coverage html -d reports\\coverage"
                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: "reports/coverage", reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                            publishCoverage adapters: [
                                            coberturaAdapter('reports/coverage.xml')
                                            ],
                                        sourceFileResolver: sourceFiles('STORE_ALL_BUILD')
                        }
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                    [pattern: "dist/", type: 'INCLUDE'],
                                    [pattern: 'build/', type: 'INCLUDE'],
                                    [pattern: 'pyhathiprep.egg-info/', type: 'INCLUDE'],
                                    [pattern: 'reports/', type: 'INCLUDE'],
                                    [pattern: 'logs/', type: 'INCLUDE']
                                    ]
                            )
                        }
                    }
                }
            }
        }
        stage("Packaging") {
            parallel {
                stage("Source and Wheel formats"){
                    agent {
                        dockerfile {
                            filename 'CI/docker/python37/windows/build/msvc/Dockerfile'
                            label "windows && docker"
                        }
                    }
                    steps{
                        bat "python setup.py sdist -d ${WORKSPACE}\\dist --format zip bdist_wheel -d ${WORKSPACE}\\dist"
                    }
                    post{
                        success{
                            archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz", fingerprint: true
                            stash includes: 'dist/*.whl,dist/*.tar.gz', name: "DIST"
                        }
                        cleanup{
                            cleanWs deleteDirs: true, patterns: [[pattern: 'dist/*.whl,dist/*.zip', type: 'INCLUDE']]
                        }
                    }
                }
                stage("Windows CX_Freeze MSI"){
                    agent {
                        dockerfile {
                            filename 'CI/docker/python37/windows/build/msvc/Dockerfile'
                            label "windows && docker"
                        }
                    }
                    steps{
                        bat "python cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir ${WORKSPACE}/build/msi -d ${WORKSPACE}/dist"
                    }
                    post{
                        success{
                            stash includes: "dist/*.msi", name: "msi"
                            archiveArtifacts artifacts: "dist/*.msi", fingerprint: true
                        }
                        cleanup{
                            cleanWs deleteDirs: true, patterns: [[pattern: 'dist/*.msi', type: 'INCLUDE']]
                        }
                    }
                }
            }
        }
         stage("Deploy to DevPi") {
            when {
                allOf{
                    anyOf{
                        equals expected: true, actual: params.DEPLOY_DEVPI
                        triggeredBy "TimerTriggerCause"
                    }
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
            }
            options{
                timestamps()
            }
            environment{
                PATH = "${WORKSPACE}\\venv\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${PATH}"
                PKG_NAME = get_package_name("DIST-INFO", "pyhathiprep.dist-info/METADATA")
                PKG_VERSION = get_package_version("DIST-INFO", "pyhathiprep.dist-info/METADATA")
            }
            stages{
                stage("Upload to DevPi Staging"){
                    steps {
                        unstash "DIST"
                        unstash "DOCS_ARCHIVE"
                        bat "pip install devpi-client"
                        devpiUpload(
                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                            url: "https://devpi.library.illinois.edu",
                            index: "${env.BRANCH_NAME}_staging",
                            distPath: "dist"
                            )
                    }
                }
                stage("Test DevPi Packages") {
                    parallel {
                        stage("Testing Submitted Source Distribution") {
                            environment {
                                PATH = "${tool 'CPython-3.7'};${tool 'CPython-3.6'};$PATH"
                            }
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            options {
                                skipDefaultCheckout(true)
                            }
                            stages{
                                stage("Creating Virtualenv to Test Sdist"){
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "python -m venv venv"
                                        }
                                        bat "venv\\Scripts\\python.exe -m pip install pip --upgrade && venv\\Scripts\\pip.exe install setuptools --upgrade && venv\\Scripts\\pip.exe install \"tox<3.7\" detox devpi-client"
                                    }
                                }
                                stage("Testing DevPi zip Package"){
                                    options{
                                        timeout(20)
                                    }
                                    environment {
                                        PATH = "${WORKSPACE}\\venv\\Scripts;$PATH"
                                    }
                                    steps {
                                        devpiTest(
                                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                            url: "https://devpi.library.illinois.edu",
                                            index: "${env.BRANCH_NAME}_staging",
                                            pkgName: "${env.PKG_NAME}",
                                            pkgVersion: "${env.PKG_VERSION}",
                                            pkgRegex: "zip",
                                            detox: false
                                        )
                                        echo "Finished testing Source Distribution: .zip"
                                    }
                                }
                            }
                            post {
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        disableDeferredWipeout: true,
                                        patterns: [
                                            [pattern: '*tmp', type: 'INCLUDE'],
                                            [pattern: 'certs', type: 'INCLUDE'],
                                            ]
                                    )
                                }
                            }
                        }
                        stage("Built Distribution: .whl") {
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            environment {
                                PATH = "${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${tool 'CPython-3.7'};$PATH"
                            }
                            options {
                                skipDefaultCheckout(true)
                            }
                            stages{
                                stage("Creating venv to Test Whl"){
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "if not exist venv\\36 mkdir venv\\36"
                                            bat "\"${tool 'CPython-3.6'}\\python.exe\" -m venv venv\\36"
                                            bat "if not exist venv\\37 mkdir venv\\37"
                                            bat "\"${tool 'CPython-3.7'}\\python.exe\" -m venv venv\\37"
                                        }
                                        bat "venv\\36\\Scripts\\python.exe -m pip install pip --upgrade && venv\\36\\Scripts\\pip.exe install setuptools --upgrade && venv\\36\\Scripts\\pip.exe install \"tox<3.7\" devpi-client"
                                    }
                                }
                                stage("Testing DevPi .whl Package"){
                                    options{
                                        timeout(20)
                                    }
                                    environment {
                                        PATH = "${WORKSPACE}\\venv\\36\\Scripts;${WORKSPACE}\\venv\\37\\Scripts;$PATH"
                                    }
                                    steps {
                                        echo "Testing Whl package in devpi"
                                        devpiTest(
                                                devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                                url: "https://devpi.library.illinois.edu",
                                                index: "${env.BRANCH_NAME}_staging",
                                                pkgName: "${env.PKG_NAME}",
                                                pkgVersion: "${env.PKG_VERSION}",
                                                pkgRegex: "whl",
                                                detox: false
                                            )
                                        echo "Finished testing Built Distribution: .whl"
                                    }
                                }
                            }
                            post {
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        disableDeferredWipeout: true,
                                        patterns: [
                                            [pattern: '*tmp', type: 'INCLUDE'],
                                            [pattern: 'certs', type: 'INCLUDE']
                                            ]
                                    )
                                }
                            }
                        }
                    }
                }
                stage("Deploy to DevPi Production") {
                        when {
                            allOf{
                                equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                                branch "master"
                            }
                        }
                        steps {
                            script {
                                try{
                                    timeout(30) {
                                        input "Release ${env.PKG_NAME} ${env.PKG_VERSION} (https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging/${env.PKG_NAME}/${env.PKG_VERSION}) to DevPi Production? "
                                    }
                                    bat "devpi.exe login ${env.DEVPI_USR} --password ${env.DEVPI_PSW}"
                                    bat "devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
                                    bat "devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} production/release"
                                } catch(err){
                                    echo "User response timed out. Packages not deployed to DevPi Production."
                                }
                            }
                        }
                }
            }
            post {
                success {
                    echo "it Worked. Pushing file to ${env.BRANCH_NAME} index"
                    bat "venv\\Scripts\\devpi.exe login ${env.DEVPI_USR} --password ${env.DEVPI_PSW}"
                    bat "venv\\Scripts\\devpi.exe use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging"
                    bat "venv\\Scripts\\devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} ${env.DEVPI_USR}/${env.BRANCH_NAME}"
                }
                cleanup{
                    remove_from_devpi("venv\\Scripts\\devpi.exe", "${env.PKG_NAME}", "${env.PKG_VERSION}", "/${env.DEVPI_USR}/${env.BRANCH_NAME}_staging", "${env.DEVPI_USR}", "${env.DEVPI_PSW}")
                }
                failure {
                    echo "At least one package format on DevPi failed."
                }
            }
        }
        stage("Deploy - SCCM"){
            agent any
            options {
                skipDefaultCheckout(true)
            }
            when{
                allOf{
                    equals expected: true, actual: params.DEPLOY_SCCM
                    branch "master"
                }
            }
            stages{
                 stage("Deploy - Staging") {
                    steps {
                        deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                        input("Deploy to production?")
                    }
                }
                stage("Deploy - SCCM Upload") {
                    steps {
                        deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
                    }
                    post {
                        success {
                            script{
                                unstash "Source"
                                def  deployment_request = requestDeploy this, "deployment.yml"
                                echo deployment_request
                                writeFile file: "deployment_request.txt", text: deployment_request
                                archiveArtifacts artifacts: "deployment_request.txt"
                            }
                        }
                    }
                }
            }
        }
        stage("Update Online Documentation") {
            agent any
            when {
                equals expected: true, actual: params.UPDATE_DOCS
            }
            options {
                skipDefaultCheckout(true)
            }
            steps {
                unstash "DOCS_ARCHIVE"
                dir("build/docs/html/"){
                    sshPublisher(
                        publishers: [
                            sshPublisherDesc(
                                configName: 'apache-ns - lib-dccuser-updater',
                                sshLabel: [label: 'Linux'],
                                transfers: [sshTransfer(excludes: '',
                                execCommand: '',
                                execTimeout: 120000,
                                flatten: false,
                                makeEmptyDirs: false,
                                noDefaultExcludes: false,
                                patternSeparator: '[, ]+',
                                remoteDirectory: "${params.URL_SUBFOLDER}",
                                remoteDirectorySDF: false,
                                removePrefix: '',
                                sourceFiles: '**')],
                            usePromotionTimestamp: false,
                            useWorkspaceInPromotion: false,
                            verbose: true
                            )
                        ]
                    )
                }
            }
        }
    }
}
