#!groovy
@Library("ds-utils@v0.1.0") // Uses library from https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*
@Library(["devpi", "PythonHelpers"]) _

SONARQUBE_CREDENTIAL_ID = "sonartoken-pyhathiprep"

// CONFIGURATIONS = [
//     '3.6': [
//         test_docker_image: "python:3.6-windowsservercore",
//         tox_env: "py36"
//         ],
//     "3.7": [
//         test_docker_image: "python:3.7",
//         tox_env: "py37"
//         ]
// ]

defaultParameterValues = [
    USE_SONARQUBE: false
]


def CONFIGURATIONS = [
    "3.6" : [
        os: [
            windows:[
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                            label: 'Windows&&Docker',
                            additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6'
                        ]
                    ],
                    test:[
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6',
                                baseImage: "python:3.6-windowsservercore"
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/msvc/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6'
                            ]
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*cp36*.whl",
                    sdist: "*.zip"
                ]
            ],
            linux: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    devpi: [
                        whl: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*cp36*.whl",
                    sdist: "*.zip"
                ]
            ]
        ],
        tox_env: "py36",
        devpiSelector: [
            sdist: "zip",
            wheel: "36.*whl",
        ],
        pkgRegex: [
            wheel: "*cp36*.whl",
            sdist: "*.zip"
        ]
    ],
    "3.7" : [
        os: [
            windows: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/windows/build/msvc/Dockerfile',
                            label: 'Windows&&Docker',
                            additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/msvc/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/test/msvc/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*cp37*.whl",
                    sdist: "*.zip"
                ]
            ],
            linux: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*cp37*.whl",
                    sdist: "*.zip"
                ]
            ]
        ],
        tox_env: "py37",
        devpiSelector: [
            sdist: "zip",
            wheel: "37.*whl",
        ],
        pkgRegex: [
            wheel: "*cp37*.whl",
            sdist: "*.zip"
        ]
    ],
    "3.8" : [
        os: [
            windows: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/windows/build/msvc/Dockerfile',
                            label: 'Windows&&Docker',
                            additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/msvc/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/test/msvc/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ]
                    ]

                ],
                pkgRegex: [
                    wheel: "*cp38*.whl",
                    sdist: "*.zip"
                ]
            ],
            linux: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*cp38*.whl",
                    sdist: "*.zip"
                ]
            ]
        ],
        tox_env: "py38",
        devpiSelector: [
            sdist: "zip",
            wheel: "38.*whl",
        ],
        pkgRegex: [
            wheel: "*cp38*.whl",
            sdist: "*.zip"
        ]
    ],
]


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
def startup(){
    def SONARQUBE_CREDENTIAL_ID = SONARQUBE_CREDENTIAL_ID
    parallel(
        [
            failFast: true,
            "Checking sonarqube Settings": {
                node(){
                    try{
                        withCredentials([string(credentialsId: SONARQUBE_CREDENTIAL_ID, variable: 'dddd')]) {
                            echo 'Found credentials for sonarqube'
                        }
                        defaultParameterValues.USE_SONARQUBE = true
                    } catch(e){
                        echo "Setting defaultValue for USE_SONARQUBE to false. Reason: ${e}"
                        defaultParameterValues.USE_SONARQUBE = false
                    }
                }
            },
            "Getting Distribution Info": {
                node('linux && docker') {
                    timeout(2){
                        ws{
                            checkout scm
                            try{
                                docker.image('python:3.8').inside {
                                    sh(
                                       label: "Running setup.py with dist_info",
                                       script: """python --version
                                                  python setup.py dist_info
                                               """
                                    )
                                    stash includes: "*.dist-info/**", name: 'DIST-INFO'
                                    archiveArtifacts artifacts: "*.dist-info/**"
                                }
                            } finally{
                                deleteDir()
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
        node(){
            unstash 'DIST-INFO'
            def metadataFile = findFiles( glob: '*.dist-info/METADATA')[0]
            def metadata = readProperties(interpolate: true, file: metadataFile.path )
            echo """Version = ${metadata.Version}
Name = ${metadata.Name}
"""
            return metadata
        }
    }
}


startup()
def props = get_props()


pipeline {
    agent none
    
    environment {
        DEVPI = credentials("DS_devpi")
    }
    parameters {
        booleanParam(name: "RUN_CHECKS", defaultValue: true, description: "Run checks on code")
        booleanParam(name: 'USE_SONARQUBE', defaultValue: true, description: 'Send data test data to SonarQube')
        booleanParam(name: "TEST_RUN_TOX", defaultValue: false, description: "Run Tox Tests")
        booleanParam(name: "BUILD_PACKAGES", defaultValue: false, description: "Build Python packages")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        string(name: 'URL_SUBFOLDER', defaultValue: "pyhathiprep", description: 'The directory that the docs should be saved under')
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
        booleanParam(name: "DEPLOY_ADD_TAG", defaultValue: false, description: "Tag commit to current version")
    }
    stages {
        stage("Building") {
            agent {
                dockerfile {
                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                    label "linux && docker"
                    additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                }
            }
            stages{
                stage("Building Python Package"){
                    steps {
                        timeout(5){
                            sh(label: "Building Python package",
                                script: """ mkdir -p logs
                                python setup.py build -b build  | tee logs/build.log
                                """
                                )
                        }
                    }
                }
                stage("Building Sphinx Documentation"){
                    environment{
                        PKG_NAME = get_package_name("DIST-INFO", "pyhathiprep.dist-info/METADATA")
                        PKG_VERSION = get_package_version("DIST-INFO", "pyhathiprep.dist-info/METADATA")
                    }
                    steps {
                        timeout(5){
                            sh(label:"Building docs on ${env.NODE_NAME}",
                               script: """mkdir -p logs
                                       python -m sphinx docs/source build/docs/html -d build/docs/.doctrees -v -w logs/build_sphinx.log
                                       """
                               )
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
                                def DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
                                zip archive: true, dir: "build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                                stash includes: "dist/${DOC_ZIP_FILENAME},build/docs/html/**", name: 'DOCS_ARCHIVE'
                            }
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
        stage("Checks"){
            when{
                equals expected: true, actual: params.RUN_CHECKS
            }
            stages{
                stage("Code Quality"){
                    stages{
                        stage("Testing"){
                            agent {
                                dockerfile {
                                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                                    label "linux && docker"
                                    additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                }
                            }
                            stages{
                                stage("Run Tests"){
                                    parallel {
                                        stage("PyTest"){
                                            steps{
                                                catchError(buildResult: 'UNSTABLE', message: 'Pytest tests failed', stageResult: 'UNSTABLE') {
                                                    sh(label:"Running pytest",
                                                       script: """mkdir -p reports/pytest/
                                                                  coverage run --parallel-mode --source=pyhathiprep -m pytest --junitxml=reports/pytest/junit-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest
                                                               """
                                                    )
                                                }
                                            }
                                            post{
                                                always{
                                                    stash includes: 'reports/pytest/*.xml', name: 'PYTEST_UNIT_TEST_RESULTS'
                                                    junit 'reports/pytest/junit-pytest.xml'
                                                }
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
                                        stage("Documentation"){
                                            steps{
                                                sh "coverage run --parallel-mode --source=pyhathiprep setup.py build_sphinx --source-dir=docs/source --build-dir=build/docs --builder=doctest"
                                            }
                                        }
                                        stage("MyPy"){
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                    sh (label: "Running MyPy",
                                                        script: """mkdir -p reports/mypy
                                                                   mkdir -p logs
                                                                   mypy -p pyhathiprep --html-report reports/mypy/mypy_html > logs/mypy.log"""
                                                        )
                                                }
                                            }
                                            post{
                                                always {
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
                                        stage("Run Pylint Static Analysis") {
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                                    sh(label: "Running pylint",
                                                        script: '''pylint pyhathiprep -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt
                                                                   '''

                                                    )
                                                }
                                                sh(
                                                    script: 'pylint pyhathiprep -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee reports/pylint_issues.txt',
                                                    label: "Running pylint for sonarqube",
                                                    returnStatus: true
                                                )
                                            }
                                            post{
                                                always{
                                                    recordIssues(tools: [pyLint(pattern: 'reports/pylint.txt')])
                                                    stash includes: "reports/pylint_issues.txt,reports/pylint.txt", name: 'PYLINT_REPORT'
                                                }
                                            }
                                        }
                                        stage("Run Flake8 Static Analysis") {
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'Flake8 found issues', stageResult: 'UNSTABLE') {
                                                    sh(label: "Running flake8",
                                                       script: """mkdir -p logs
                                                                  flake8 pyhathiprep --tee --output-file=logs/flake8.log
                                                                  """
                                                     )
                                                }
                                            }
                                            post {
                                                always {
                                                    stash includes: 'logs/flake8.log', name: 'FLAKE8_REPORT'
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
                                            sh(label: "Combining Coverage data",
                                               script: """coverage combine
                                                          coverage xml -o reports/coverage.xml
                                                          coverage html -d reports/coverage
                                                       """
                                            )
                                            stash(includes: 'reports/coverage*.xml', name: 'COVERAGE_REPORT_DATA')
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
                        stage('Run Sonarqube Analysis'){
                            options{
                                lock('pyhathiprep-sonarscanner')
                            }
                            when{
                                equals expected: true, actual: params.USE_SONARQUBE
                                beforeAgent true
                                beforeOptions true
                            }
                            steps{
                                script{
                                    def sonarqube
                                    node(){
                                        checkout scm
                                        sonarqube = load('ci/jenkins/scripts/sonarqube.groovy')
                                    }
                                    def stashes = [
                                        'COVERAGE_REPORT_DATA',
                                        'PYTEST_UNIT_TEST_RESULTS',
                                        'PYLINT_REPORT',
                                        'FLAKE8_REPORT'
                                    ]
                                    def sonarqubeConfig = [
                                        installationName: 'sonarcloud',
                                        credentialsId: SONARQUBE_CREDENTIAL_ID,
                                    ]
                                    def agent = [
                                            dockerfile: [
                                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                                label: 'linux && docker',
                                                additionalBuildArgs: '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                args: '--mount source=sonar-cache-hathiprep,target=/home/user/.sonar/cache',
                                            ]
                                        ]
                                    if (env.CHANGE_ID){
                                        sonarqube.submitToSonarcloud(
                                            agent: agent,
                                            reportStashes: stashes,
                                            artifactStash: 'sonarqube artifacts',
                                            sonarqube: sonarqubeConfig,
                                            pullRequest: [
                                                source: env.CHANGE_ID,
                                                destination: env.BRANCH_NAME,
                                            ],
                                            package: [
                                                version: props.Version,
                                                name: props.Name
                                            ],
                                        )
                                    } else {
                                        sonarqube.submitToSonarcloud(
                                            agent: agent,
                                            reportStashes: stashes,
                                            artifactStash: 'sonarqube artifacts',
                                            sonarqube: sonarqubeConfig,
                                            package: [
                                                version: props.Version,
                                                name: props.Name
                                            ]
                                        )
                                    }
                                }
                            }
                            post {
                                always{
                                    node(''){
                                        unstash 'sonarqube artifacts'
                                        recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
                                    }
                                }
                            }
                        }
                    }
                }
                stage("Run Tox Test") {
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                     steps {
                        script{
                            def tox
                            node(){
                                checkout scm
                                tox = load("ci/jenkins/scripts/tox.groovy")
                            }
                            def windowsJobs = [:]
                            def linuxJobs = [:]
                            stage("Scanning Tox Environments"){
                                parallel(
                                    "Linux":{
                                        linuxJobs = tox.getToxTestsParallel(
                                                envNamePrefix: "Tox Linux",
                                                label: "linux && docker",
                                                dockerfile: "ci/docker/python/linux/tox/Dockerfile",
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                            )
                                    },
                                    "Windows":{
//                                         windowsJobs = tox.getToxTestsParallel(
//                                                 envNamePrefix: "Tox Windows",
//                                                 label: 'windows && docker',
//                                                 dockerfile: "ci/docker/python/windows/tox/Dockerfile",
//                                                 dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
//                                             )
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
        stage("Packaging") {
            when{
                anyOf{
                    equals expected: true, actual: params.BUILD_PACKAGES
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                }
                beforeAgent true
            }
            stages{
                stage("Building"){
                    parallel{
                        stage("Building Source and Wheel formats"){
                            agent {
                                dockerfile {
                                    filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                                    label 'linux&&docker'
                                    additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                  }
                            }
                            steps{
                                timeout(5){
                                    sh "python -m pep517.build ."
                                }
                            }
                            post{
                                success{
                                    archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.g,dist/*.zip", fingerprint: true
                                }
                                always{
                                    stash includes: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', name: "PYTHON_PACKAGES"
                                }
                                cleanup{
                                    cleanWs deleteDirs: true, patterns: [[pattern: 'dist/*.whl,dist/*.zip', type: 'INCLUDE']]
                                }
                            }
                        }
                        stage("Windows CX_Freeze MSI"){
                            agent {
                                dockerfile {
                                    filename 'ci/docker/python/windows/jenkins/Dockerfile'
                                    label "windows && docker"
                                }
                            }
                            steps{
                                timeout(5){
                                    bat "python cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir ${WORKSPACE}/build/msi -d ${WORKSPACE}/dist"
                                }
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
                stage('Testing all Package') {
                    matrix{
                        agent none
                        axes{
                            axis {
                                name "PLATFORM"
                                values(
                                    "windows",
                                    "linux"
                                )
                            }
                            axis {
                                name "PYTHON_VERSION"
                                values(
                                    "3.7",
                                    "3.8"
                                )
                            }
                        }
                        stages{
                            stage("Testing Wheel Package"){
                                agent {
                                    dockerfile {
                                        filename "ci/docker/python/${PLATFORM}/jenkins/Dockerfile"
                                        label "${PLATFORM} && docker"
                                        additionalBuildArgs "--build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg PIP_INDEX_URL --build-arg PIP_EXTRA_INDEX_URL"
                                    }
                                }
                                steps{
                                    unstash "PYTHON_PACKAGES"
                                    script{
                                        findFiles(glob: "**/*.whl").each{
                                            cleanWs(
                                                deleteDirs: true,
                                                disableDeferredWipeout: true,
                                                patterns: [
                                                    [pattern: '.git/', type: 'EXCLUDE'],
                                                    [pattern: 'tests/', type: 'EXCLUDE'],
                                                    [pattern: 'dist/', type: 'EXCLUDE'],
                                                    [pattern: 'tox.ini', type: 'EXCLUDE']
                                                ]
                                            )
                                            timeout(15){
                                                if(isUnix()){
                                                    sh(label: "Testing ${it}",
                                                        script: """python --version
                                                                   tox --installpkg=${it.path} -e py -vv
                                                                   """
                                                    )
                                                } else {
                                                    bat(label: "Testing ${it}",
                                                        script: """python --version
                                                                   tox --installpkg=${it.path} -e py -vv
                                                                   """
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }
                                post{
                                    cleanup{
                                        cleanWs(
                                            notFailBuild: true,
                                            deleteDirs: true,
                                            patterns: [
                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                [pattern: '**/__pycache__', type: 'INCLUDE'],
                                                [pattern: 'build/', type: 'INCLUDE'],
                                                [pattern: '.tox/', type: 'INCLUDE'],
                                                ]
                                        )
                                    }
                                }
                            }
                            stage("Testing sdist Package"){
                                agent {
                                    dockerfile {
                                        filename "ci/docker/python/${PLATFORM}/jenkins/Dockerfile"
                                        label "${PLATFORM} && docker"
                                        additionalBuildArgs "--build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg PIP_INDEX_URL --build-arg PIP_EXTRA_INDEX_URL"
                                    }
                                }
                                steps{
                                    unstash "PYTHON_PACKAGES"
                                    script{
                                        findFiles(glob: "dist/*.tar.gz,dist/*.zip").each{
                                            cleanWs(
                                                deleteDirs: true,
                                                disableDeferredWipeout: true,
                                                patterns: [
                                                    [pattern: '.git/', type: 'EXCLUDE'],
                                                    [pattern: 'tests/', type: 'EXCLUDE'],
                                                    [pattern: 'dist/', type: 'EXCLUDE'],
                                                    [pattern: 'tox.ini', type: 'EXCLUDE']
                                                ]
                                            )
                                            timeout(15){
                                                if(isUnix()){
                                                    sh(label: "Testing ${it}",
                                                        script: """python --version
                                                                   tox --installpkg=${it.path} -e py -vv
                                                                   """
                                                    )
                                                } else {
                                                    bat(label: "Testing ${it}",
                                                        script: """python --version
                                                                   tox --installpkg=${it.path} -e py -vv
                                                                   """
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }
                                post{
                                    cleanup{
                                        cleanWs(
                                            notFailBuild: true,
                                            deleteDirs: true,
                                            patterns: [
                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                [pattern: 'build/', type: 'INCLUDE'],
                                                [pattern: '**/__pycache__', type: 'INCLUDE'],
                                                [pattern: '.tox/', type: 'INCLUDE'],
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
        stage("Deploy to Devpi"){
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
                beforeAgent true
            }
            agent none
            environment{
                DEVPI = credentials("DS_devpi")
            }
            options{
                lock("pyhathiprep-devpi")
            }
            stages{
                stage("Deploy to Devpi Staging") {
                    agent {
                        dockerfile {
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux&&docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                          }
                    }
                    steps {
                        timeout(5){
                            unstash "PYTHON_PACKAGES"
                            unstash "DOCS_ARCHIVE"
                            sh(
                                label: "Connecting to DevPi Server",
                                script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                            )
                            sh(
                                label: "Uploading to DevPi Staging",
                                script: """devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi
    devpi upload --from-dir dist --clientdir ${WORKSPACE}/devpi"""
                            )
                        }
                    }
                }
                stage("Test DevPi packages") {
                    matrix {
                        axes {
                            axis {
                                name 'PYTHON_VERSION'
                                values '3.7', '3.8'
                            }
                            axis {
                                name 'FORMAT'
                                values "wheel", 'sdist'
                            }
                            axis {
                                name 'PLATFORM'
                                values(
                                    "windows",
                                    "linux"
                                )
                            }
                        }
                        excludes{
                             exclude {
                                 axis {
                                     name 'PLATFORM'
                                     values 'linux'
                                 }
                                 axis {
                                     name 'FORMAT'
                                     values 'wheel'
                                 }
                             }
                        }
                        agent none
                        stages{
                            stage("Testing DevPi Package"){
                                agent {
                                  dockerfile {
                                    filename "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi[FORMAT].dockerfile.filename}"
                                    additionalBuildArgs "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi[FORMAT].dockerfile.additionalBuildArgs}"
                                    label "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi[FORMAT].dockerfile.label}"
                                  }
                                }
                                steps{
                                    script{
                                        if(isUnix()){
                                            sh(
                                                label: "Checking Python version",
                                                script: "python --version"
                                            )
                                            sh(
                                                label: "Connecting to DevPi index",
                                                script: "devpi use https://devpi.library.illinois.edu --clientdir certs && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir certs && devpi use ${env.BRANCH_NAME}_staging --clientdir certs"
                                            )
                                            sh(
                                                label: "Running tests on Devpi",
                                                script: "devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${CONFIGURATIONS[PYTHON_VERSION].devpiSelector[FORMAT]} --clientdir certs -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v"
                                            )
                                        } else {
                                            bat(
                                                label: "Checking Python version",
                                                script: "python --version"
                                            )
                                            bat(
                                                label: "Connecting to DevPi index",
                                                script: "devpi use https://devpi.library.illinois.edu --clientdir certs\\ && devpi login %DEVPI_USR% --password %DEVPI_PSW% --clientdir certs\\ && devpi use ${env.BRANCH_NAME}_staging --clientdir certs\\"
                                            )
                                            bat(
                                                label: "Running tests on Devpi",
                                                script: "devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${CONFIGURATIONS[PYTHON_VERSION].devpiSelector[FORMAT]} --clientdir certs\\ -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v"
                                            )
                                        }
                                    }
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
                        beforeAgent true
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux&&docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    steps {
                        script {
                            try{
                                timeout(30) {
                                    input "Release ${props.Name} ${props.Version} (https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging/${props.Name}/${props.Version}) to DevPi Production? "
                                }
                                sh "devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi  && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi && devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi && devpi push --index ${env.DEVPI_USR}/${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} production/release --clientdir ${WORKSPACE}/devpi"
                            } catch(err){
                                echo "User response timed out. Packages not deployed to DevPi Production."
                            }
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker') {
                        checkout scm
                        script{
                            docker.build("pyhathiprep:devpi",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                sh "devpi push ${props.Name}==${props.Version} DS_Jenkins/${env.BRANCH_NAME} --clientdir ${WORKSPACE}/devpi"
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker') {
                       script{
                            docker.build("pyhathiprep:devpi",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                sh "devpi remove -y ${props.Name}==${props.Version} --clientdir ${WORKSPACE}/devpi"
                            }
                       }
                    }
                }
            }
        }
        stage("Deploy"){
            parallel{
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
                        beforeAgent true
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
                        beforeAgent true
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
                stage("Tagging git Commit"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    when{
                        allOf{
                            equals expected: true, actual: params.DEPLOY_ADD_TAG
                        }
                        beforeAgent true
                        beforeInput true
                    }
                    options{
                        timeout(time: 1, unit: 'DAYS')
                        retry(3)
                    }
                    input {
                          message 'Add a version tag to git commit?'
                          parameters {
                                credentials credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl', defaultValue: 'github.com', description: '', name: 'gitCreds', required: true
                          }
                    }
                    steps{
                        script{
                            def commitTag = input message: 'git commit', parameters: [string(defaultValue: "v${props.Version}", description: 'Version to use a a git tag', name: 'Tag', trim: false)]
                            withCredentials([usernamePassword(credentialsId: gitCreds, passwordVariable: 'password', usernameVariable: 'username')]) {
                                sh(label: "Tagging ${commitTag}",
                                   script: """git config --local credential.helper "!f() { echo username=\\$username; echo password=\\$password; }; f"
                                              git tag -a ${commitTag} -m 'Tagged by Jenkins'
                                              git push origin --tags
                                   """
                                )
                            }
                        }
                    }
                    post{
                        cleanup{
                            deleteDir()
                        }
                    }
                }

            }
        }

    }
}
