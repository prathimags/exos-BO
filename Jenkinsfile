pipeline {
  agent none
  stages {
    stage('build') {
      steps {
        build 'Image Sanity Test (Stage)/435-summitlitearm-job'
        git 'https://github.com/prathimags/exos-bo.git'
      }
    }

    stage('test') {
      steps {
        sh 'echo "test"'
        sh 'python -V'
        sh 'python -m pytest'
      }
    }

  }
}