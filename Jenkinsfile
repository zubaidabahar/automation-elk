pipeline {
    agent any
    environment {
        PROJECT_ID = 'eloquent-ratio-344711'
        CLUSTER_NAME = 'elk-autmation'
        LOCATION = 'ús-central1-c'
        CREDENTIALS_ID = credentials('automation-elk')
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
