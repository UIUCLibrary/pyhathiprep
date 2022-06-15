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

// ============================================================================
// Versions of python that are supported
// ----------------------------------------------------------------------------
SUPPORTED_MAC_VERSIONS = ['3.8', '3.9', '3.10']
SUPPORTED_LINUX_VERSIONS = ['3.6', '3.7', '3.8', '3.9', '3.10']
SUPPORTED_WINDOWS_VERSIONS = ['3.6', '3.7', '3.8', '3.9', '3.10']

PYPI_SERVERS = [
    'https://jenkins.library.illinois.edu/nexus/repository/uiuc_prescon_python_public/',
    'https://jenkins.library.illinois.edu/nexus/repository/uiuc_prescon_python/',
    'https://jenkins.library.illinois.edu/nexus/repository/uiuc_prescon_python_testing/'
    ]

defaultParameterValues = [
    USE_SONARQUBE: false
]

def getDevPiStagingIndex(){

    if (env.TAG_NAME?.trim()){
        return 'tag_staging'
    } else{
        return "${env.BRANCH_NAME}_staging"
    }
}

DEVPI_CONFIG = [
    index: getDevPiStagingIndex(),
    server: 'https://devpi.library.illinois.edu',
    credentialsId: 'DS_devpi',
]

def CONFIGURATIONS = [
    "3.6" : [
        os: [
            windows:[
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                            label: 'windows && docker && x86',
                            additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6'
                        ]
                    ],
                    test:[
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6',
                                baseImage: "python:3.6-windowsservercore"
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/msvc/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker && x86',
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
                            label: 'linux && docker && x86',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    devpi: [
                        whl: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
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
                            label: 'windows && docker && x86',
                            additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/msvc/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/test/msvc/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker && x86',
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
                            label: 'linux && docker && x86',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
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
                            label: 'windows && docker && x86',
                            additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/msvc/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/windows/build/test/msvc/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker && x86',
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
                            label: 'linux && docker && x86',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    devpi: [
                        wheel: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        sdist: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux && docker && x86',
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
node(){
    checkout scm//     tox = load('ci/jenkins/scripts/tox.groovy')
    devpi = load('ci/jenkins/scripts/devpi.groovy')
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
                node('linux && docker && x86') {
                    timeout(2){
                        ws{
                            checkout scm
                            try{
                                docker.image('python').inside {
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


startup()
def props = get_props()


pipeline {
    agent none
    parameters {
        booleanParam(name: "RUN_CHECKS", defaultValue: true, description: "Run checks on code")
        booleanParam(name: 'USE_SONARQUBE', defaultValue: defaultParameterValues.USE_SONARQUBE, description: 'Send data test data to SonarQube')
        booleanParam(name: "TEST_RUN_TOX", defaultValue: false, description: "Run Tox Tests")
        booleanParam(name: "BUILD_PACKAGES", defaultValue: false, description: "Build Python packages")
        booleanParam(name: 'TEST_PACKAGES', defaultValue: false, description: 'Test packages')
        booleanParam(name: 'TEST_PACKAGES_ON_MAC', defaultValue: false, description: 'Test Python packages on Mac')
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: 'DEPLOY_PYPI', defaultValue: false, description: 'Deploy to pypi')
        string(name: 'URL_SUBFOLDER', defaultValue: "pyhathiprep", description: 'The directory that the docs should be saved under')
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    }
    stages {
        stage("Building") {
            agent {
                dockerfile {
                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                    label "linux && docker && x86"
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
                                    label "linux && docker && x86"
                                    additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                    args '--mount source=sonar-cache-tyko,target=/opt/sonar/.sonar/cache'
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
//                                             post{
//                                                 always{
//                                                     stash includes: 'reports/pytest/*.xml', name: 'PYTEST_UNIT_TEST_RESULTS'
//                                                     junit 'reports/pytest/junit-pytest.xml'
//                                                 }
//                                             }
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
                                            }
                                        }
                                        stage('Task Scanner'){
                                            steps{
                                                recordIssues(tools: [taskScanner(highTags: 'FIXME', includePattern: 'pyhathiprep/**/*.py', normalTags: 'TODO')])
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
                                    }
                                }
                                stage('Run Sonarqube Analysis'){
                                    options{
                                        lock('pyhathiprep-sonarscanner')
                                        retry(3)
                                    }
                                    when{
                                        equals expected: true, actual: params.USE_SONARQUBE
                                    }
                                    steps{
                                        script{
                                            def sonarqube = load('ci/jenkins/scripts/sonarqube.groovy')
                                            def newProps = get_props()
                                            sonarqube.sonarcloudSubmit(
                                                credentialsId: SONARQUBE_CREDENTIAL_ID,
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
                                            [pattern: "dist/", type: 'INCLUDE'],
                                            [pattern: 'build/', type: 'INCLUDE'],
                                            [pattern: 'pyhathiprep.egg-info/', type: 'INCLUDE'],
                                            [pattern: 'reports/', type: 'INCLUDE'],
                                            [pattern: 'logs/', type: 'INCLUDE'],
                                            [pattern: '.mypy_cache/', type: 'INCLUDE'],
                                            [pattern: '.pytest_cache/', type: 'INCLUDE'],

                                            ]
                                    )
                                }
                            }
                        }
//                         stage('Run Sonarqube Analysis'){
//                             options{
//                                 lock('pyhathiprep-sonarscanner')
//                                 retry(3)
//                             }
//                             when{
//                                 equals expected: true, actual: params.USE_SONARQUBE
//                                 beforeAgent true
//                                 beforeOptions true
//                             }
//                             steps{
//                                 script{
//                                     def sonarqube
//                                     node(){
//                                         checkout scm
//                                         sonarqube = load('ci/jenkins/scripts/sonarqube.groovy')
//                                     }
//                                     def stashes = [
//                                         'COVERAGE_REPORT_DATA',
//                                         'PYTEST_UNIT_TEST_RESULTS',
//                                         'PYLINT_REPORT',
//                                         'FLAKE8_REPORT'
//                                     ]
//                                     def sonarqubeConfig = [
//                                         installationName: 'sonarcloud',
//                                         credentialsId: SONARQUBE_CREDENTIAL_ID,
//                                     ]
//                                     def agent = [
//                                             dockerfile: [
//                                                 filename: 'ci/docker/python/linux/jenkins/Dockerfile',
//                                                 label: 'linux && docker && x86',
//                                                 additionalBuildArgs: '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
//                                                 args: '--mount source=sonar-cache-hathiprep,target=/home/user/.sonar/cache',
//                                             ]
//                                         ]
//                                     if (env.CHANGE_ID){
//                                         sonarqube.submitToSonarcloud(
//                                             agent: agent,
//                                             reportStashes: stashes,
//                                             artifactStash: 'sonarqube artifacts',
//                                             sonarqube: sonarqubeConfig,
//                                             pullRequest: [
//                                                 source: env.CHANGE_ID,
//                                                 destination: env.BRANCH_NAME,
//                                             ],
//                                             package: [
//                                                 version: props.Version,
//                                                 name: props.Name
//                                             ],
//                                         )
//                                     } else {
//                                         sonarqube.submitToSonarcloud(
//                                             agent: agent,
//                                             reportStashes: stashes,
//                                             artifactStash: 'sonarqube artifacts',
//                                             sonarqube: sonarqubeConfig,
//                                             package: [
//                                                 version: props.Version,
//                                                 name: props.Name
//                                             ]
//                                         )
//                                     }
//                                 }
//                             }
//                             post {
//                                 always{
//                                     node(''){
//                                         unstash 'sonarqube artifacts'
//                                         recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
//                                     }
//                                 }
//                             }
//                         }
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
                                                label: "linux && docker && x86",
                                                dockerfile: "ci/docker/python/linux/tox/Dockerfile",
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                            )
                                    },
                                    "Windows":{
                                        windowsJobs = tox.getToxTestsParallel(
                                                envNamePrefix: "Tox Windows",
                                                label: 'windows && docker && x86',
                                                dockerfile: "ci/docker/python/windows/tox/Dockerfile",
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
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
                stage("Building Source and Wheel formats"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux && docker && x86'
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
                stage("Testing Packages"){
                    when{
                        equals expected: true, actual: params.TEST_PACKAGES
                        beforeAgent true
                    }
                    steps{
                        script{
                            def packages
                            node(){
                                checkout scm
                                packages = load('ci/jenkins/scripts/packaging.groovy')
                            }
                        def windowsTests = [:]
                            SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                                windowsTests["Windows - Python ${pythonVersion}: sdist"] = {
                                        packages.testPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
                                                ]
                                            ],
                                            glob: 'dist/*.tar.gz,dist/*.zip',
                                            stash: 'PYTHON_PACKAGES',
                                            pythonVersion: pythonVersion
                                        )
                                    }
                                windowsTests["Windows - Python ${pythonVersion}: wheel"] = {
                                        packages.testPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
                                                ]
                                            ],
                                            glob: 'dist/*.whl',
                                            stash: 'PYTHON_PACKAGES',
                                            pythonVersion: pythonVersion
                                        )
                                    }
                            }

                            def linuxTests = [:]
                            SUPPORTED_LINUX_VERSIONS.each{ pythonVersion ->
                                linuxTests["Linux - Python ${pythonVersion}: sdist"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'linux && docker && x86',
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                            ]
                                        ],
                                        glob: 'dist/*.tar.gz',
                                        stash: 'PYTHON_PACKAGES',
                                        pythonVersion: pythonVersion
                                    )
                                }
                                linuxTests["Linux - Python ${pythonVersion}: wheel"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'linux && docker && x86',
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                            ]
                                        ],
                                        glob: 'dist/*.whl',
                                        stash: 'PYTHON_PACKAGES',
                                        pythonVersion: pythonVersion
                                    )
                                }
                            }

                            def macTests = [:]
                            SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
                                macTests["Mac - Python ${pythonVersion}: sdist"] = {
                                    packages.testPkg(
                                            agent: [
                                                label: "mac && python${pythonVersion}",
                                            ],
                                            glob: 'dist/*.tar.gz,dist/*.zip',
                                            stash: 'PYTHON_PACKAGES',
                                            pythonVersion: pythonVersion,
                                            toxExec: 'venv/bin/tox',
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                                sh(
                                                    label:'Install Tox',
                                                    script: '''python3 -m venv venv
                                                               venv/bin/pip install pip --upgrade
                                                               venv/bin/pip install tox
                                                               '''
                                                )
                                            },
                                            testTeardown: {
                                                sh 'rm -r venv/'
                                            }

                                        )
                                }
                                macTests["Mac - Python ${pythonVersion}: wheel"] = {
                                    packages.testPkg(
                                            agent: [
                                                label: "mac && python${pythonVersion}",
                                            ],
                                            glob: 'dist/*.whl',
                                            stash: 'PYTHON_PACKAGES',
                                            pythonVersion: pythonVersion,
                                            toxExec: 'venv/bin/tox',
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                                sh(
                                                    label:'Install Tox',
                                                    script: '''python3 -m venv venv
                                                               venv/bin/pip install pip --upgrade
                                                               venv/bin/pip install tox
                                                               '''
                                                )
                                            },
                                            testTeardown: {
                                                sh 'rm -r venv/'
                                            }

                                        )
                                }
                            }
                            def tests = linuxTests + windowsTests
                            if(params.TEST_PACKAGES_ON_MAC == true){
                                tests = tests + macTests
                            }
                            parallel(tests)
                        }
                    }
                }
            }
        }
        stage("Deploy to Devpi"){
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
                lock("pyhathiprep-devpi")
            }
            stages{
                stage('Uploading to DevPi Staging'){
                    agent {
                        dockerfile {
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux && docker && devpi-access'
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
                                        index: DEVPI_CONFIG.index,
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
                            SUPPORTED_MAC_VERSIONS.each{pythonVersion ->
                                macPackages["Test Python ${pythonVersion}: wheel Mac"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            label: "mac && python${pythonVersion} && devpi-access"
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.index,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                            devpiExec: 'venv/bin/devpi'
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'whl'
                                        ],
                                        test:[
                                            setup: {
                                                sh(
                                                    label:'Installing Devpi client',
                                                    script: '''python3 -m venv venv
                                                                venv/bin/python -m pip install pip --upgrade
                                                                venv/bin/python -m pip install devpi_client
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
                                macPackages["Test Python ${pythonVersion}: sdist Mac"]= {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            label: "mac && python${pythonVersion} && devpi-access"
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.index,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                            devpiExec: 'venv/bin/devpi'
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'tar.gz'
                                        ],
                                        test:[
                                            setup: {
                                                sh(
                                                    label:'Installing Devpi client',
                                                    script: '''python3 -m venv venv
                                                                venv/bin/python -m pip install pip --upgrade
                                                                venv/bin/python -m pip install devpi_client
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
                            def windowsPackages = [:]
                            SUPPORTED_WINDOWS_VERSIONS.each{pythonVersion ->
                                windowsPackages["Test Python ${pythonVersion}: sdist Windows"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                additionalBuildArgs: "--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE",
                                                label: 'windows && docker && x86'
                                            ]
                                        ],
                                        devpi: DEVPI_CONFIG,
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
                                                additionalBuildArgs: "--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE",
                                                label: 'windows && docker && x86 && devpi-access'
                                            ]
                                        ],
                                        devpi: DEVPI_CONFIG,
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
                            def linuxPackages = [:]
                            SUPPORTED_LINUX_VERSIONS.each{pythonVersion ->
                                linuxPackages["Test Python ${pythonVersion}: sdist Linux"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: "--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL",
                                                label: 'linux && docker && x86 && devpi-access'
                                            ]
                                        ],
                                        devpi: DEVPI_CONFIG,
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
                                                additionalBuildArgs: "--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL",
                                                label: 'linux && docker && x86 && devpi-access'
                                            ]
                                        ],
                                        devpi: DEVPI_CONFIG,
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
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
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
                                indexSource: DEVPI_CONFIG.index,
                                indexDestination: 'production/release',
                                credentialsId: DEVPI_CONFIG.credentialsId
                            )
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker && x86') {
                        checkout scm
                        script{
                            if (!env.TAG_NAME?.trim()){
                                docker.build("pyhathiprep:devpi",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                    devpi.pushPackageToIndex(
                                        pkgName: props.Name,
                                        pkgVersion: props.Version,
                                        server: DEVPI_CONFIG.server,
                                        indexSource: DEVPI_CONFIG.index,
                                        indexDestination: "DS_Jenkins/${env.BRANCH_NAME}",
                                        credentialsId: DEVPI_CONFIG.credentialsId
                                    )
                                }
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker && x86') {
                       script{
                            docker.build("pyhathiprep:devpi",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                devpi.removePackage(
                                    pkgName: props.Name,
                                    pkgVersion: props.Version,
                                    index: DEVPI_CONFIG.index,
                                    server: DEVPI_CONFIG.server,
                                    credentialsId: DEVPI_CONFIG.credentialsId,

                                )
                            }
                       }
                    }
                }
            }
        }
        stage("Deploy"){
            parallel{
                stage('Deploy to pypi') {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label "linux && docker && x86"
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
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
                                choices: PYPI_SERVERS,
                                description: 'Url to the pypi index to upload python packages.',
                                name: 'SERVER_URL'
                            )
                        }
                    }
                    steps{
                        unstash 'PYTHON_PACKAGES'
                        script{
                            def pypi = fileLoader.fromGit(
                                    'pypi',
                                    'https://github.com/UIUCLibrary/jenkins_helper_scripts.git',
                                    '2',
                                    null,
                                    ''
                                )
                            pypi.pypiUpload(
                                credentialsId: 'jenkins-nexus',
                                repositoryUrl: SERVER_URL,
                                glob: 'dist/*'
                                )
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
                stage('Deploy Online Documentation') {
                    when{
                        equals expected: true, actual: params.DEPLOY_DOCS
                        beforeAgent true
                        beforeInput true
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label "linux && docker && x86"
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
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
