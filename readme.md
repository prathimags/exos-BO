## XIQ Release Test

## Install python 3.x
Install [Python 3](https://www.python.org/downloads/) on your development system. This is required to run these tests.

### Install Packages

Install all the required packages
~~~
pip install -r requirements.txt
~~~

### Pytest Execution

##### Pytest Command Format: 
pytest -x --html="Path to html report file" --tc-file="Path to device config file" --tc-file="Path to topo environment file" --tc-format=yaml test_exos_relsanity.py

#### Example cmds:
summitX(x450) test on G2 Environment:
~~~
pytest -x --html=".\reports\report-summitX_X450-G2-yaml.html" --tc-file=".\Config_files\device_summitX_x450.yaml" --tc-file=".\Config_files\topo.test.g2r1.qa.yaml" test_exos_relsanity.py

pytest -x --html=".\reports\report-summitX_X450-G2-yaml.html" --tc-file=".\Config_files\device_summitX_x450.yaml" --tc-file=".\Config_files\topo.test.g2r1.qa.yaml" --tc-format=yaml test_exos_relsanity.py
~~~

summitArm(5520) test on Prod AUS RDC Environment:
~~~
pytest -x --html=".\reports\report-summitArm_5520-Aus-yaml.html" --tc-file=".\Config_files\device_summitarm_5520.yaml" --tc-file=".\Config_files\topo.prod.aus.yaml" test_exos_relsanity.py

pytest -x --html=".\reports\report-summitArm_5520-Aus-yaml.html" --tc-file=".\Config_files\device_summitarm_5520.yaml" --tc-file=".\Config_files\topo.prod.aus.yaml" --tc-format=yaml test_exos_relsanity.py
~~~

#### Performance Testing:
While testing the performance on any environment, policy templates must be created on GUI manually and for each policy a separate yaml file must be created by specifying the policy name.

Refer example yaml files for performance testing on G2 Env:
* [topo.test.g2r1.100vlan_10ports.yaml](https://github.com/extremenetworks/extreme_automation_tests/blob/exos-xiqrelease/Tests/Pytest/ReleaseTest/exos/Config_files/topo.test.g2r1.100vlan_10ports.yaml)
* [topo.test.g2r1.1000vlan_10ports.yaml](https://github.com/extremenetworks/extreme_automation_tests/blob/exos-xiqrelease/Tests/Pytest/ReleaseTest/exos/Config_files/topo.test.g2r1.1000vlan_10ports.yaml)


