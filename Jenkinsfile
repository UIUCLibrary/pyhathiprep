#!groovy
@Library("ds-utils@v0.1.0") // Uses library from https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*

pipeline {
    agent {
            label "Windows"
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
            string(name: "PROJECT_NAME", defaultValue: "Hathi Validate", description: "Name given to the project")
            booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
            booleanParam(name: "ADDITIONAL_TESTS", defaultValue: true, description: "Run additional tests")
            // booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
            // booleanParam(name: "DEPLOY_SCCM", defaultValue: false, description: "Deploy SCCM")
            booleanParam(name: "DEPLOY_DEVPI", defaultValue: true, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
            booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
            booleanParam(name: "DEPLOY_HATHI_TOOL_BETA", defaultValue: false, description: "Deploy standalone to \\\\storage.library.illinois.edu\\HathiTrust\\Tools\\beta\\")
            booleanParam(name: "DEPLOY_SCCM", defaultValue: false, description: "Request deployment of MSI installer to SCCM")
            booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    //        booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
            string(name: 'URL_SUBFOLDER', defaultValue: "pyhathiprep", description: 'The directory that the docs should be saved under')
        }
//    agent any
//    environment {
//        mypy_args = "--junit-xml=mypy.xml"
//        pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
//    }
//    parameters {
//        string(name: "PROJECT_NAME", defaultValue: "PyHathiPrep", description: "Name given to the project")
//        booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run automated unit tests")
//        booleanParam(name: "ADDITIONAL_TESTS", defaultValue: true, description: "Run additional tests")
//        booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a package")
//        booleanParam(name: "DEPLOY_SCCM", defaultValue: false, description: "Create SCCM deployment package")
//        booleanParam(name: "DEPLOY_DEVPI", defaultValue: true, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
//        booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update online documentation")
//        string(name: 'URL_SUBFOLDER', defaultValue: "pyhathiprep", description: 'The directory that the docs should be saved under')
//    }
    stages {

//        stage("Cloning Source") {
//            agent any
//
//            steps {
//                deleteDir()
//                checkout scm
//                stash includes: '**', name: "Source", useDefaultExcludes: false
//            }
//
//        }
//        stage("Unit tests") {
//            when {
//                expression { params.UNIT_TESTS == true }
//            }
//            steps {
//                parallel(
//                        "Windows": {
//                            script {
//                                def runner = new Tox(this)
//                                runner.env = "pytest"
//                                runner.windows = true
//                                runner.stash = "Source"
//                                runner.label = "Windows"
//                                runner.post = {
//                                    junit 'reports/junit-*.xml'
//                                }
//                                runner.run()
//                            }
//                        }
////                        "Linux": {
////                            script {
////                                def runner = new Tox(this)
////                                runner.env = "pytest"
////                                runner.windows = false
////                                runner.stash = "Source"
////                                runner.label = "!Windows"
////                                runner.post = {
////                                    junit 'reports/junit-*.xml'
////                                }
////                                runner.run()
////                            }
////                        }
//                )
//            }
//        }
//        stage("Additional tests") {
//            when {
//                expression { params.ADDITIONAL_TESTS == true }
//            }
//
//            steps {
//                parallel(
//                    "Documentation": {
//                        node(label: "Windows") {
//                            checkout scm
//                            bat "${tool 'Python3.6.3_Win64'} -m tox -e docs"
//                            script{
//                                // Multibranch jobs add the slash and add the branch to the job name. I need only the job name
//                                def alljob = env.JOB_NAME.tokenize("/") as String[]
//                                def project_name = alljob[0]
//                                dir('.tox/dist') {
//                                    zip archive: true, dir: 'html', glob: '', zipFile: "${project_name}-${env.BRANCH_NAME}-docs-html-${env.GIT_COMMIT.substring(0,6)}.zip"
//                                    dir("html"){
//                                        stash includes: '**', name: "HTML Documentation"
//                                    }
//                                }
//                            }
//                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: '.tox/dist/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
//                        }
//                    },
//                    "MyPy": {
//
//                        node(label: "Windows") {
//                            checkout scm
//                            bat "call make.bat install-dev"
//                            bat "venv\\Scripts\\mypy.exe -p hathizip --junit-xml=junit-${env.NODE_NAME}-mypy.xml --html-report reports/mypy_html"
//                            junit "junit-${env.NODE_NAME}-mypy.xml"
//                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
//                        }
//                    }
//                )
//            }
//        }
        stage("Configure") {
            stages{
                stage("Purge all existing data in workspace"){
                    when{
                        equals expected: true, actual: params.FRESH_WORKSPACE
                    }
                    steps {
                        deleteDir()
                        bat "dir"
                        echo "Cloning source"
                        dir("source"){
                            checkout scm
                        }
                    }
                    post{
                        success {
                            bat "dir /s /B"
                        }
                    }
                }
                stage("Stashing important files for later"){
                    steps{
                       dir("source"){
                            stash includes: 'deployment.yml', name: "Deployment"
                       }
                    }
                }
                stage("Cleanup extra dirs"){
                    steps{
                        dir("reports"){
                            deleteDir()
                            echo "Cleaned out reports directory"
                            bat "dir"
                        }
                        dir("dist"){
                            deleteDir()
                            echo "Cleaned out dist directory"
                            bat "dir"
                        }
                        dir("build"){
                            deleteDir()
                            echo "Cleaned out build directory"
                            bat "dir"
                        }
                    }
                }
                stage("Creating virtualenv for building"){
                    steps{
                        bat "${tool 'CPython-3.6'} -m venv venv"
                        script {
                            try {
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip>=18.0"
                            }
                            catch (exc) {
                                bat "${tool 'CPython-3.6'} -m venv venv"
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip>=18.0 --no-cache-dir"
                            }
                        }
                        bat "venv\\Scripts\\pip.exe install devpi-client --upgrade-strategy only-if-needed"
                        bat "venv\\Scripts\\pip.exe install tox mypy lxml pytest pytest-cov flake8 sphinx wheel --upgrade-strategy only-if-needed"
                        bat "venv\\Scripts\\pip.exe install -r source\\requirements.txt -r source\\requirements-dev.txt -r source\\requirements-freeze.txt --upgrade-strategy only-if-needed"

                        tee("logs/pippackages_venv_${NODE_NAME}.log") {
                            bat "venv\\Scripts\\pip.exe list"
                        }
                    }
                    post{
                        always{
                            dir("logs"){
                                script{
                                    def log_files = findFiles glob: '**/pippackages_venv_*.log'
                                    log_files.each { log_file ->
                                        echo "Found ${log_file}"
                                        archiveArtifacts artifacts: "${log_file}"
                                        bat "del ${log_file}"
                                    }
                                }
                            }
                        }
                        failure {
                            deleteDir()
                        }
                    }
                }
                stage("Setting variables used by the rest of the build"){
                    steps{

                        script {
                            // Set up the reports directory variable
                            REPORT_DIR = "${pwd tmp: true}\\reports"
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
                    post{
                        always{
                            bat "dir /s / B"
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
            }
            post {
                success{
                    tee("logs/workspace_files_${NODE_NAME}.log") {
                        bat "dir /s /B"
                    }
                }
            }
        }
        stage("Build"){
            stages{
                stage("Python Package"){
                    steps {
                        tee("logs/build.log") {
                            dir("source"){
                                bat "${WORKSPACE}\\venv\\Scripts\\python.exe setup.py build -b ${WORKSPACE}\\build"
                            }

                        }
                    }
                }
                stage("Docs"){
                    steps{
                        echo "Building docs on ${env.NODE_NAME}"
                        tee("logs/build_sphinx.log") {
                            dir("build/lib"){
                                bat "${WORKSPACE}\\venv\\Scripts\\sphinx-build.exe -b html ${WORKSPACE}\\source\\docs\\source ${WORKSPACE}\\build\\docs\\html -d ${WORKSPACE}\\build\\docs\\doctrees"
                            }
                        }
                    }
                    post{
                        always {
                            dir("logs"){
                                script{
                                    def log_files = findFiles glob: '**/*.log'
                                    log_files.each { log_file ->
                                        echo "Found ${log_file}"
                                        archiveArtifacts artifacts: "${log_file}"
                                        bat "del ${log_file}"
                                    }
                                }
                            }
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            dir("${WORKSPACE}/dist"){
                                zip archive: true, dir: "${WORKSPACE}/build/docs/html", glob: '', zipFile: "${DOC_ZIP_FILENAME}"
                            }
                        }
                    }
                }
            }
        }
        stage("Tests") {

            parallel {
                stage("PyTest"){
                    when {
                        equals expected: true, actual: params.UNIT_TESTS
                    }
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\pytest.exe --junitxml=${WORKSPACE}/reports/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest --cov-report html:${WORKSPACE}/reports/coverage/ --cov=pyhathiprep" //  --basetemp={envtmpdir}"
                        }

                    }
                    post {
                        always{
                            junit "reports/junit-${env.NODE_NAME}-pytest.xml"
                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/coverage', reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                        }
                    }
                }
                stage("MyPy"){
                    when{
                        equals expected: true, actual: params.ADDITIONAL_TESTS
                    }
                    steps{
                        dir("source") {
                            bat "${WORKSPACE}\\venv\\Scripts\\mypy.exe -p pyhathiprep --junit-xml=${WORKSPACE}/junit-${env.NODE_NAME}-mypy.xml --html-report ${WORKSPACE}/reports/mypy_html"
                        }
                    }
                    post{
                        always {
                            junit "junit-${env.NODE_NAME}-mypy.xml"
                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                        }
                    }
                }
                stage("Documentation"){
                    when{
                        equals expected: true, actual: params.ADDITIONAL_TESTS
                    }
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\sphinx-build.exe -b doctest docs\\source ${WORKSPACE}\\build\\docs -d ${WORKSPACE}\\build\\docs\\doctrees -v"
                        }
                    }

                }
            }
        }
        // stage("Additional tests") {
        //     when {
        //         expression { params.ADDITIONAL_TESTS == true }
        //     }

        //     steps {
        //         parallel(
        //                 "Documentation": {
        //                     script {
        //                         def runner = new Tox(this)
        //                         runner.env = "docs"
        //                         runner.windows = false
        //                         runner.stash = "Source"
        //                         runner.label = "Linux"
        //                         runner.post = {
        //                             dir('.tox/dist/html/') {
        //                                 stash includes: '**', name: "HTML Documentation", useDefaultExcludes: false
        //                             }
        //                         }
        //                         runner.run()

        //                     }
        //                 },
        //                 "MyPy": {
        //                     script {
        //                         def runner = new Tox(this)
        //                         runner.env = "mypy"
        //                         runner.windows = false
        //                         runner.stash = "Source"
        //                         runner.label = "Linux"
        //                         runner.post = {
        //                             junit 'mypy.xml'
        //                         }
        //                         runner.run()

        //                     }
        //                 }
        //         )
        //     }
        // }

//        stage("Packaging") {
//            when {
//                expression { params.PACKAGE == true || params.DEPLOY_SCCM == true }
//            }
//
//            steps {
//                parallel(
//                        "Source Release": {
//                            createSourceRelease(env.PYTHON3, "Source")
//                        },
//                        "Windows Wheel": {
//                            node(label: "Windows") {
//                                deleteDir()
//                                unstash "Source"
//                                bat "${tool 'Python3.6.3_Win64'} setup.py bdist_wheel --universal"
//                                archiveArtifacts artifacts: "dist/**", fingerprint: true
//                            }
//                        },
//                        "Windows CX_Freeze MSI": {
//                            node(label: "Windows") {
//                                deleteDir()
//                                unstash "Source"
//                                bat """${tool 'Python3.6.3_Win64'} -m venv .env
//                                       call .env/Scripts/activate.bat
//                                       pip install -r requirements.txt
//                                       pip install ruamel.base
//                                       python cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir build/msi
//                                       call .env/Scripts/deactivate.bat
//                                    """
//                                bat "build\\msi\\pyhathiprep.exe --pytest"
//                                dir("dist") {
//                                    stash includes: "*.msi", name: "msi"
//                                }
//
//                            }
//                            node(label: "Windows") {
//                                deleteDir()
//                                git url: 'https://github.com/UIUCLibrary/ValidateMSI.git'
//                                unstash "msi"
//                                bat "call validate.bat -i"
//                                archiveArtifacts artifacts: "*.msi", fingerprint: true
//                            }
//                        },
//                )
//            }
//        }
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
                    steps{
                        dir("source"){
//                            bat "venv\\Scripts\\pip.exe install -r requirements.txt -r requirements-dev.txt -r requirements-freeze.txt"
                            bat "${WORKSPACE}\\venv\\Scripts\\python cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir ${WORKSPACE}/build/msi --dist-dir ${WORKSPACE}/dist"
                        }
                        bat "build\\msi\\hathivalidate.exe --pytest"
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
                            dir("build/msi") {
                                deleteDir()
                            }
                        }
                    }
                }
            }
        }
        stage("Deploy - Staging") {
            agent {
                label 'Linux'
            }
            when {
                expression { params.DEPLOY_SCCM == true }
            }

            steps {
                deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                input("Deploy to production?")
            }
        }

        stage("Deploy - SCCM upload") {
            agent {
                label 'Linux'
            }
            when {
                expression { params.DEPLOY_SCCM == true }
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
            agent {
                node {
                    label 'Windows&&DevPi'
                }
            }
            when {
                expression { params.DEPLOY_DEVPI == true }
            }
            steps {
                deleteDir()
                unstash "Source"
                bat "devpi use http://devpy.library.illinois.edu"
                withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {

                    bat "devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                    bat "devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}"
                    script {
                        try{
                            bat "devpi upload --with-docs"

                        } catch (exc) {
                            echo "Unable to upload to devpi with docs. Trying without"
                            bat "devpi upload"
                        }
                    }
                    bat "devpi test pyhathiprep"
                }

            }
        }

        stage("Update online documentation") {
            agent {
                label 'Linux'

            }
            when {
              expression {params.UPDATE_DOCS == true }
            }

            steps {
                updateOnlineDocs url_subdomain: params.URL_SUBFOLDER, stash_name: "HTML Documentation"
            }
        }
    }
}
