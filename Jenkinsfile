#!groovy
@Library("ds-utils@v0.1.0") // Uses library from https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*
@Library("devpi") _

def PKG_NAME = "unknown"
def PKG_VERSION = "unknown"
def DOC_ZIP_FILENAME = "doc.zip"
def junit_filename = "junit.xml"
def REPORT_DIR = ""
def VENV_ROOT = ""
def VENV_PYTHON = ""
def VENV_PIP = ""

pipeline {
    agent {
        label "Windows && VS2015 && Python3 && longfilenames"
    }
    options {
        disableConcurrentBuilds()  //each branch has 1 job running at a time
        timeout(60)  // Timeout after 60 minutes. This shouldn't take this long but it hangs for some reason
        checkoutToSubdirectory("source")
    }
    triggers {
        cron('@daily')
    }
    environment {
        PATH = "${tool 'CPython-3.6'};${tool 'CPython-3.7'};$PATH"
    }
    // environment {
        //mypy_args = "--junit-xml=mypy.xml"
        //pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    // }
    parameters {
        booleanParam(name: "FRESH_WORKSPACE", defaultValue: false, description: "Purge workspace before staring and checking out source")
        booleanParam(name: "BUILD_DOCS", defaultValue: true, description: "Build documentation")
        booleanParam(name: "TEST_RUN_DOCTEST", defaultValue: true, description: "Test documentation")
//        booleanParam(name: "TEST_RUN_FLAKE8", defaultValue: true, description: "Run Flake8 static analysis")
        booleanParam(name: "TEST_RUN_FLAKE8", defaultValue: true, description: "Run Flake8 Tests")
        booleanParam(name: "TEST_RUN_PYTEST", defaultValue: true, description: "Run unit tests with PyTest")
        booleanParam(name: "TEST_RUN_MYPY", defaultValue: true, description: "Run MyPy static analysis")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: true, description: "Run Tox Tests")

        booleanParam(name: "DEPLOY_DEVPI", defaultValue: true, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        // choice(choices: 'None\nrelease', description: "Release the build to production. Only available in the Master branch", name: 'RELEASE')
        string(name: 'URL_SUBFOLDER', defaultValue: "pyhathiprep", description: 'The directory that the docs should be saved under')
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    }
    stages {
        stage("Configure") {
            stages{
                stage("Purge all existing data in workspace"){
                    when{
                        equals expected: true, actual: params.FRESH_WORKSPACE
                    }
                    steps{
                        deleteDir()
                        dir("source"){
                            checkout scm
                        }
                    }
                    post{
                        success{
                            bat "dir /s /B"
                        }
                    }
                }
//                stage("Cleanup"){
//                    steps {
//
//                        dir("build"){
//                            deleteDir()
//                            echo "Cleaned out build directory"
//                            bat "dir"
//                        }
//                        dir("dist"){
//                            deleteDir()
//                            echo "Cleaned out dist directory"
//                            bat "dir"
//                        }
//
//                        dir("reports"){
//                            deleteDir()
//                            echo "Cleaned out reports directory"
//                            bat "dir"
//                        }
//                    }
//                    post{
//                        failure {
//                            deleteDir()
//                        }
//                    }
//                }
                stage("Installing required system level dependencies"){
                    steps{
                        lock("system_python_${NODE_NAME}"){
                            bat "${tool 'CPython-3.6'}\\python -m pip install --upgrade pip --quiet"
                        }
                    }
                    post{
                        always{
                            bat "if not exist logs mkdir logs"
                            lock("system_python_${NODE_NAME}"){
                                bat "${tool 'CPython-3.6'}\\python -m pip list > logs\\pippackages_system_${NODE_NAME}.log"
                            }
                            archiveArtifacts artifacts: "logs/pippackages_system_${NODE_NAME}.log"
                        }
                        failure {
                            deleteDir()
                        }
                    }
                }
                stage("Creating virtualenv for building"){
                    steps{
                        bat "${tool 'CPython-3.6'}\\python -m venv venv"
                        script {
                            try {
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip"
                            }
                            catch (exc) {
                                bat "${tool 'CPython-3.6'}\\python -m venv venv"
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip --no-cache-dir"
                            }
                        }
                        bat "venv\\Scripts\\pip.exe install -U setuptools"
//                        TODO: when detox is fixed, just use the most recent version
                        bat "venv\\Scripts\\pip.exe install devpi-client pytest pytest-cov lxml -r source\\requirements.txt -r source\\requirements-dev.txt -r source\\requirements-freeze.txt --upgrade-strategy only-if-needed"
                        bat "venv\\Scripts\\pip.exe install detox==0.13 tox==3.2.1"
                    }
                    post{
                        success{
                            bat "venv\\Scripts\\pip.exe list > ${WORKSPACE}\\logs\\pippackages_venv_${NODE_NAME}.log"
                            archiveArtifacts artifacts: "logs/pippackages_venv_${NODE_NAME}.log"
                        }
                    }
                }
                stage("Setting variables used by the rest of the build"){
                    steps{

                        script {
                            // Set up the reports directory variable
                            REPORT_DIR = "${WORKSPACE}\\reports"
                            dir("source"){
                                PKG_NAME = bat(returnStdout: true, script: "@${tool 'CPython-3.6'}\\python  setup.py --name").trim()
                                PKG_VERSION = bat(returnStdout: true, script: "@${tool 'CPython-3.6'}\\python setup.py --version").trim()
                            }
                        }

                        script{
                            DOC_ZIP_FILENAME = "${PKG_NAME}-${PKG_VERSION}.doc.zip"
                            junit_filename = "junit-${env.NODE_NAME}-${env.GIT_COMMIT.substring(0,7)}-pytest.xml"
                        }




                        script{
                            VENV_ROOT = "${WORKSPACE}\\venv\\"

                            VENV_PYTHON = "${WORKSPACE}\\venv\\Scripts\\python.exe"
                            bat "${VENV_PYTHON} --version"

                            VENV_PIP = "${WORKSPACE}\\venv\\Scripts\\pip.exe"
                            bat "${VENV_PIP} --version"
                        }


                        bat "venv\\Scripts\\devpi use https://devpi.library.illinois.edu"
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                        }
                        bat "dir"
                    }
                }
            }
            post{
                always{
                    echo """Name                            = ${PKG_NAME}
Version                         = ${PKG_VERSION}
Report Directory                = ${REPORT_DIR}
documentation zip file          = ${DOC_ZIP_FILENAME}
Python virtual environment path = ${VENV_ROOT}
VirtualEnv Python executable    = ${VENV_PYTHON}
VirtualEnv Pip executable       = ${VENV_PIP}
junit_filename                  = ${junit_filename}
"""

                }

            }

        }
        stage("Building") {
            stages{
                stage("Building Python Package"){
                    steps {


                        dir("source"){
                            powershell "& ${WORKSPACE}\\venv\\Scripts\\python.exe setup.py build -b ${WORKSPACE}\\build  | tee ${WORKSPACE}\\logs\\build.log"
                        }

                    }
                    post{
                        always{
                             recordIssues(tools: [
                                    pyLint(name: 'Setuptools Build: PyLint', pattern: 'logs/build.log'),
                                ]
                            )
//                            warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'Pep8', pattern: 'logs/build.log']]
                            archiveArtifacts artifacts: "logs/build.log"
                        }
                        failure{
                            echo "Failed to build Python package"
                        }
                    }
                }
                stage("Building Sphinx Documentation"){
                    steps {
                        echo "Building docs on ${env.NODE_NAME}"
                        dir("source"){
                            powershell "& ${WORKSPACE}\\venv\\Scripts\\python.exe setup.py build_sphinx --build-dir ${WORKSPACE}\\build\\docs | tee ${WORKSPACE}\\logs\\build_sphinx.log"
                        }
                    }
                    post{
                        always {
                            recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log')])
//                            warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'Pep8', pattern: 'logs/build_sphinx.log']]
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            zip archive: true, dir: "build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                            stash includes: "dist/${DOC_ZIP_FILENAME},build/docs/html/**", name: 'DOCS_ARCHIVE'
                        }
                        failure{
                            echo "Failed to build Python package"
                        }
                    }
                }
            }
        }
        stage("Tests") {
            parallel {
                stage("PyTest"){
                    when {
                        equals expected: true, actual: params.TEST_RUN_PYTEST
                    }
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe run --parallel-mode --source=pyhathiprep -m pytest --junitxml=${WORKSPACE}/reports/pytest/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest" //  --basetemp={envtmpdir}"
                        }

                    }
                }
                stage("Run Tox test") {
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    steps {
                        dir("source"){
                            script{
                                try{
                                    bat "${WORKSPACE}\\venv\\Scripts\\detox --workdir ${WORKSPACE}\\.tox"
                                } catch (exc) {
                                    bat "${WORKSPACE}\\venv\\Scripts\\detox --workdir ${WORKSPACE}\\.tox --recreate"
                                }
                            }

                        }
                    }
                }
                stage("Documentation"){
                    when{
                        equals expected: true, actual: params.TEST_RUN_DOCTEST
                    }
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe run --parallel-mode --source=pyhathiprep setup.py build_sphinx --source-dir=docs/source --build-dir=${WORKSPACE}\\build\\docs --builder=doctest"
                        }
                    }

                }
                stage("MyPy"){
                    when{
                        equals expected: true, actual: params.TEST_RUN_MYPY
                    }
                    steps{
                        bat "if not exist reports\\mypy mkdir reports\\mypy"
                        dir("source") {

                            bat returnStatus: true, script: "${WORKSPACE}\\venv\\Scripts\\mypy.exe -p pyhathiprep --junit-xml=${WORKSPACE}/reports/mypy/junit-${env.NODE_NAME}-mypy.xml --html-report ${WORKSPACE}/reports/mypy/mypy_html > ${WORKSPACE}\\logs\\mypy.log"
                        }
                    }
                    post{
                        always {
                            junit "reports/mypy/junit-${env.NODE_NAME}-mypy.xml"
                            recordIssues(tools: [myPy(name: 'MyPy', pattern: 'logs/mypy.log')])
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                        }
                        cleanup{
                            cleanWs deleteDirs: true, patterns: [[pattern: 'reports/mypy', type: 'INCLUDE']]
                        }
                    }
                }
                stage("Run Flake8 Static Analysis") {
                    when {
                        equals expected: true, actual: params.TEST_RUN_FLAKE8
                    }
                    steps{
                        script{
                            bat "venv\\Scripts\\pip.exe install flake8"
                            try{
                                dir("source"){
                                    bat "${WORKSPACE}\\venv\\Scripts\\flake8.exe pyhathiprep --tee --output-file=${WORKSPACE}\\logs\\flake8.log"
                                }
                            } catch (exc) {
                                echo "flake8 found some warnings"
                            }
                        }
                    }
                    post {
                        always {
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
                    dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe combine"
                            bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe xml -o ${WORKSPACE}\\reports\\coverage.xml"
                            bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe html -d ${WORKSPACE}\\reports\\coverage"

                    }
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: "reports/coverage", reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                    publishCoverage adapters: [
                                    coberturaAdapter('reports/coverage.xml')
                                    ],
                                sourceFileResolver: sourceFiles('STORE_ALL_BUILD')
                }
                cleanup{
                    cleanWs(patterns: [
                            [pattern: 'reports/coverage.xml', type: 'INCLUDE'],
                            [pattern: 'reports/coverage', type: 'INCLUDE'],
                            [pattern: 'source/.coverage', type: 'INCLUDE']
                        ]
                    )
                }
            }
        }
        stage("Packaging") {
            parallel {
                stage("Source and Wheel formats"){
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\scripts\\python.exe setup.py sdist -d ${WORKSPACE}\\dist bdist_wheel -d ${WORKSPACE}\\dist"
                        }

                    }
                    post{
                        success{
                            archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz", fingerprint: true
                            stash includes: 'dist/*.whl,dist/*.tar.gz', name: "DIST"
                        }
                        cleanup{
                            cleanWs deleteDirs: true, patterns: [[pattern: 'dist/*.whl,dist/*.tar.gz', type: 'INCLUDE']]
                        }
                    }
                }

                stage("Windows CX_Freeze MSI"){
//                    }
                    steps{
                        bat "if not exist dist mkdir dist"
                        bat "venv\\Scripts\\pip.exe install -r source\\requirements.txt -r source\\requirements-dev.txt -r source\\requirements-freeze.txt"
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\python.exe cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir build/msi -d ${WORKSPACE}/dist"
                        }


                    }
                    post{
                        success{
                            dir("dist") {
                                stash includes: "*.msi", name: "msi"
                            }
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
            stages{
                stage("Upload to DevPi Staging"){
                    steps {
                        unstash "DIST"
                        unstash "DOCS_ARCHIVE"
                        bat "venv\\Scripts\\devpi.exe use https://devpi.library.illinois.edu"
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"

                        }
                        bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
                        script {
                                bat "venv\\Scripts\\devpi.exe upload --from-dir dist"
                                try {
                                    bat "venv\\Scripts\\devpi.exe upload --only-docs ${WORKSPACE}\\dist\\${DOC_ZIP_FILENAME}"
                                } catch (exc) {
                                    echo "Unable to upload to devpi with docs."
                                }
                            }

                    }
                }
                stage("Test DevPi packages") {

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
                                stage("Creating venv to test sdist"){
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "${tool 'CPython-3.6'}\\python -m venv venv"
                                        }
                                        bat "venv\\Scripts\\python.exe -m pip install pip --upgrade && venv\\Scripts\\pip.exe install setuptools --upgrade && venv\\Scripts\\pip.exe install \"tox<3.7\" detox devpi-client"
                                    }

                                }
                                stage("Testing DevPi tar.gz Package"){
                                    steps {
                                        echo "Testing Source tar.gz package in devpi"
                                        bat "where python"
                                        timeout(20){
                                            devpiTest(
                                                devpiExecutable: "venv\\Scripts\\devpi.exe",
                                                url: "https://devpi.library.illinois.edu",
                                                index: "${env.BRANCH_NAME}_staging",
                                                pkgName: "${PKG_NAME}",
                                                pkgVersion: "${PKG_VERSION}",
                                                pkgRegex: "tar.gz",
                                                detox: false
                                            )
                                        }
                                        echo "Finished testing Source Distribution: .tar.gz"
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
                        stage("Built Distribution: .whl") {
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            environment {
                                PATH = "${tool 'CPython-3.7'};${tool 'CPython-3.6'};$PATH"
                            }
                            options {
                                skipDefaultCheckout(true)
                            }
                            stages{
                                stage("Creating venv to test sdist"){
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "${tool 'CPython-3.6'}\\python -m venv venv"
                                        }
                                        bat "venv\\Scripts\\python.exe -m pip install pip --upgrade && venv\\Scripts\\pip.exe install setuptools --upgrade && venv\\Scripts\\pip.exe install \"tox<3.7\" detox devpi-client"
                                        bat "venv\\Scripts\\pip.exe install devpi --upgrade"
                                    }

                                }
                                stage("Testing DevPi .whl Package"){

                                    steps {
                                        echo "Testing Whl package in devpi"
                                        bat "where python"
                                        devpiTest(
                                                devpiExecutable: "venv\\Scripts\\devpi.exe",
                                                url: "https://devpi.library.illinois.edu",
                                                index: "${env.BRANCH_NAME}_staging",
                                                pkgName: "${PKG_NAME}",
                                                pkgVersion: "${PKG_VERSION}",
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

        }
//        stage("Test DevPi packages") {
//            when {
//                allOf{
//                    anyOf{
//                        equals expected: true, actual: params.DEPLOY_DEVPI
//                        triggeredBy "TimerTriggerCause"
//                    }
//                    anyOf {
//                        equals expected: "master", actual: env.BRANCH_NAME
//                        equals expected: "dev", actual: env.BRANCH_NAME
//                    }
//                }
//            }
//
//            parallel {
//                stage("Testing Submitted Source Distribution") {
//                    environment {
//                        PATH = "${tool 'cmake3.12'};${tool 'CPython-3.6'};${tool 'CPython-3.7'};$PATH"
//                    }
//                    steps {
//                        echo "Testing Source tar.gz package in devpi"
//
//                        timeout(20){
//                            devpiTest(
//                                devpiExecutable: "venv36\\Scripts\\devpi.exe",
//                                url: "https://devpi.library.illinois.edu",
//                                index: "${env.BRANCH_NAME}_staging",
//                                pkgName: "${PKG_NAME}",
//                                pkgVersion: "${PKG_VERSION}",
//                                pkgRegex: "tar.gz",
//                                detox: false
//                            )
//                        }
//                        echo "Finished testing Source Distribution: .tar.gz"
//                    }
//                    post {
//                        failure {
//                            echo "Tests for .tar.gz source on DevPi failed."
//                        }
//                    }
//
//                }
//                stage("Built Distribution: py36 .whl") {
//                    agent {
//                        node {
//                            label "Windows && Python3"
//                        }
//                    }
//                    environment {
//                        PATH = "${tool 'CPython-3.6'};$PATH"
//                    }
//                    options {
//                        skipDefaultCheckout(true)
//                    }
//
//                    steps {
//                        bat "${tool 'CPython-3.6'}\\python -m venv venv36"
//                        bat "venv36\\Scripts\\python.exe -m pip install pip --upgrade"
//                        bat "venv36\\Scripts\\pip.exe install devpi --upgrade"
//                        echo "Testing Whl package in devpi"
//                        devpiTest(
//                                devpiExecutable: "venv36\\Scripts\\devpi.exe",
//                                url: "https://devpi.library.illinois.edu",
//                                index: "${env.BRANCH_NAME}_staging",
//                                pkgName: "${PKG_NAME}",
//                                pkgVersion: "${PKG_VERSION}",
//                                pkgRegex: "36.*whl",
//                                detox: false,
//                                toxEnvironment: "py36"
//                            )
//
//                        echo "Finished testing Built Distribution: .whl"
//                    }
//                    post {
//                        failure {
//                            archiveArtifacts allowEmptyArchive: true, artifacts: "**/MSBuild_*.failure.txt"
//                        }
//                        cleanup{
//                            cleanWs(
//                                deleteDirs: true,
//                                disableDeferredWipeout: true,
//                                patterns: [
//                                    [pattern: 'certs', type: 'INCLUDE']
//                                    ]
//                            )
//                        }
//                    }
//                }
//                stage("Built Distribution: py37 .whl") {
//                    agent {
//                        node {
//                            label "Windows && Python3"
//                        }}
//                    environment {
//                        PATH = "${tool 'CPython-3.7'};$PATH"
//                    }
//                    options {
//                        skipDefaultCheckout(true)
//                    }
//
//                    steps {
//                        echo "Testing Whl package in devpi"
//                        bat "\"${tool 'CPython-3.7'}\\python.exe\" -m venv venv37"
//                        bat "venv37\\Scripts\\python.exe -m pip install pip --upgrade"
//                        bat "venv37\\Scripts\\pip.exe install devpi --upgrade"
//                        devpiTest(
//                                devpiExecutable: "venv37\\Scripts\\devpi.exe",
//                                url: "https://devpi.library.illinois.edu",
//                                index: "${env.BRANCH_NAME}_staging",
//                                pkgName: "${PKG_NAME}",
//                                pkgVersion: "${PKG_VERSION}",
//                                pkgRegex: "37.*whl",
//                                detox: false,
//                                toxEnvironment: "py37"
//                            )
//                        echo "Finished testing Built Distribution: .whl"
//                    }
//                    post {
//                        failure {
//                            archiveArtifacts allowEmptyArchive: true, artifacts: "**/MSBuild_*.failure.txt"
//                        }
//                        cleanup{
//                            cleanWs(
//                                deleteDirs: true,
//                                disableDeferredWipeout: true,
//                                patterns: [
//                                    [pattern: 'certs', type: 'INCLUDE']
//                                    ]
//                            )
//                        }
//                    }
//                }
//            }
            post {
                success {
                    echo "it Worked. Pushing file to ${env.BRANCH_NAME} index"
                    script {
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                            bat "venv\\Scripts\\devpi.exe use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                            bat "venv\\Scripts\\devpi.exe push ${PKG_NAME}==${PKG_VERSION} ${DEVPI_USERNAME}/${env.BRANCH_NAME}"
                        }

                    }
                }
                failure {
                    echo "At least one package format on DevPi failed."
                }
            }
        }
        stage("Deploy - SCCM"){
            agent any
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

                stage("Deploy - SCCM upload") {
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
//         stage("Deploy to SCCM") {
//            when {
//                expression { params.RELEASE == "Release_to_devpi_and_sccm"}
//            }
//
//            steps {
//                node("Linux"){
//                    unstash "msi"
//                    deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
//                    input("Push a SCCM release?")
//                    deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
//                }
//
//            }
//            post {
//                success {
//                    script{
//                        def  deployment_request = requestDeploy this, "deployment.yml"
//                        echo deployment_request
//                        writeFile file: "deployment_request.txt", text: deployment_request
//                        archiveArtifacts artifacts: "deployment_request.txt"
//                    }
//                }
//            }
//        }
//        stage("Release to DevPi production") {
//            when {
//            allOf{
//              equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
//              branch "master"
//            }
//          }
//            steps {
//                script {
//                    try{
//                        timeout(30) {
//                            input "Release ${PKG_NAME} ${PKG_VERSION} (https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging/${PKG_NAME}/${PKG_VERSION}) to DevPi Production? "
//                        }
//                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
//                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
//                        }
//
//                        bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
//                        bat "venv\\Scripts\\devpi.exe push ${PKG_NAME}==${PKG_VERSION} production/release"
//                    } catch(err){
//                        echo "User response timed out. Packages not deployed to DevPi Production."
//                    }
//                }
//            }
//        }
        stage("Update online documentation") {
            agent any
            when {
                expression { params.UPDATE_DOCS == true }
            }
            steps {
                dir("build/docs/html/"){
                    bat "dir /s /B"
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
                // updateOnlineDocs stash_name: "HTML Documentation", url_subdomain: params.URL_SUBFOLDER
            }
        }

        // stage("Update online documentation") {
        //     agent any
        //     when {
        //         expression { params.UPDATE_DOCS == true }
        //     }

        //     steps {
        //         updateOnlineDocs url_subdomain: params.URL_SUBFOLDER, stash_name: "HTML Documentation"
        //     }
        // }
    }
    post{
        cleanup{

            script {
                if(fileExists('source/setup.py')){
                    dir("source"){
                        try{
                            retry(3) {
                                bat "${WORKSPACE}\\venv\\Scripts\\python.exe setup.py clean --all"
                            }
                        } catch (Exception ex) {
                            echo "Unable to successfully run clean. Purging source directory."
                            deleteDir()
                        }
                    }
                }
                bat "tree /A"
                if (env.BRANCH_NAME == "master" || env.BRANCH_NAME == "dev"){
                    withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                        bat "venv\\Scripts\\devpi.exe login DS_Jenkins --password ${DEVPI_PASSWORD}"
                        bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
                    }

                    def devpi_remove_return_code = bat returnStatus: true, script:"venv\\Scripts\\devpi.exe remove -y ${PKG_NAME}==${PKG_VERSION}"
                    echo "Devpi remove exited with code ${devpi_remove_return_code}."
                }
            }
            cleanWs(
                deleteDirs: true,
                patterns: [
                    [pattern: 'dist', type: 'INCLUDE'],
                    [pattern: 'build', type: 'INCLUDE'],
                    [pattern: 'reports', type: 'INCLUDE'],
                    [pattern: 'logs', type: 'INCLUDE'],
                    [pattern: 'certs', type: 'INCLUDE'],
                    [pattern: '*tmp', type: 'INCLUDE'],
                    ]
                )
        }
    }
}
