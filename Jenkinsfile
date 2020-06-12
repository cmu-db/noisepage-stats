#!groovy
pipeline {
  environment{
    BRANCH_NAME = branch
  }
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
          when{
            changeset "performance-storage-service/**"
          }
          steps{
            build job: "performance-storage-service/${BRANCH_NAME}", wait: true
          }
        }
        stage('TimescaleDB'){
          when{
            changeset "timescale/**"
          }
          steps{
            build job: "noisepage-test-timescale", wait: true
          }
        }
        stage('Grafana'){
          when{
            changeset "grafana/**"
          }
          steps{
            build job: "noisepage-test-grafana", wait: true
          }
        }
      }
    }
  }
}
