from pytest_testconfig import config
import logging as logger


#Function to get the attributes from the yaml file
def get_yaml_file_attributes():
    
    apiurl=config['xiq']['apiurl']
    xiquser=config['xiq']['xiquser']
    xiqpass=config['xiq']['xiqpass']
    authurl=config['xiq']['authurl']
    policy_name=config['policy']['name']
    iqagentversion=config['iqagent']['version']
    
    
    try:
        snsList=config['device']['snsList']
    except KeyError:
        logger.info("Serial undefined for device- Probably digital twin")
        snsList=["DIGITAL TWIN AUTOSERIAL"]

    try:
        dtisendpoint=config['dtis']['endpoint']
    except KeyError:
        logger.info("Endpoint only applicable for DT- Check testfile")
        dtisendpoint=""

    try:
        dtisauthtoken=config['dtis']['authtoken']
    except KeyError:
        logger.info("DTIS authtoken only applicable for DT- Check testfile")
        dtisauthtoken=""

    try:
        dtosver=config['dtis']['osver']
    except KeyError:
        logger.info("osver only applicable for DT- Check testfile")
        dtosver=""
    
    
    

    

    return apiurl,xiquser,xiqpass,authurl,snsList,policy_name,iqagentversion,dtisendpoint,dtisauthtoken,dtosver