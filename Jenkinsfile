pipeline {
  agent none
  stages {
    stage('build') {
      steps {
        build 'Image Sanity Test (Stage)/450-SummitX-job'
      }
    }

    stage('test') {
      steps {
        echo 'Check the reports in http://10.127.13.204/'
      }
    }

  }
}