#!groovy
@Library("ds-utils@v0.1.0") // Uses library from https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*

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

    // environment {
        //mypy_args = "--junit-xml=mypy.xml"
        //pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    // }
    parameters {
        booleanParam(name: "FRESH_WORKSPACE", defaultValue: false, description: "Purge workspace before staring and checking out source")
        booleanParam(name: "BUILD_DOCS", defaultValue: true, description: "Build documentation")
        booleanParam(name: "TEST_RUN_DOCTEST", defaultValue: true, description: "Test documentation")
//        booleanParam(name: "TEST_RUN_FLAKE8", defaultValue: true, description: "Run Flake8 static analysis")
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
                stage("Cleanup"){
                    steps {


                        dir("logs"){
                            deleteDir()
                            echo "Cleaned out logs directory"
                            bat "dir"
                        }

                        dir("build"){
                            deleteDir()
                            echo "Cleaned out build directory"
                            bat "dir"
                        }
                        dir("dist"){
                            deleteDir()
                            echo "Cleaned out dist directory"
                            bat "dir"
                        }

                        dir("reports"){
                            deleteDir()
                            echo "Cleaned out reports directory"
                            bat "dir"
                        }
                    }
                    post{
                        failure {
                            deleteDir()
                        }
                    }
                }
                stage("Installing required system level dependencies"){
                    steps{
                        lock("system_python_${NODE_NAME}"){
                            bat "${tool 'CPython-3.6'} -m pip install --upgrade pip --quiet"
                        }
                    }
                    post{
                        always{
                            lock("system_python_${NODE_NAME}"){
                                bat "${tool 'CPython-3.6'} -m pip list > logs\\pippackages_system_${NODE_NAME}.log"
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
                        bat "${tool 'CPython-3.6'} -m venv venv"
                        script {
                            try {
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip"
                            }
                            catch (exc) {
                                bat "${tool 'CPython-3.6'} -m venv venv"
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip --no-cache-dir"
                            }
                        }
                        bat "venv\\Scripts\\pip.exe install devpi-client -r source\\requirements.txt -r source\\requirements-dev.txt -r source\\requirements-freeze.txt --upgrade-strategy only-if-needed"
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
                                PKG_NAME = bat(returnStdout: true, script: "@${tool 'CPython-3.6'}  setup.py --name").trim()
                                PKG_VERSION = bat(returnStdout: true, script: "@${tool 'CPython-3.6'} setup.py --version").trim()
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
                            warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'Pep8', pattern: 'logs/build.log']]
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
                            warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'Pep8', pattern: 'logs/build_sphinx.log']]
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            zip archive: true, dir: "build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                            stash includes: 'build/docs/html/**', name: 'docs'
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
                            bat "${WORKSPACE}\\venv\\Scripts\\pytest.exe --junitxml=${WORKSPACE}/reports/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest --cov-report html:${WORKSPACE}/reports/coverage/ --cov=pyhathiprep" //  --basetemp={envtmpdir}"
                        }

                    }
                    post {
                        always{
                            dir("reports"){
                                script{
                                    def report_files = findFiles glob: '**/*.pytest.xml'
                                    report_files.each { report_file ->
                                        echo "Found ${report_file}"
                                        // archiveArtifacts artifacts: "${log_file}"
                                        junit "${report_file}"
                                        bat "del ${report_file}"
                                    }
                                }
                            }
                            // junit "reports/junit-${env.NODE_NAME}-pytest.xml"
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/coverage', reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                        }
                    }
                }
                stage("Documentation"){
                    when{
                        equals expected: true, actual: params.TEST_RUN_DOCTEST
                    }
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\sphinx-build.exe -b doctest docs\\source ${WORKSPACE}\\build\\docs -d ${WORKSPACE}\\build\\docs\\doctrees -v"
                        }
                    }

                }
                stage("MyPy"){
                    when{
                        equals expected: true, actual: params.TEST_RUN_MYPY
                    }
                    steps{
                        dir("source") {
                            bat "${WORKSPACE}\\venv\\Scripts\\mypy.exe -p pyhathiprep --junit-xml=${WORKSPACE}/junit-${env.NODE_NAME}-mypy.xml --html-report ${WORKSPACE}/reports/mypy_html"
                        }
                    }
                    post{
                        always {
                            junit "junit-${env.NODE_NAME}-mypy.xml"
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                        }
                    }
                }
            }
        }
        stage("Packaging") {
            when {
                expression { params.DEPLOY_DEVPI == true || params.RELEASE != "None"}
            }
            parallel {
                stage("Source and Wheel formats"){
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\scripts\\python.exe setup.py sdist -d ${WORKSPACE}\\dist bdist_wheel -d ${WORKSPACE}\\dist"
                        }

                    }
                    post{
                        success{
                            dir("dist"){
                                archiveArtifacts artifacts: "*.whl", fingerprint: true
                                archiveArtifacts artifacts: "*.tar.gz", fingerprint: true
                            }
                        }
                    }
                }
                stage("Windows CX_Freeze MSI"){
                    agent{
                        node {
                            label "Windows"
                        }
                    }
                    options {
                        skipDefaultCheckout true
                    }
                    steps{
                        bat "dir"
                        deleteDir()
                        bat "dir"
                        checkout scm
                        bat "dir /s / B"
                        bat "${tool 'CPython-3.6'} -m venv venv"
                        bat "venv\\Scripts\\python.exe -m pip install -U pip>=18.0"
                        bat "venv\\Scripts\\pip.exe install -U setuptools"
                        bat "venv\\Scripts\\pip.exe install -r requirements.txt -r requirements-dev.txt -r requirements-freeze.txt"
                        bat "venv\\Scripts\\python.exe cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir build/msi"
                        // bat "make freeze"


                    }
                    post{
                        success{
                            dir("dist") {
                                stash includes: "*.msi", name: "msi"
                                archiveArtifacts artifacts: "*.msi", fingerprint: true
                            }
                        }
                        cleanup{
                            bat "dir"
                            deleteDir()
                            bat "dir"
                        }
                    }
                }
//                stage("Windows CX_Freeze MSI"){
//                    steps{
//                        dir("source"){
////                            bat "venv\\Scripts\\pip.exe install -r requirements.txt -r requirements-dev.txt -r requirements-freeze.txt"
//                            bat "${WORKSPACE}\\venv\\Scripts\\python cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir ${WORKSPACE}/build/msi --dist-dir ${WORKSPACE}/dist"
//                        }
//                        bat "build\\msi\\hathivalidate.exe --pytest"
//                        // bat "make freeze"
//
//
//                    }
//                    post{
//                        success{
//                            dir("dist") {
//                                stash includes: "*.msi", name: "msi"
//                                archiveArtifacts artifacts: "*.msi", fingerprint: true
//                            }
//                        }
//                        cleanup{
//                            dir("build/msi") {
//                                deleteDir()
//                            }
//                        }
//                    }
//                }
            }
        }
        stage("Deploy - Staging") {
            agent any
            when {
                expression { params.DEPLOY_SCCM == true && params.PACKAGE == true }
            }

            steps {
                deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                input("Deploy to production?")
            }
        }

        stage("Deploy - SCCM upload") {
            agent any
            when {
                expression { params.DEPLOY_SCCM == true && params.PACKAGE == true }
            }

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
        stage("Deploying to Devpi") {
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
            }
            steps {
                bat "venv\\Scripts\\devpi.exe use http://devpy.library.illinois.edu"
                withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                    bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                    bat "venv\\Scripts\\devpi.exe use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                    script {
                        bat "venv\\Scripts\\devpi.exe upload --from-dir dist"
                        try {
//                            bat "venv\\Scripts\\devpi.exe upload --only-docs"
                            bat "venv\\Scripts\\devpi.exe upload --only-docs ${WORKSPACE}\\dist\\${DOC_ZIP_FILENAME}"
                        } catch (exc) {
                            echo "Unable to upload to devpi with docs."
                        }
                    }
                }

            }
        }
        stage("Test Devpi packages") {
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
            }
//            steps {
            parallel {
                stage("Source Distribution: .tar.gz") {
                    steps {
                        echo "Testing Source tar.gz package in devpi"
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"

                        }
                        bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"

                        script {
                            def devpi_test_return_code = bat returnStatus: true, script: "venv\\Scripts\\devpi.exe test --index https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging ${PKG_NAME} -s tar.gz  --verbose"
                            if(devpi_test_return_code != 0){
                                error "Devpi exit code for tar.gz was ${devpi_test_return_code}"
                            }
                        }
                        echo "Finished testing Source Distribution: .tar.gz"
                    }
                    post {
                        failure {
                            echo "Tests for .tar.gz source on DevPi failed."
                        }
                    }

                }
                stage("Source Distribution: .zip") {
                    steps {
                        echo "Testing Source zip package in devpi"
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                        }
                        bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
                        script {
                            def devpi_test_return_code = bat returnStatus: true, script: "venv\\Scripts\\devpi.exe test --index https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging ${PKG_NAME} -s zip --verbose"
                            if(devpi_test_return_code != 0){
                                error "Devpi exit code for zip was ${devpi_test_return_code}"
                            }
                        }
                        echo "Finished testing Source Distribution: .zip"
                    }
                    post {
                        failure {
                            echo "Tests for .zip source on DevPi failed."
                        }
                    }
                }
                stage("Built Distribution: .whl") {
                    agent {
                        node {
                            label "Windows && Python3"
                        }
                    }
                    options {
                        skipDefaultCheckout()
                    }
                    steps {
                        echo "Testing Whl package in devpi"
                        bat "${tool 'CPython-3.6'} -m venv venv"
                        bat "venv\\Scripts\\pip.exe install tox devpi-client"
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                        }
                        bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
                        script{
                            def devpi_test_return_code = bat returnStatus: true, script: "venv\\Scripts\\devpi.exe test --index https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging ${PKG_NAME} -s whl  --verbose"
                            if(devpi_test_return_code != 0){
                                error "Devpi exit code for whl was ${devpi_test_return_code}"
                            }
                        }
                        echo "Finished testing Built Distribution: .whl"
                    }
                    post {
                        failure {
                            echo "Tests for whl on DevPi failed."
                        }
                    }
                }
            }

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
            }
        }
         stage("Deploy to SCCM") {
            when {
                expression { params.RELEASE == "Release_to_devpi_and_sccm"}
            }

            steps {
                node("Linux"){
                    unstash "msi"
                    deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                    input("Push a SCCM release?")
                    deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
                }

            }
            post {
                success {
                    script{
                        def  deployment_request = requestDeploy this, "deployment.yml"
                        echo deployment_request
                        writeFile file: "deployment_request.txt", text: deployment_request
                        archiveArtifacts artifacts: "deployment_request.txt"
                    }
                }
            }
        }
        stage("Release to DevPi production") {
            when {
                expression { params.RELEASE != "None" && env.BRANCH_NAME == "master" }
            }
            steps {
                script {
                    try{
                        timeout(30) {
                            input "Release ${PKG_NAME} ${PKG_VERSION} (https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging/${PKG_NAME}/${PKG_VERSION}) to DevPi Production? "
                        }
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                        }

                        bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
                        bat "venv\\Scripts\\devpi.exe push ${PKG_NAME}==${PKG_VERSION} production/release"
                    } catch(err){
                        echo "User response timed out. Packages not deployed to DevPi Production."
                    }
                }
            }
        }
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
//            bat "dir /s / B"
        }
    }
//        stage("Deploy - Staging") {
//            agent {
//                label 'Linux'
//            }
//            when {
//                expression { params.DEPLOY_SCCM == true }
//            }
//
//            steps {
//                deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
//                input("Deploy to production?")
//            }
//        }
//
//        stage("Deploy - SCCM upload") {
//            agent {
//                label 'Linux'
//            }
//            when {
//                expression { params.DEPLOY_SCCM == true }
//            }
//
//            steps {
//                deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
//            }
//            post {
//                success {
//                    script{
//                        unstash "Source"
//                        def  deployment_request = requestDeploy this, "deployment.yml"
//                        echo deployment_request
//                        writeFile file: "deployment_request.txt", text: deployment_request
//                        archiveArtifacts artifacts: "deployment_request.txt"
//                    }
//                }
//            }
//        }
//        stage("Deploying to Devpi") {
//            agent {
//                node {
//                    label 'Windows&&DevPi'
//                }
//            }
//            when {
//                expression { params.DEPLOY_DEVPI == true }
//            }
//            steps {
//                deleteDir()
//                unstash "Source"
//                bat "devpi use http://devpy.library.illinois.edu"
//                withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
//
//                    bat "devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
//                    bat "devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}"
//                    script {
//                        try{
//                            bat "devpi upload --with-docs"
//
//                        } catch (exc) {
//                            echo "Unable to upload to devpi with docs. Trying without"
//                            bat "devpi upload"
//                        }
//                    }
//                    bat "devpi test pyhathiprep"
//                }
//
//            }
//        }
//
//        stage("Update online documentation") {
//            agent {
//                label 'Linux'
//
//            }
//            when {
//              expression {params.UPDATE_DOCS == true }
//            }
//
//            steps {
//                updateOnlineDocs url_subdomain: params.URL_SUBFOLDER, stash_name: "HTML Documentation"
//            }
//        }
//    }
}
