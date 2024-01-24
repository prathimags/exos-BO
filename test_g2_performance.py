
import time
import sys
import logging
sys.path.append("..")
from libs.xiqrestlib import *
from libs.st_common_lib import *


apiurl,xiquser,xiqpass,authurl,snsList,policy_name,iqagentversion, dtisendpoint,dtisauthtoken,dtosver = get_yaml_file_attributes()

#snsList=["2008G-01292"]

endvlan="VLAN_0999"

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
    putresponse = put_xiqpoldevice(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, snsList=snsList,
                                     polname=polname, auth_token=auth_token)
    
    
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
   
        policyupdatestatus=CheckPolicyStatusPeriodic(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn=sn,auth_token=auth_token,starttime=30,incrementtime=15,endtime=1000)
        
        polStatusdict[sn]=policyupdatestatus
    
    if False not in polStatusdict.values():
        logger.info(f"Policy and/or images updated successfully for serials {snsList}. Update status:{polStatusdict}")
        assert True
    else:
        logger.error(f"Policy and/or image update failed for one of the devices.{polStatusdict} ")
        assert False


def test_check_vlan():
    checkvlan=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show vlan"],snsList=snsList,auth_token=auth_token,checkList=["VLAN_0002",endvlan])

    if checkvlan==True:
        
        assert True
    else:
        
        assert False
        
def test_check_memory():
    checkmemory=executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,cliList=["show memory process vlan"],snsList=snsList,auth_token=auth_token,checkList=["Total DRAM","vlan"])

    if checkmemory==True:
        
        assert True
    else:
        
        assert False
