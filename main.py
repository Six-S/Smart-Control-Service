from govee_control import Govee

if __name__ == '__main__':
    Govee.log("INFO", "Running smart-control v0.1")

    deviceListResponse = Govee.makeRequest("devices")

    if deviceListResponse['code'] != 200:
        Govee.log("WARN", "Got {0} response code. Failed to fetch device list".format(deviceListResponse['code']))
        exit(1)

    Govee.setDeviceList(deviceListResponse)
    # print(response)