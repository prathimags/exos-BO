pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        build 'CI-CD-Blueocean-G2R1/exos-github-repo'
      }
    }

    stage('SanityRun') {
      steps {
        build 'CI-CD-Blueocean-G2R1/450-SummitX-job-bo'
      }
    }

    stage('Reports') {
      steps {
        echo 'Check the reports in http://10.127.13.204/blueocean/imagetesting/'
      }
    }

  }
}