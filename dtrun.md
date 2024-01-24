

**Architecture**

Below block diagram gives an overview of DT automation with APIs

![image](https://user-images.githubusercontent.com/17583786/165476237-4b687ec7-87e7-4175-a76b-5cff72703f87.png)

**Script Flow**

- Get VIQ ID
- Dynamically generate serial number based on VIQ ID:
Format: viqstr+serpadding+"-"+str(random.randint(10000,99999))
- Dynamically generate MAC address
  Format: macseed+":"+str(viqstr[:2])+":"+str(viqstr[2:4])+":"+str(random.randint(11,63))+":"+"00"
  macseed: Fist 2 octects of MAC- passed as parameter to function
- Create DT instance. Use dynamically generated ser,mac from previous steps (gRPC- DTIS middleware)
- Onboard created DT to XIQ (XIQ XAPI)
- Validate license consumption (XIQ XAPI- SEE XIQ-5864)
- Assign policy (XIQ XAPI)
- Update policy (XIQ XAPI)
- Validate configuration with device CLIs (XAPI CLI)
- Delete device from XIQ (XAPI)
- Delete DT instance (gRPC- DTIS)

**YAML files required**

The scripts do not require device YAMLs as devices are generanted dynamically. Howeve, YAML files are needed for XIQ and DTIS endpoits

**XIQ sample yaml**


![image](https://user-images.githubusercontent.com/17583786/165481927-b8e6e899-0666-4afe-859b-e808152326aa.png)

  
 Note: 
 1. THe policy mentioned in YAML should be precreatead and should have devicetemplates, config required for tests.
 2. IQAgent version should be latest supported in the environment.
 
 **DTIS endpoint yaml**
 
 
 ![image](https://user-images.githubusercontent.com/17583786/165480484-2ff35f5b-5524-430e-b695-28e75fef0384.png)

  Note: Seperate DTIS YAMLs might be required for switchengine and fabricengine. Ensure supported OSVERSION is mentioned
  
  **Running Tests**
  
  pytest -x --html=".\reports\DigitalTwin-5520-24T.html" --tc-file=".\Config_files\dtisendpoint.yaml" --tc-file=".\Config_files\xiq.cp3.qa.yaml" --model "5520-24T" test_dtsanity.py
  
 
  **Author/Contact info**
  Sathish Kumar Srinivasan sasrinivasan@extremenetworks.com
