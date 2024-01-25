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
        //sh 'pip install --user -r requirements.txt'
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
