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

       
        stage("Prepare for testing"){
            steps{
            sh """
                python3 -m venv env
                . env/bin/activate
                pip3 install -r requirements.txt
                """
            }
         }

        stage("Infrastructure test"){
            steps{
            sh """
                pip3 install pytest
                pytest /tests/test_infrastructure.py
                """
            }
         }

    }



}
