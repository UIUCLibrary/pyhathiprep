def get_sonarqube_unresolved_issues(report_task_file){
    script{

        def props = readProperties  file: '.scannerwork/report-task.txt'
        def response = httpRequest url : props['serverUrl'] + '/api/issues/search?componentKeys=' + props['projectKey'] + '&resolved=no'
        def outstandingIssues = readJSON text: response.content
        return outstandingIssues
    }
}


def sonarcloudSubmit(args = [:]){
    args.outputJson = args.outputJson ? args.outputJson: "reports/sonar-report.json"
    withSonarQubeEnv(installationName:'sonarcloud', credentialsId: args.credentialsId) {
        echo "args = ${args}"
//         def command
//         if (env.CHANGE_ID){
//             command = "sonar-scanner -Dsonar.projectVersion=${props.Version} -Dsonar.buildString=\"${env.BUILD_TAG}\" -Dsonar.pullrequest.key=${env.CHANGE_ID} -Dsonar.pullrequest.base=${env.CHANGE_TARGET} -Dsonar.cfamily.cache.enabled=false -Dsonar.cfamily.threads=\$(grep -c ^processor /proc/cpuinfo) -Dsonar.cfamily.build-wrapper-output=build/build_wrapper_output_directory"
//         } else {
//             command = "sonar-scanner -Dsonar.projectVersion=${props.Version} -Dsonar.buildString=\"${env.BUILD_TAG}\" -Dsonar.branch.name=${env.BRANCH_NAME} -Dsonar.cfamily.cache.enabled=false -Dsonar.cfamily.threads=\$(grep -c ^processor /proc/cpuinfo) -Dsonar.cfamily.build-wrapper-output=build/build_wrapper_output_directory"
//         }
//         sh command
    }
//     timeout(time: 1, unit: 'HOURS') {
//          def sonarqube_result = waitForQualityGate(abortPipeline: false)
//          if (sonarqube_result.status != 'OK') {
//              unstable "SonarQube quality gate: ${sonarqube_result.status}"
//          }
//          def outstandingIssues = get_sonarqube_unresolved_issues('.scannerwork/report-task.txt')
//          writeJSON file: args.outputJson, json: outstandingIssues
//      }
}
return this