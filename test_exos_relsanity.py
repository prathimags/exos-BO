
import time
import sys
import logging
sys.path.append("..")
from libs.xiqrestlib import *
from libs.st_common_lib import *

apiurl,xiquser,xiqpass,authurl,snsList,policy_name,iqagentversion, dtisendpoint,dtisauthtoken,dtosver = get_yaml_file_attributes()



logger= logging.getLogger()
#This is required for pytest logging- default loglevel is warn
logger.setLevel(logging.INFO)

#generate JWT token
auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
logger.info(f"Auth JWT token to be passed is {auth_token}")

#Verify onboarding
def test_onboard_devices():
    #Onboard device
    onboarded=post_xiqOnboardDevices(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,snsList=snsList,auth_token=auth_token)
    logger.info (f"{snsList} with Onboarded Successfully")
    if not onboarded:
        logger.error("One of device from {snsList} not onboarded. Check logs")   

    assert onboarded





#Check device status changes to managed
def test_check_device_status():

    mangeddevices=0
    for sn in snsList:
        deviceStatus = CheckDeviceStatusPeriodic(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, sn=sn, auth_token="None", starttime=30, incrementtime=30, endtime=1600)
        logger.info(f"Device Status: {deviceStatus}")
        if (deviceStatus == "MANAGED"):
            mangeddevices=mangeddevices+1
        else:
            logger.error(f"Device with {sn} did not change to managed state")
    
    logger.info(f"Number of devices in managed state {mangeddevices}. Total onboarded devices {len(snsList)}")
    
    if (mangeddevices == len(snsList)):
        assert True
    else:
        assert False
#verify policy assignment is successfull
def test_assign_policy():
    polname=policy_name
    putresponse = put_xiqpoldevice(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, snsList=snsList, polname=polname, auth_token=auth_token)
    
    
    logger.info (f"Devices with serial numbers {snsList} associated with policy {polname}")


    if putresponse!=False:
        logger.info(f"Policy with name {polname} assigned to devices with serial numbers {snsList}")
        
        assert True
    else:
        logger.info(f"Policy with name {polname} assignment failed for one of the devices")
        assert False

#Update policy
def test_update_policy_image_and_checkstatus():
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

def test_check_iqagent_Version():
    checkiqagent=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show iqagent"],snsList=snsList,auth_token=auth_token,checkList=[iqagentversion,"Last Health Status                  SUCCESS","Last Poll Status                    SUCCESS"])

    if checkiqagent==True:
        logger.info(f"{iqagentversion} found in output of show iqagent")
        assert True
    else:
        logger.error(f"{iqagentversion} not found in output of show iqagent")
        assert False

def test_check_switchengine_Version():

    swversion="32.6.2.68"
    checkswver=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show version"],snsList=snsList,auth_token=auth_token,checkList=[swversion])

    if checkswver==True:
        logger.info(f"{swversion} found in output of show version")
        assert True
    else:
        logger.error(f"{swversion} not found in output of show version")
        assert False

def test_check_vlan():
    checkvlan=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show vlan"],snsList=snsList,auth_token=auth_token,checkList=["VLAN_0002","VLAN_0003","VLAN_0004","VLAN_0005","VLAN_0006","VLAN_0007","VLAN_0008","VLAN_0009","VLAN_0010","VLAN_0011","VLAN_0012","VLAN_0013","VLAN_0014","VLAN_0015","VLAN_0016","VLAN_0017","VLAN_0018","VLAN_0019","VLAN_0020","api_v1001","api_v1002","api_v1003","api_v1004","api_v1005","api_v1006","api_v1007","api_v1008","api_v1009","api_v1010"])

    if checkvlan==True:
        
        assert True
    else:
        
        assert False

# Verify ipv4 and ipv6 config present
def test_check_ipv4():
    checkipv4=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show iproute ipv4 origin direct"],snsList=snsList,auth_token=auth_token,checkList=["8.8.1.1","8.8.2.1","8.8.3.1","8.8.4.1","8.8.5.1","8.8.6.1","8.8.7.1","8.8.8.1","8.8.9.1","8.8.10.1"])

    if checkipv4==True:
        
        assert True
    else:
        
        assert False

# Verify ipv4 and ipv6 config present
def test_check_ipv6():
    checkipv6=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show iproute ipv6 origin direct"],snsList=snsList,auth_token=auth_token,checkList=["2008:1::1","2008:2::","2008:3::1","2008:4::1","2008:5::1","2008:6::1","2008:7::1","2008:8::1","2008:9::/64","2008:a::/64"])

    if checkipv6==True:
        
        assert True
    else:
        
        assert False

'''
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

'''
'''
#Reboot device
def test_rebootdevice():
    sn=snsList[0]
    rebooted=post_xiqRebootOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn=sn,auth_token="None",path="/devices/:reboot")
    if rebooted==True:
        logger.info(f"Device with serial {sn} rebooted")
        assert True
    else:
        logger.info(f"Device with serial {sn} cannot be rebooted")
        assert False'''
