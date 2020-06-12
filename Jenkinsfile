#!groovy
pipeline {
  agent {
    label 'docker'
  }
  stages{
    stage('Checkout'){
      steps{
        checkout scm
      }
    }
    stage('Trigger Build Pipelines') {
      parallel {
        stage('Performance Storage Service'){
          steps{
            when{
              changeset "/performance-storage-service"
            }
            build job: 'performance-storage-service', wait: true
          }
        }
        stage('TimescaleDB'){
          steps{
            when{
              changeset "/timescale"
            }
            build job: 'noisepage-test-timescale', wait: true
          }
        }
        stage('Grafana'){
          steps{
            when{
              changeset "/grafana"
            }
            build job: 'noisepage-test-grafana', wait: true
          }
        }
      }
    }
  }
}
