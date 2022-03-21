pipeline {
    agent any
    environment {
        PROJECT_ID = 'eloquent-ratio-344711'
        CLUSTER_NAME = 'elk-automation'
        LOCATION = 'us-central1-c'
        CREDENTIALS_ID = 'automation-elk'
    }

    stages {
        stage("Code checkout"){
            steps {
               checkout scm
            }
        }

        stage('Compile manifests'){
            steps{
            sh """ kubectl kustomize . > compiled.yml  """
            }
        }

        stage ('Deploy to Google Kubernetes Engine') {
            steps {
                step([
                $class: 'KubernetesEngineBuilder',
                projectId: env.PROJECT_ID,
                clusterName: env.CLUSTER_NAME,
                location: env.LOCATION,
                manifestPattern: 'compiled.yml',
                credentialsId: env.CREDENTIALS_ID,
                verifyDeployments: false
                ])
            }
        }

        stage ('Prepare for Testing'){
        steps {
            script{
                withCredentials([file(credentialsId: 'service-account', variable: 'service_account')]){
                    sh """
                        cp \$service_account support/gcp_sa.json
                        chmod 640 support/gcp_sa.json
                       """
                }
            }
        }
        }
        stage("Install Requirements"){
            steps{
            sh """
                pip3 install -r requirements.txt
                """
            }
         }

        stage("Infrastructure test"){
            steps{
            sh """
                . env/bin/activate
                pytest --junitxml=report.xml
                """
            }
         }

    }



}
