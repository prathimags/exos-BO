from statistics import mode
import time
import sys


sys.path.append("..")

from libs.xiqrestlib import *
from libs.st_common_lib import *
from libs.dtislib import *

logger= logging.getLogger()
#This is required for pytest logging- default loglevel is warn
logger.setLevel(logging.INFO)





apiurl,xiquser,xiqpass,authurl,snsList,policy_name,iqagentversion,dtisendpoint,dtisauthtoken,dtosver = get_yaml_file_attributes()


dtinstanceid=""


snsList=[]
viqinstance=""
instanceid=""
generatedonboardser=""
generatedonboardmac=""
devicemodel=""

auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
logger.info(f"Auth JWT token to be passed is {auth_token}")


#create DT instance 
def test_createDtInstance(model):
    global snsList
    global viqinstance
    global instanceid
    global generatedonboardser
    global generatedonboardmac
    global devicemodel
    devicemodel=model
    dtupstatus,generatedonboardser,generatedonboardmac,instanceid,ownerid=CreatedtandGetStatus(servsock=endpoint,apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token,model=model,dtisauthtoken=dtisauthtoken,endpoint=dtisendpoint,osver=dtosver,make="SwitchEngine")
    logger.info(f"Digital twin status {dtupstatus} and generated onboardserial={generatedonboardser}")
    if dtupstatus==True:
        logger.info(f"Created successfully- DT Instance of type {model} with exos ver {osver} and serial {snsList}.Onboarding serial is {generatedonboardser}")
        logger.info(f"VIQ ID Is {ownerid} for user {xiqlogin}")
        onboardserial=generatedonboardser
        snsList.append(onboardserial)
        viqinstance=ownerid
        assert True
    elif dtupstatus==False:
        logger.error(f"Creation failed- DT Instance of type {model} with exos ver {osver} and serial {snsList}")
        assert False
        onboardserial=""
        

#Verify onboarding
def test_onboard_devices():
    global snsList
    global viqinstance

    #Attempt onboarding only if create DT is successfull and snsList contains atleast 1
    if len(snsList) > 0:
        #Onboard device
        onboarded=post_xiqOnboardDevices(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,snsList=snsList,auth_token=auth_token)
        logger.info (f"{snsList} with Onboarded Successfully")
        if not onboarded:
            logger.error(f"One of device from {snsList} not onboarded. Check logs")


    assert onboarded
'''
#verify license is not consumed for DT
#See XIQ-5864

def test_checklicenseconsumption():
    viqinfo={}
    viqinfo=get_xiqviqinfo(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token)
    logger.info(viqinfo)
    avl_license=(viqinfo["licenses"][0]["available"])
    logger.info(f"Available device licenses in {xiqlogin} is {avl_license}")

    consumed_license=(viqinfo["licenses"][0]["activated"])

    logger.info(f"Consumed device licenses in {xiqlogin} is {consumed_license}")
    
    if consumed_license == 0:
        logger.info(f"DT instnace did not consume any license as expected")
        assert True
    else:
        logger.info(f"DT instance consumed licenses")
        assert False
'''
#Check device status changes to managed
def test_check_device_status():
    global snsList
    global viqinstance

    mangeddevices=0
    logger.info(f"Checking serial {snsList} status")
    for sn in snsList:
        deviceStatus = CheckDeviceStatusPeriodic(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, sn=sn, auth_token=auth_token, starttime=30, incrementtime=30, endtime=300)
        logger.info(f"Device Status: {deviceStatus}")
        if (deviceStatus == "MANAGED"):
            mangeddevices=mangeddevices+1
        else:
            logger.error(f"Device with {sn} did not change to managed state")
    
    logger.info(f"Number of devices in managed state {mangeddevices}. Total onboarded devices {len(snsList)}")
    
    if (mangeddevices == len(snsList)) and len(snsList) > 0:
        assert True
    else:
        assert False

#Check IQagent is upgraded

def test_check_iqagent_Version():
    checkiqagent=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show iqagent"],snsList=snsList,auth_token=auth_token,checkList=[iqagentversion,"Last Health Status                  SUCCESS","Last Poll Status                    SUCCESS"])

    if checkiqagent==True:
        logger.info(f"{iqagentversion} found in output of show iqagent")
        assert True
    else:
        logger.error(f"{iqagentversion} not found in output of show iqagent")
        assert False

#verify policy assignment is successfull
def test_assign_policy():
    polname=policy_name
    putresponse = put_xiqpoldevice(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, snsList=snsList,
                                     polname=polname, auth_token=auth_token)
    
    
    logger.info (f"Devices with serial numbers {snsList} associated with policy {polname}")

    if putresponse!=False:
        logger.info(f"Policy with name {polname} assigned to devices with serial numbers {snsList}")
        
        assert True
    else:
        logger.info(f"Policy with name {polname} assignment failed for one of the devices")
        assert False
#Update policy and check if update was successfull
def test_update_policy_and_checkstatus():
    global snsList
    global viqinstance
    polrespjson = post_xiqupdatepolicy(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, snsList=snsList,imageupdate=False,auth_token=auth_token)
    logger.info("Policy update json")
    logger.info(polrespjson)
    polStatusdict={}

    for sn in snsList:
   
        policyupdatestatus=CheckPolicyStatusPeriodic(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn=sn,auth_token=auth_token,starttime=30,incrementtime=30,endtime=600)
        
        polStatusdict[sn]=policyupdatestatus
    
    if False not in polStatusdict.values():
        logger.info(f"Policy and/or images updated successfully for serials {snsList}. Update status:{polStatusdict}")
        assert True
    else:
        logger.error(f"Policy and/or image update failed for one of the devices.{polStatusdict} ")
        assert False


def test_check_switchengine_Version():
    global snsList
    global viqinstance
    swversion=dtosver
    checkswver=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show version"],snsList=snsList,auth_token=auth_token,checkList=[swversion])

    if checkswver==True:
        logger.info(f"{swversion} found in output of show version")
        assert True
    else:
        logger.error(f"{swversion} not found in output of show version")
        assert False

def test_check_universal_switch_sku(model):
    global snsList
    global viqinstance
    
    checkswver=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show switch"],snsList=snsList,auth_token=auth_token,checkList=[model])

    if checkswver==True:
        logger.info(f"{model} found in output of show switch")
        assert True
    else:
        logger.error(f"{model} not found in output of show switch")
        assert False


def test_check_vlan():
    checkvlan=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show vlan"],snsList=snsList,auth_token=auth_token,checkList=["VLAN_0002","VLAN_0020"])

    if checkvlan==True:
        
        assert True
        logger.info(f"VLANs configured from XIQ policy found in output of show vlan")
    else:
        
        assert False
        logger.error(f"Vlans configured from XIQ policy missing in output of show vlan")

def test_shutdowndtInstance():
    global viqinstance
    global instanceid
    shutdownResp={}
    shutdownResp=ShutdownDtInstances({"owner_id": viqinstance, "instance_ids":[instanceid]},servsock=dtisendpoint,dtisauthtoken=dtisauthtoken)
    
    #Check if shutdown response is empty-implying success
    if not shutdownResp:
        time.sleep(7)
        getdtresp=GetDtInstance({"owner_id": viqinstance, "instance_ids":[instanceid]},dtisauthtoken=dtisauthtoken,servsock=dtisendpoint)
        logger.info(f"Shutdown DT status>>{getdtresp}")
        if (getdtresp["dt_instances"][0]["gns3_status"]== "GNS3_STATUS_SHUTDOWN"):
            logger.info(f"DT instance with {instanceid} Shutdown successfully")
            assert True

    else:
        logger.error(f"Unable to Shutdown instance with instance id {instanceid}")
        assert False

    
def test_relaunchdtInstance():
    global viqinstance
    global instanceid
    global generatedonboardser
    global generatedonboardmac
    global devicemodel
    relaunchResp={}
    #relaunchResp=RelaunchDtInstance({"owner_id": viqinstance, "mac_address": generatedonboardmac, "device_model": devicemodel, "os_version": dtosver, "serial_number":generatedonboardser,"make":"SwitchEngine"},servsock=dtisendpoint,dtisauthtoken=dtisauthtoken)
    dtupstatus,relaunchResp=RelaunchDtInstance({"owner_id": viqinstance,"instance_ids": [instanceid] },servsock=dtisendpoint,dtisauthtoken=dtisauthtoken)
    
    if dtupstatus:
        logger.info(f"DT instance with {instanceid} relaunched successfully")
        assert True
    else:
        logger.error(f"Unable to relaunch instance with instance id {instanceid}")
        assert False

#verify previously pushed config is persistant after relaunch

def test_check_configpersistance():
    #To prevent http 504 ngix error when calling CLI XAPI immediately after relaunch add sleep
    #ERROR    root:xiqrestlib.py:43 Unexpected response from REST server- Response  is {"error_code":"UNAVAILABLE","error_id":"821289490e0346258df3d69c91977132","error_message":"UNAVAILABLE: HTTP status code 504\ninvalid content-type: text/html\nheaders: Metadata(:status=504,server=nginx/1.20.2,date=Tue, 12 Jul 2022 04:44:34 GMT,content-type=text/html,content-length=167)\nDATA-----------------------------\n<html>\r\n<head><title>504 Gateway Time-out</title></head>\r\n<body>\r\n<center><h1>504 Gateway Time-out</h1></center>\r\n<hr><center>nginx/1.20.2</center>\r\n</body>\r\n</html>

    time.sleep(20)
    checkvlan=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show vlan"],snsList=snsList,auth_token=auth_token,checkList=["VLAN_0002","VLAN_0020"])

    if checkvlan==True:
        
        assert True
        logger.info(f"VLANs configured from XIQ policy found in output of show vlan-Config persisted after re-launch")
    else:
        
        assert False
        logger.error(f"Vlans configured from XIQ policy missing in output of show vlan-Config Peristance failed")
    
    

def test_deletedevicefromxiq():
    deletefromxiq=post_xiqDelOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:delete",snsList=snsList,auth_token=auth_token)

    if deletefromxiq==True:
        assert True
        logger.info(f"Device with serial {snsList} deleted from XIQ")
    else:
        assert False
        logger.error(f"Removal of device with serial {snsList} from XIQ failed")

def test_deletedt():
    global viqinstance
    global instanceid
    deleteresp={""}
    deleteresp=DeleteDtInstance({"owner_id": viqinstance, "instance_id":instanceid},servsock=dtisendpoint,dtisauthtoken=dtisauthtoken)
    logger.info(deleteresp)
    if deleteresp["Delete successful"]["instance_id"]==str(instanceid):
        logger.info(f"DT instance with {instanceid} deleted successfully")

        assert True
    else:
        logger.error(f"Unable to delete instance with instance id {instanceid}")
        assert False




