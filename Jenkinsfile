pipeline {
  agent any
  stages {
    stage('Initialize') {
      steps {
        echo 'This is a minimal pipeline'
      }
    }

    stage('TriggerPytest') {
      steps {
        sh '''file_name="/report-summitlite-arm_435_staging_Jenkins-Job.html "
home_dir="./reports"
target_directory=$home_dir$file_name
sudo_password="Extreme@123"

pytest --html=$target_directory --tc-file="./Config_files/device_summitarm_lite_x435.yaml" --tc-file="./Config_files/topo.test.staging.yaml" ./test_exos_relsanity.py

'''
      }
    }

  }
}