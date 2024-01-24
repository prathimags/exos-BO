####################################################
# Author:Sathish Kumar Srinivasan
# Contact: sasrinivasan@extremenetworks.com
#
#
####################################################

import json 
import subprocess
import  logging as logger
import requests
import random,inspect
import time



from libs.xiqrestlib import *

endpoint=""
dtisauthtoken=''
osver=""

apiurl=""
xiquser=""
xiqpass=""
authurl=""


#Accepts string respone of gRPC call, trims other strings and returns json
def getresponsedict(call_result="",callresultstartkey="{",callresultendkey="Response trailers received"):
        logger.info(f"Call Response from get response dictionary>>>>> {call_result}")
        resp={}
        #Find begining and end of json resp
        startjson=call_result.find(callresultstartkey)
        endjson=call_result.find(callresultendkey)
        
          
        resp=call_result[startjson:endjson]

              
        return json.loads(resp)

#Get details of DT instance
def CreateDtInstance(params = {"owner_id": 4362, "mac_address": "00:A3:59:e8:40:00", "device_model": "5520-24T", "os_version": "31.5.0.324", "serial_number":"44956-12345","make":"SwitchEngine"},servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/CreateDtInstance',dtisauthtoken=dtisauthtoken):
    
    resp={}
    try:
        call_result = subprocess.check_output(['grpcurl', '-format-error', '-vv','-insecure','-H', dtisauthtoken, '-d', json.dumps(params), servsock, stub])
        #Response is bytestrem- decode to str
        logger.info(call_result)
        resp=getresponsedict(call_result.decode())
        
    except subprocess.CalledProcessError as e:
        logger.error(e.returncode)
        logger.error(e.output)
        resp["Error code"]=str(e.returncode)
        resp["Error"] = str(e.output)
        logger.error(resp)

    
    return resp

#Get details of DT instance
def GetDtInstance(params = {"owner_id": 4362, "instance_ids":559},servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/GetDtInstance',dtisauthtoken=dtisauthtoken):
    
    resp={}
    try:
        call_result = subprocess.check_output(['grpcurl', '-format-error', '-vv','-insecure','-H', dtisauthtoken, '-d', json.dumps(params), servsock, stub])
        #Response is bytestrem- decode to str
        resp=getresponsedict(call_result.decode())
        logger.info("GetDTInstance>>>>>>>>>>> resp")
        
    except subprocess.CalledProcessError as e:
        logger.error(e.returncode)
        logger.error(e.output)
        resp["Error code"]=str(e.returncode)
        resp["Error"] = str(e.output)
        logger.error(resp)
    
    return resp

#List DT instances for owner
def ListDtInstances(params = {"owner_id": 92689, "page":0, "limit": 100},servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/ListDtInstances',dtisauthtoken=dtisauthtoken):
    
    resp={}
    try:
        call_result = subprocess.check_output(['grpcurl', '-format-error', '-vv','-insecure','-H', dtisauthtoken, '-d', json.dumps(params), servsock, stub])
        #Response is bytestrem- decode to str
        resp=getresponsedict(call_result.decode())
        
    except subprocess.CalledProcessError as e:
        logger.error(e.returncode)
        logger.error(e.output)
        resp["Error code"]=str(e.returncode)
        resp["Error"] = str(e.output)
        logger.error(resp)
    
    return resp

#22R5 shutdown DT instance

def ShutdownDtInstances(params = {"owner_id": 4362, "instance_ids":[559]},servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/ShutdownDtInstances',dtisauthtoken=dtisauthtoken ):
    
    resp={}
    
    try:
        call_result = subprocess.check_output(['grpcurl', '-format-error', '-vv','-insecure','-H', dtisauthtoken, '-d', json.dumps(params), servsock, stub])
        logger.info(call_result)
        #Response is bytestrem- decode to str
        resp=getresponsedict(call_result.decode())
        logger.info(f"Shutdown Response is >>>>>>>>>>>>{resp}")

       
    except subprocess.CalledProcessError as e:
        logger.error(e.returncode)
        logger.error(e.output)
        resp["Error code"]=str(e.returncode)
        resp["Error"] = str(e.output)
        logger.error(resp)

    
    
    return resp

#22R5 relaunch DT instance

def RelaunchDtInstance(params = {"owner_id": 4362, "instance_ids":[1001]},servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/RelaunchDtInstances',dtisauthtoken=dtisauthtoken,starttime=5,incrementtime=5,endtime=150):
    
    relaunchresp={}
    try:
        call_result = subprocess.check_output(['grpcurl', '-format-error', '-vv','-insecure','-H', dtisauthtoken, '-d', json.dumps(params), servsock, stub])
        #Response is bytestrem- decode to str
        logger.info(call_result)
        relaunchresp=getresponsedict(call_result.decode())
        logger.info(f"Relaunch Response is >>>>>>>>>>>>{relaunchresp}")

        if relaunchresp:
            dtupstatus=False
            connecttime=starttime
            viq_id=params["owner_id"]
            instance_id=params["instance_ids"][0]

            poll=True
            while poll==True:
                getdtresp=GetDtInstance(params = {"owner_id": viq_id, "instance_ids": [instance_id]},dtisauthtoken=dtisauthtoken,servsock=servsock)
                logger.info(getdtresp)
                if (getdtresp["dt_instances"][0]["gns3_status"]== "GNS3_STATUS_RUNNING") and (getdtresp["dt_instances"][0]["node_status"]== "started"):
                    logger.info(f"DT with ownerID {viq_id} and instance ID {instance_id} relaunched successfully")
                    poll=False
                    dtupstatus=True
                    break
                elif (connecttime >= endtime):
                        logger.info(f"Relaunch of DT with ownerID {viq_id} and instance ID {instance_id} failed after {endtime} seconds")
                        logger.info(f"Response from DTIS is {getdtresp}")
                        poll=False
                        break
                else:
                    logger.info(f"Time elapsed {connecttime} sec.Sleeping for {incrementtime} seconds before polling DTIS")
                    time.sleep(incrementtime)
                    connecttime=connecttime+incrementtime

        
    except subprocess.CalledProcessError as e:
        logger.error(e.returncode)
        logger.error(e.output)
        relaunchresp["Error code"]=str(e.returncode)
        relaunchresp["Error"] = str(e.output)
        logger.error(relaunchresp)

    
    return dtupstatus,relaunchresp



#Delete Dt instance
def DeleteDtInstance(params = {"owner_id": 4362, "instance_id":559},servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/DeleteDtInstance',dtisauthtoken=dtisauthtoken):
    
    resp={}
    
    try:
        call_result = subprocess.check_output(['grpcurl', '-format-error', '-vv','-insecure','-H', dtisauthtoken, '-d', json.dumps(params), servsock, stub])
        logger.info(call_result)
        #Response is bytestrem- decode to str
        resp=getresponsedict(call_result.decode())
        logger.info(f"Delete Response is >>>>>>>>>>>>{resp}")
        #Check if response is empty
        if not resp:
            resp={"Delete successful":params}
    except subprocess.CalledProcessError as e:
        logger.error(e.returncode)
        logger.error(e.output)
        resp["Error code"]=str(e.returncode)
        resp["Error"] = str(e.output)
        logger.error(resp)
    
    return resp
#Cleanup all running DT instances given a owner ID
def CleanupDtInstances(params = {"owner_id": 21652, "page":0, "limit": 100},servsock=endpoint,dtisauthtoken=dtisauthtoken):
    
    dtinstancelist=ListDtInstances(params=params,servsock=endpoint,dtisauthtoken=dtisauthtoken)
   
    instances=dtinstancelist["dt_instances"]
    cleanedupList=[]
    for instance in instances:
        
        
        if instance["gns3_status"]=="GNS3_STATUS_RUNNING":
            logger.info(instance)
            logger.info(instance["instance_id"])
           
            deleteresp=DeleteDtInstance({"owner_id": params["owner_id"], "instance_id":instance["instance_id"]},servsock=endpoint,dtisauthtoken=dtisauthtoken)
            cleanedupList.append(deleteresp)
    return cleanedupList

#Generate mac and serial for create DT gRPC call
def GenMacSerial(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token="None",model="5520-24T",serlen=16,macseed="00:0A"):
    viqinfo={}
    viqinfo=get_xiqviqinfo(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    ownerid=viqinfo['owner_id']
    viqstr=str(ownerid)
    viqlen=len(viqstr)
    padding=""
    serpadding=""

    if viqlen < 5:
        serpadding="0"

    generatedSerial=viqstr+serpadding+"-"+str(random.randint(10000,99999))
    #generatedSerial=str(viqstr[:2])+"-"+str(viqstr[2:5])+str(random.randint(100,999))
    
    generatedMac=macseed+":"+str(viqstr[:2])+":"+str(viqstr[2:4])+":"+str(random.randint(11,63))+":"+"00"
 
    onboardingSerial=generatedSerial


    return generatedSerial,generatedMac,onboardingSerial,ownerid

def CreatedtandGetStatus(servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/CreateDtInstance',starttime=5,incrementtime=5,endtime=150,apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token="None",model="5520-24T",macseed="00:0A",dtisauthtoken=dtisauthtoken,osver=osver,endpoint=endpoint,make="EXOS"):

    
    genserial,generatedmac,onboardserial,ownerid=GenMacSerial(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token="None",model=model,serlen=16,macseed="00:0A")
    createresp=CreateDtInstance(params = {"owner_id": ownerid, "mac_address": generatedmac, "device_model": model, "os_version": osver, "serial_number":genserial,"make":make},servsock=endpoint,stub='extremecloudiq.dtis.v1.DtInstanceService/CreateDtInstance',dtisauthtoken=dtisauthtoken)
    instanceid=createresp["instance"]["instance_id"]
    
    dtupstatus=False
    connecttime=starttime
    poll=True
    while poll==True:
        getdtresp=GetDtInstance(params = {"owner_id": ownerid, "instance_ids":[createresp["instance"]["instance_id"]]},dtisauthtoken=dtisauthtoken,servsock=endpoint)
        logger.info(getdtresp)
        if (getdtresp["dt_instances"][0]["gns3_status"]== "GNS3_STATUS_RUNNING") and (getdtresp["dt_instances"][0]["node_status"]== "started"):
            logger.info(f"DT instance of type {model} with serial {genserial} mac {generatedmac} and {ownerid} started successfully")
            poll=False
            dtupstatus=True
            break
        elif (connecttime >= endtime):
                logger.info(f"Creation of DTInstance of type {model} with serial {genserial} mac {generatedmac} and {ownerid} failed after {endtime} seconds")
                logger.info(f"Response from DTIS is {getdtresp}")
                poll=False
                break
        else:
            logger.info(f"Time elapsed {connecttime} sec.Sleeping for {incrementtime} seconds before polling DTIS")
            time.sleep(incrementtime)
            connecttime=connecttime+incrementtime
    return dtupstatus,onboardserial,generatedmac,instanceid,ownerid
        



       



if __name__=="__main__":
    logger.info("In dtislib main")
    

    