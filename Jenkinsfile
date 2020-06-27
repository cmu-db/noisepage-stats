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
          when{
            changeset "performance-storage-service/**"
          }
          steps{
            build job: "noisepage-test-performance-storage-service/${env.BRANCH_NAME}", wait: true, propagate: true
          }
        }
        stage('TimescaleDB'){
          when{
            changeset "timescaledb/**"
          }
          steps{
            build job: "noisepage-test-timescale/${env.BRANCH_NAME}", wait: true, propagate: true
          }
        }
        stage('Grafana'){
          when{
            changeset "grafana/**"
          }
          steps{
            build job: "noisepage-test-grafana/${env.BRANCH_NAME}", wait: true,  propagate: true
          }
        }
      }
    }
  }
}
