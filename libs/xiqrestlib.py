###################################################
# Author:Sathish Kumar Srinivasan
# Contact: sasrinivasan@extremenetworks.com
#
#
####################################################
import time
import logging
import requests
import inspect
import datetime
import logging as logger
import os


okRespCodeList=[200,202]
snsList=[]

apiurl="apiurl"
xiquser="xiquser"
xiqpass="xiqpass"
authurl="authurl"
'''
apiurl="https://g2-api.qa.xcloudiq.com/"
xiquser="sasrinivasan@extremenetworks.com"
xiqpass="Aerohive123"
authurl="https://g2-api.qa.xcloudiq.com/login"
'''

polname=""

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

def CheckRestError(status_code=500,response=""):
    respOK=True
    callerfunction=str(inspect.stack()[1].function)


    if status_code not in okRespCodeList:
        logging.error("Unexpected response from REST server- Response  is %s",response)
        
        logging.error("Calling Function is %s",callerfunction)
        respOK=False
    return respOK

def CreateLogReport(logname='Logs_'):
    filename= logname +"_"+ datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.log'
    if not os.path.exists("Testlog"):
        os.makedirs("Testlog")
        
    
    logging.basicConfig(
    filename='./Testlog/'+filename,
    level=logging.INFO, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
     )


# Login to XIQ with user/pass and get  a bearer/auth token. This is needed for further REST requests
def xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass):
    accessToken=None
    auth_token_header_value = None

    data = { "username": xiquser, "password": xiqpass }
    auth_response = requests.post(authurl, json=data,headers=headers)
    statusCode=auth_response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=auth_response.text)
  
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("Authentication  successfull. Access token is:")
        logger.debug(auth_response.text)

        #authToken=json.dumps(auth_response.text)["access_token"]
        auth_token=auth_response.json()
        accessToken=auth_token["access_token"]
        auth_token_header_value = "Bearer %s" % accessToken
    
    
    return auth_token_header_value

#Returns a dictionary with VIQ, license info
#{'devices': 10, 'standalone': True, 'expired': True, 'customer_id': 'CMJJ-39NQ-YQMH-VUQP', 'vhm_id': 'VHM-ZMLJFVIJ', 'owner_id': 4362, 'licenses': [{'id': 4229912, 'create_time': '2022-03-04T09:06:13.000+0000', 'update_time': '2022-03-04T09:06:13.000+0000', 'status': 'BUY', 'active_date': '2022-03-04T09:06:13.000+0000', 'expire_date': '2023-03-04T00:00:00.000+0000', 'entitlement_key': 'IZSF9-JBMLW-A4WLP-2YQLE-CYHAT-QJDEA', 'entitlement_type': 'PERMANENT', 'mode': 'BUY', 'devices': 10, 'activated': 0, 'available': 0}]}
def get_xiqviqinfo(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="account/viq",auth_token="None"):
    url=apiurl+path
    
    ViqInfo={}
    if auth_token=="None":
        logger.info("get_xiqviqinfo-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqdeviceList-XIQ added list of devices:")
        logger.debug(response.json())
        ViqInfo=response.json()
    
    return ViqInfo

def post_xiqOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:onboard",deviceType="exos",field="sns",snsList=[],auth_token="None"):
    url=apiurl+path
    onboardeddeviceList=None
    
    OnBoarded=False
    
    onboardDeviceDict={deviceType:{ "sns": []}}
    
    if auth_token=="None":
        logger.info("post_xiqOnboardDevices-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
        
    logger.info(f"Onboarding devices with serial numbers:{snsList}")
    for serialno in snsList:
        onboardDeviceDict[deviceType][field].append(serialno)
    
    data=onboardDeviceDict
    #print (data)
    headers={'accept': 'application/json',"Authorization": auth_token}
    response = requests.post(url, json=data,headers=headers)

    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.info("Devices added to XIQ")

        OnBoarded=True

    return OnBoarded

#Returns a dictionary list of  onboarded  devices
def get_xiqdeviceListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices?page=1&limit=100&deviceTypes=REAL&deviceTypes=DIGITAL_TWIN&async=false",auth_token="None"):
    url=apiurl+path
    DeviceInfo={}
    if auth_token=="None":
        logger.info("get_xiqdeviceListDict-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqdeviceList-XIQ added list of devices:")
        logger.debug(response.json())
        DeviceInfo=response.json()
    
    return DeviceInfo

#Returns a dictionary list of  clients connected to  onboarded devices
def get_xiqclientListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="clients/active?page=1&limit=10000", auth_token="None"):
    url=apiurl+path
    ClientInfo={}
    if auth_token=="None":
        logger.info("get_xiqclientListDict-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqclientListDict-List of connected clients")
        logger.debug(response.json())
        ClientInfo=response.json()
    #print(UserInfo)
    return ClientInfo

# Given a device serial  number, fetch onboarded device ID
def get_xiqDeviceId(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None"):
    DeviceId=None
    
    if auth_token=="None":
        logger.info("get_xiqDeviceId-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    deviceInfoDict=get_xiqdeviceListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token)

    logger.info("get_xiqDeviceId:List of devices\t" +str(deviceInfoDict))
    deviceList=deviceInfoDict['data']
    for device in deviceList:
        if device['serial_number']== sn:
            DeviceId=device['id']
    return DeviceId


# Poll device status periodically till it reaches a state Managed in given time
#Start time- Inital sleep, increment time- periodic poll time, endtime- final time before returning failure

def CheckDeviceStatusPeriodic(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None",starttime=30,incrementtime=10,endtime=600):
    deviceStatus="NOT_PRESENT"
    connecttime=starttime
    poll=True
    if auth_token=="None":
        logger.info("get_xiqDeviceId-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    logger.info(f"Sleeping for {starttime} before checking device status")
    time.sleep(starttime)

    while poll==True:
        
        deviceInfoDict=get_xiqdeviceListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token)

        logger.info("get_xiqDeviceId:List of devices\t" +str(deviceInfoDict))
        deviceList=deviceInfoDict['data']

        if (deviceList == []):
            logger.error(f"Get device API did not return any devices - Issue similar to XIQ-14386.")
            poll=False
            break

        for device in deviceList:
 
            if (device['serial_number']== sn) and (device["device_admin_state"]=="MANAGED"):
                
                
                logger.info(f"Device status is Managed- Time taken {connecttime} seconds")
                poll=False
                deviceStatus="MANAGED"
                

                break
                
            elif (connecttime >= endtime):
                    logger.error(f"Device state did not change to managed in {endtime} seconds.")
                    logger.info(device)
                    poll=False
                    break
            else:
                #devicestate=device["device_admin_state"]
                #logger.info(f"Current state of device with serial number {sn} is {devicestate} ")
                logger.info(f"Time elapsed {connecttime} sec.Sleeping for {incrementtime} seconds before next poll")
                time.sleep(incrementtime)
                connecttime=connecttime+incrementtime
                    

    return deviceStatus

# Delete Devices from XIQ
def post_xiqDelOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:delete",snsList=[],auth_token="None"):
    url=apiurl+path
    data = {"ids":[]}
    Deleted=False
    if auth_token=="None":
        logger.info("post_xiqDelOnboardDevice-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    for serialno in snsList:
        devid=""
        devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=serialno,auth_token=auth_token)
        if devid !="None":
            data["ids"].append(devid)
    
    #print(data)

    logger.info("From post_xiqDelOnboardDevices- Devices ID list:\t",data)

  
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response = requests.post(url, json=data,headers=headers)
    #print(response)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)

    if responseOK!=False: 
        #print(auth_response.text)
        logger.debug("Devices deleted from XIQ")

        Deleted=True

    return  Deleted



def xiqsendclitodevice(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:cli",deviceType="exos",cliList=[],snsList=[],auth_token="None"):

    cliResp={}
    url=apiurl+path
    cliRespJson={}
   
     
    cliDict = {"devices":{"ids":[]},"clis":[]}
    
    cliExecTImeDict={"devices":{"ids":[]},"clis":[],"execTime":[]}

    if auth_token=="None":
        logger.info("xiqsendclitodevice-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    for serialno in snsList:
        id=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=serialno,auth_token=auth_token)
        cliDict["devices"]["ids"].append(id)
        cliExecTImeDict["devices"]["ids"].append(id)
        
    for cli in cliList:
        cliDict["clis"].append(cli)
        cliExecTImeDict["clis"].append(cli)
        #Dict for CLIresp time

    #print(cliDict)
    headers={'accept': 'application/json',"Authorization": auth_token,}
    #Start clock tick
    cli_begin_time = datetime.datetime.now()
    logger.debug(f"CLI dictionary is {cliDict}")
    response = requests.post(url, json=cliDict,headers=headers)
    #End it after getting resp from XIQ
    cli_endtime=datetime.datetime.now()-cli_begin_time
    cliExecTImeDict["execTime"].append(cli_endtime)

    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)

    
    if responseOK!=False:
        
        logger.debug(f"CLI executed for devices")
        cliRespJson=response.json()
        
    return cliRespJson,cliExecTImeDict

#Returns a dictionary list of  policies
def get_xiqpolicyListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="network-policies?page=1&limit=30",auth_token="None"):
    url=apiurl+path
    #print(url)
    PolicyInfo={}

    if auth_token=="None":
        logger.info("Auth token not passed- Generating new token")
        accessToken,auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqpolicyListDic-List of policies")
        logger.debug(response.json())
        PolicyInfo=response.json()
    #print(UserInfo)
    return PolicyInfo

def get_xiqpolicyId(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,polname="Wired",auth_token="None"):
    PolicyId=None
    
    if auth_token=="None":
        logger.info("Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    policyInfoDict=get_xiqpolicyListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token)
    
    logger.debug("get_xiqDeviceId:List of policy\t" +str(policyInfoDict))
    policyList=policyInfoDict['data']
    for pol in policyList:
        if pol['name']== polname:
            PolicyId=pol['id']

    return PolicyId
#assign a policy to device
def put_xiqpoldevice(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,snsList=[],polname="None",auth_token="None"):
    
    if auth_token=="None":
        logger.info("Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    headers={'accept': 'application/json',"Authorization": auth_token,}
    
    polstatusdict={}
    
    for serialno in snsList:
        deviceid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=serialno,auth_token=auth_token)
        policyid=get_xiqpolicyId(apiurl=apiurl,polname=polname,authurl=authurl,auth_token=auth_token)
        logger.info(f"Policy id {policyid} will be associated with {deviceid} with serialno {serialno}")
        url=apiurl+"devices/"+str(deviceid)+"/network-policy?networkPolicyId="+str(policyid)
       
        response=requests.put(url,headers=headers)
        polstatusdict["serial_no"]=serialno
        polstatusdict["device_id"]=deviceid
        polstatusdict["policy_id"]=policyid
        polstatusdict["put_url"]=url
        polstatusdict["policy assignment status"]=response

    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
   
    if responseOK!=False:
        
        logger.debug(f"{polname} assigned to devices in {snsList}" )
        logger.info(polstatusdict)

    return responseOK

    # update policy


def post_xiqupdatepolicy(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, path="deployments",
                         snsList=[],imageupdate=False, auth_token="None"):
    url = apiurl + path
    polUpdateResponseJson = {}
    if imageupdate==False:
        poldict = {
            "devices": {
                "ids": [

                ]
            },
            "policy": {
                "enable_complete_configuration_update": "true"

            }
        }
    elif imageupdate==True:
        poldict = {
            "devices": {
                "ids": [

                ]
            },
            "policy": {
                "enable_complete_configuration_update": "true",
                "firmware_upgrade_policy": {
                "enable_enforce_upgrade": "true"
           
                },
                "firmware_activate_option": {
                "activation_delay_seconds": 60,
                }

            }
        }
        



    if auth_token == "None":
        logger.info("Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    for serialno in snsList:
        id = get_xiqDeviceId(apiurl=apiurl, authurl=authurl, sn=serialno, auth_token=auth_token,
                             xiquser=xiquser, xiqpass=xiqpass)
        poldict["devices"]["ids"].append(id)
        logger.info(f"Policy json is {poldict}")

    headers = {'accept': 'application/json', "Authorization": auth_token, }

    logger.info(f"Policy dictionary is {poldict}")
    
    response = requests.post(url, json=poldict, headers=headers)

    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.debug(f"policy update successfull")
        polUpdateResponseJson = response.json()

    return polUpdateResponseJson
 


def get_policyupdatestatus(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="deployments/status?deviceIds=",auth_token="None",sn=""):
    
    
    PolStatusInfo={}
    if auth_token=="None":
        logger.info("get_policyupdatestatus-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    
    devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=sn,auth_token=auth_token)
    
    url=apiurl+path+str(devid)
    logger.info(f"Update status post url {url}")
    headers={'accept': 'application/json',"Authorization": auth_token,}
    
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        
        logger.debug(f"policy update status info for device with {sn} is {response.json()}")
        
        PolStatusInfo=response.json()
    
    return PolStatusInfo

# Poll policy update status periodically for a given device IDs
#Start time- Inital sleep, increment time- periodic poll time, endtime- final time before returning failure

def CheckPolicyStatusPeriodic(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None",starttime=10,incrementtime=30,endtime=900):
    policyupdateStatus=False
    connecttime=starttime
    poll=True
    if auth_token=="None":
        logger.info("CheckPolicyStatusPeriodic-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=sn,auth_token=auth_token)
    logger.info(f"Sleeping for {starttime} before checking policy update status")
    time.sleep(starttime)

    while poll==True:
        
        
        polstatusInfoDict=get_policyupdatestatus(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="deployments/status?deviceIds=",auth_token=auth_token,sn=sn)
        


        if (polstatusInfoDict[str(devid)]['finished']== True) and (polstatusInfoDict[str(devid)]["is_finished_successful"]==True):
                               
                logger.info(f"Policy update for device with serial {sn} is successful")
                logger.info(f"Policy updated completed in {connecttime-starttime} seconds")
                poll=False
                policyupdateStatus=True
                break
                
        elif (connecttime >= endtime):
                logger.error(f"Policy did not update in {endtime} seconds.")
                logger.info(polstatusInfoDict)
                poll=False
                
                break
        else:
            logger.info(f"Time elapsed {connecttime} sec.Sleeping for {incrementtime} seconds before next poll")
            time.sleep(incrementtime)
            connecttime=connecttime+incrementtime
                

    return policyupdateStatus

def post_xiqRebootOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None",path="/devices/:reboot"):
    url=apiurl+path
    data = {"ids":[]}
    Rebooted=False
    if auth_token=="None":
        logger.info("CheckPolicyStatusPeriodic-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=sn,auth_token=auth_token)
        
    
        
    data["ids"].append(devid)
    logger.info("From post_xiqRebootOnboardDevices- Devices ID list:\t",data)
    
    
    logger.info("From post_xiqRebootOnboardDevices\t",data) 
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response = requests.post(url, json=data,headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)


    if responseOK!=False: 
        #print(auth_response.text)
        logger.info("Devices  Rebooted")

        Rebooted=True



    return  Rebooted
#Sends CLI to device, receivces response, splits the reponse based on newlines and checks lines for patterns.
#only single CLI in CLIList is supported currently- this is a API infra limitation for switching devices
def executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:cli",deviceType="exos",cliList=[],snsList=[],auth_token="None",checkList=[]):
    CheckValidCLiExecution=False
    if auth_token=="None":
        logger.info("CheckPolicyStatusPeriodic-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    devid=str(get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=snsList[0],auth_token=auth_token))

    cliresp={}
    cliExecTIme={}
    cliresp,cliExecTIme=xiqsendclitodevice(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:cli",deviceType="exos",cliList=cliList,snsList=snsList,auth_token=auth_token)
    logger.info(f"Cli response is {cliresp}")
    clioutput=cliresp['device_cli_outputs'][devid][0]['output']
    splitout=clioutput.split("\n")

    testList=[]

    for checkString in checkList:
        if checkString in clioutput:
            
            logger.info(f"{checkString} found in {cliList[0]}.")
            testList.append("True")
            
        else:
            logger.error(f"{checkString} not found in {cliList[0]}.")
            testList.append("False")
    
    if len(testList) == len(checkList) and  "False" not in testList :
        CheckValidCLiExecution=True
    else:
        CheckValidCLiExecution=False
            

    return CheckValidCLiExecution





        




if __name__=="__main__":
    print("In XIQ rest main")
    apiurl="https://g2-api.qa.xcloudiq.com/"
    xiquser="sasrinivasan+exosdt@extremenetworks.com"
    xiqpass="Aerohive123"
    authurl="https://g2-api.qa.xcloudiq.com/login"
    auth=xiqlogin(authurl=authurl,xiquser="sasrinivasan+exosdt@extremenetworks.com",xiqpass=xiqpass)
    print(auth)
  
