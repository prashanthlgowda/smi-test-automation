# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Prashanth_L_Gowda
'''
import json
import unittest
import sys, os
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handlers.DiscoveryMicroservice import DiscoveryHandler
from utility.UtilBase import Utility


# import os
# import sys
# from scripts.SMI.utility.UtilBase import Utility
# from scripts.SMI.handlers.DiscoveryMicroservice import DiscoveryHandler
# run_dir=os.path.abspath(os.path.dirname(__file__))
# current_dir = os.getcwd()
# os.chdir(run_dir)
# sys.path.insert(0,os.path.abspath('../utility'))
# sys.path.append(os.path.abspath('../handlers'))

logger = logging.getLogger(__name__)
class DiscoveryMicroserviceTest(unittest.TestCase):
    


    def testDiscoveryEndpointIPSGlobalCredentialServer(self):
        try :
            
            x = 0;
            response = DiscoveryHandler().discoveryByIPS(x)
            logger.info("Response:" + response.text)
            responseJson = json.loads(response.text)
            requestData, url = DiscoveryHandler().getByIpsRequestData()
            requestIPAddress = requestData[x]["ips"]         
            # logger.info("Request IP Address: " + requestIPAddress[:])           
            for obj in responseJson:
                deviceGroup = obj["deviceGroup"]
                if deviceGroup == 'SERVER':
                    discoveredDeviceTypeList = obj["discoveredDeviceList"]
                    for deviceTypes in discoveredDeviceTypeList:
                        deviceName = deviceTypes["deviceName"]
                        discovered = deviceTypes["discovered"]
                        if deviceName == 'IDRAC8':
                            self.assertTrue(discovered >= 1, "NO IP Discovered")
                            deviceInfoList = deviceTypes["discoveredDeviceInfoList"]                        
                            for deviceInfo in deviceInfoList:
                                discoveredIP = deviceInfo["ipAddress"]
                                logger.info("Response IP Address after Discovery: " + discoveredIP)   
                                if discoveredIP in requestIPAddress :
                                    status = deviceInfo["status"]
                                    self.assertEqual(status, "SUCCESS", "Discovery status NOT success")                                            
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      
    
    def testDiscoveryEndpointIPSGlobalCredentialServerChassis(self):
        try :
            
            x = 1
            response = DiscoveryHandler().discoveryByIPS(x)
            logger.info("Response" + response.text)
            responseJson = json.loads(response.text)
            requestData, url = DiscoveryHandler().getByIpsRequestData()
            requestIPAddress = requestData[x]["ips"]         
            # logger.info("Request IP Address: " + requestIPAddress[:])           
            for obj in responseJson:
                deviceGroup = obj["deviceGroup"]
                if deviceGroup == 'SERVER' or deviceGroup == 'CHASSIS':
                    discoveredDeviceTypeList = obj["discoveredDeviceList"]
                    for deviceTypes in discoveredDeviceTypeList:
                        deviceName = deviceTypes["deviceName"]
                        discovered = deviceTypes["discovered"]
                        if deviceName == 'IDRAC8' or deviceName == 'CMC_FX2':
                            self.assertTrue(discovered >= 1, "NO IP Discovered")
                            deviceInfoList = deviceTypes["discoveredDeviceInfoList"]                        
                            for deviceInfo in deviceInfoList:
                                discoveredIP = deviceInfo["ipAddress"]
                                logger.info("Response IP Address after Discovery: " + discoveredIP)   
                                if discoveredIP in requestIPAddress :
                                    status = deviceInfo["status"]
                                    self.assertEqual(status, "SUCCESS", "Discovery status NOT success")                                            
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1   
        
    def testDiscoveryEndpointIPSDefaultCredentialServer(self):
        try :
            
            x = 2
            response = DiscoveryHandler().discoveryByIPS(x)
            logger.info("Response" + response.text)
            responseJson = json.loads(response.text)
            requestData, url = DiscoveryHandler().getByIpsRequestData()
            requestIPAddress = requestData[x]["ips"]         
            #logger.info("Request IP Address: " + requestIPAddress[0])           
            for obj in responseJson:
                deviceGroup = obj["deviceGroup"]
                if deviceGroup == 'SERVER':
                    discoveredDeviceTypeList = obj["discoveredDeviceList"]
                    for deviceTypes in discoveredDeviceTypeList:
                        deviceName = deviceTypes["deviceName"]
                        discovered = deviceTypes["discovered"]
                        if deviceName == 'IDRAC8':
                            self.assertTrue(discovered >= 1, "NO IP Discovered")
                            deviceInfoList = deviceTypes["discoveredDeviceInfoList"]                        
                            for deviceInfo in deviceInfoList:
                                discoveredIP = deviceInfo["ipAddress"]
                                logger.info("Response IP Address after Discovery: " + discoveredIP)   
                                if discoveredIP in requestIPAddress :
                                    status = deviceInfo["status"]
                                    self.assertEqual(status, "SUCCESS", "Discovery status NOT success")                                            
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1       
    
    
    
    def testDiscoveryEndpointRangeGlobalCredentialServerChassis(self):
        try :                                                
            x = 0
            response = DiscoveryHandler().discoveryByRange(x)
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)
            requestData, url = DiscoveryHandler().getByRangeRequestData()
            requestIPAddress = [requestData[x]["discoverIpRangeDeviceRequests"][0]["deviceStartIp"] , requestData[x]["discoverIpRangeDeviceRequests"][0]["deviceEndIp"]]           
            # logger.info("DiscoveryMicroserviceTest: testDiscoveryEndpointRange: Request IP Address: " + requestIPAddress[:])           
            for obj in responseJson:
                deviceGroup = obj["deviceGroup"]
                if deviceGroup == 'SERVER' or deviceGroup == 'CHASSIS':
                    discoveredDeviceTypeList = obj["discoveredDeviceList"]
                    for deviceTypes in discoveredDeviceTypeList:
                        deviceName = deviceTypes["deviceName"]
                        discovered = deviceTypes["discovered"]
                        if deviceName == 'IDRAC8' or deviceName == 'CMC_FX':
                            self.assertTrue(discovered >= 1, "NO IP Discovered")
                            deviceInfoList = deviceTypes["discoveredDeviceInfoList"]                        
                            for deviceInfo in deviceInfoList:
                                discoveredIP = deviceInfo["ipAddress"]
                                logger.info("Response IP Address after Discovery: " + discoveredIP)   
                                if discoveredIP in requestIPAddress :
                                    status = deviceInfo["status"]
                                    self.assertEqual(status, "SUCCESS", "Discovery status NOT success")                          
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1          
 
 
 
    def testDiscoveryEndpointRangeLocalCredentialServer(self):
        try :                                                
            x = 1
            response = DiscoveryHandler().discoveryByRange(x)
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)
            requestData, url = DiscoveryHandler().getByRangeRequestData()
            requestIPAddress = [requestData[x]["discoverIpRangeDeviceRequests"][0]["deviceStartIp"] , requestData[x]["discoverIpRangeDeviceRequests"][0]["deviceEndIp"]]           
            # logger.info("DiscoveryMicroserviceTest: testDiscoveryEndpointRange: Request IP Address: " + requestIPAddress[:])           
            for obj in responseJson:
                deviceGroup = obj["deviceGroup"]
                if deviceGroup == 'SERVER':
                    discoveredDeviceTypeList = obj["discoveredDeviceList"]
                    for deviceTypes in discoveredDeviceTypeList:
                        deviceName = deviceTypes["deviceName"]
                        discovered = deviceTypes["discovered"]
                        if deviceName == 'IDRAC8':
                            self.assertTrue(discovered >= 1, "NO IP Discovered")
                            deviceInfoList = deviceTypes["discoveredDeviceInfoList"]                        
                            for deviceInfo in deviceInfoList:
                                discoveredIP = deviceInfo["ipAddress"]
                                logger.info("Response IP Address after Discovery: " + discoveredIP)   
                                if discoveredIP in requestIPAddress :
                                    status = deviceInfo["status"]
                                    self.assertEqual(status, "SUCCESS", "Discovery status NOT success")   
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1         
    
    def testDiscoveryEndpointRangeDefaultCredentialChassis(self):
        try :                                                
            x =2
            response = DiscoveryHandler().discoveryByRange(x)
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)
            requestData, url = DiscoveryHandler().getByRangeRequestData()
            requestIPAddress = [requestData[x]["discoverIpRangeDeviceRequests"][0]["deviceStartIp"] , requestData[x]["discoverIpRangeDeviceRequests"][0]["deviceEndIp"]]           
            # logger.info("DiscoveryMicroserviceTest: testDiscoveryEndpointRange: Request IP Address: " + requestIPAddress[:])           
            for obj in responseJson:
                deviceGroup = obj["deviceGroup"]
                if deviceGroup == 'CHASSIS':
                    discoveredDeviceTypeList = obj["discoveredDeviceList"]
                    for deviceTypes in discoveredDeviceTypeList:
                        deviceName = deviceTypes["deviceName"]
                        discovered = deviceTypes["discovered"]
                        if deviceName == 'CMC_FX2':
                            self.assertTrue(discovered >= 1, "NO IP Discovered")
                            deviceInfoList = deviceTypes["discoveredDeviceInfoList"]                        
                            for deviceInfo in deviceInfoList:
                                discoveredIP = deviceInfo["ipAddress"]
                                logger.info("Response IP Address after Discovery: " + discoveredIP)   
                                if discoveredIP in requestIPAddress :
                                    status = deviceInfo["status"]
                                    self.assertEqual(status, "SUCCESS", "Discovery status NOT success")                                          
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1  
if __name__ == "__main__":
    if len(sys.argv) > 1:
        DiscoveryHandler.host = sys.argv.pop()
    else:
        DiscoveryHandler.host = "http://localhost:46002"
    from test_manager import run_tests
    run_tests('DISC')
