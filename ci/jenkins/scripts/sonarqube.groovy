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
    def buildString = args['buildString'] ? args['buildString']: env.BUILD_TAG
    def isPullRequest = args['pullRequest'] ? true: false
    withSonarQubeEnv(installationName:'sonarcloud', credentialsId: args.credentialsId) {
        echo "args = ${args}"
        def projectVersion = args.version

        if (isPullRequest == true){
            def pullRequestKey = args.pullRequest.source
            def pullRequestBase = args.pullRequest.destination
            sh(
                label: "Running Sonar Scanner",
                script:"sonar-scanner -Dsonar.projectVersion=${projectVersion} -Dsonar.buildString=\"${buildString}\" -Dsonar.pullrequest.key=${pullRequestKey} -Dsonar.pullrequest.base=${pullRequestBase}"
                )
        } else {
            def branchName =  args['branchName'] ? args['branchName']: env.BRANCH_NAME
            sh(
                label: "Running Sonar Scanner",
                script: "sonar-scanner -Dsonar.projectVersion=${projectVersion} -Dsonar.buildString=\"${buildString}\" -Dsonar.branch.name=${branchName}"
                )
        }
    }
    timeout(time: 1, unit: 'HOURS') {
         def sonarqube_result = waitForQualityGate(abortPipeline: false)
         if (sonarqube_result.status != 'OK') {
             unstable "SonarQube quality gate: ${sonarqube_result.status}"
         }
         def outstandingIssues = get_sonarqube_unresolved_issues('.scannerwork/report-task.txt')
         writeJSON file: args.outputJson, json: outstandingIssues
     }
}
return this