import json
import requests
from datetime import datetime

class Govee():

    def __init__(self):
        self.apikey = None
        self.baseURL = "https://developer-api.govee.com/v1/"
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
        
        return json.load(jsonResponse)
    
    #Move this into a utils file.
    def log(level, msg):
        time = str(datetime.now())
        print("{0} [{1}] {2}".format(time, level, msg))
