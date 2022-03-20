pipeline {
    agent any
    environment {
        PROJECT_ID = ''
        CLUSTER_NAME = ''
        LOCATION = ''
        CREDENTIALS_ID = credentials('automation')
    }

    stages {
        stage("Code checkout"){
            steps {
               checkout scm
            }
        }

        stage('Compile manifests'){
            steps{
            sh """ kubectl kustomize . > compile.yml  """
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

    }



}
