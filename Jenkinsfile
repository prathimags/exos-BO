pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        build 'Image Sanity Test (G2R1)/450-SummitX-job'
      }
    }

    stage('test') {
      steps {
        echo 'Check the reports in http://10.127.13.204/'
      }
    }

  }
}