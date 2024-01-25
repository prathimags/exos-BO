pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('build') {
      steps {
        git 'https://github.com/prathimags/exos-bo.git'
        build 'Image Sanity Test (Stage)/435-summitlitearm-job'
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