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
home_dir="/home/extreme/automation/exos/reports"
target_directory=$home_dir$file_name
sudo_password="Extreme@123"

pytest --html=$target_directory --tc-file="/home/extreme/automation/exos/Config_files/device_summitarm_lite_x435.yaml" --tc-file="/home/extreme/automation/exos/Config_files/topo.test.staging.yaml" /home/extreme/automation/exos/test_exos_relsanity.py

echo $sudo_password | sudo -S cp $target_directory $test_suite_dir
'''
      }
    }

  }
}