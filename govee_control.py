import requests
from datetime import datetime

class Govee():

    def __init__(self):
        self.apikey = ""
        self.baseURL = "https://developer-api.govee.com/v1/"
        self.deviceList = {}
        self.legalActions = {
            "devices": {
                "headers": {
                    "Govee-API-Key": self.apikey
                },
                "type": "GET"
            },
            "devices/control": {
                "headers": {
                    "content-type" : "application/json",
                    "Govee-API-Key": self.apikey
                },
                "type": "PUT"
            },
            "devices/state": {
                "headers": {
                    "content-type" : "application/json",
                    "Govee-API-Key": self.apikey
                },
                "type": "GET"
            }
        }
    
    def toggleDeviceState(self, device, cmd, options=None):

        if not device or type(device) != dict:
            self.log("ERROR", "Unable to toggle device state. Device argument does not exist or is not a dict.")
            return
        
        if not cmd:
            self.log("ERROR", "Unable to toggle device state. No new state to toggle to.")
            return

        if cmd not in device['supportCmds']:
            self.log("ERROR", "Unable to toggle device state. Illegal command.")
        
        if not device['controllable']:
            self.log("ERROR", "Unable to toggle device state. Device cannot be controlled via API.")
        
        
    
    def setDeviceList(self, deviceObject):
        self.log("INFO", "Setting new device list")
        self.deviceList = deviceObject['data']['devices']
        return self.deviceList

    def makeRequest(self, action, body=None):

        if not action:
            self.log("ERROR", "Unable to make an API request without an action.")
            return False
        
        if action not in self.legalActions.keys():
            self.log("ERROR", "Illegal action: {0}".format(action))
            return False
        
        try:
            if self.legalActions[action]["type"] == "GET":
                jsonResponse = requests.get(self.baseURL + action, headers=self.legalActions[action]["headers"])
            else:
                if not body:
                    self.log("ERROR", "Unable to POST without a request body.")

                jsonResponse = requests.post(self.baseURL + action, headers=self.legalActions[action]["headers"], data=body)
        except Exception as error:
            self.log("ERROR", "Unable to complete request due to the following error: {0}".format(error))
            return False
        
        return jsonResponse.json()
    
    #Move this into a utils file.
    def log(self, level, msg):
        time = str(datetime.now())
        print("{0} [{1}] {2}".format(time, level, msg))
