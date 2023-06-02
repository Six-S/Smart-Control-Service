import sys
import govee_control

if __name__ == '__main__':

    watch = True
    deviceList = None

    if len(sys.argv) > 1:
        if sys.argv[1] == "--watch":
            watch = True

    Govee = govee_control.Govee()

    Govee.log("INFO", "Running smart-control v0.1")

    deviceListResponse = Govee.makeRequest("devices")

    if deviceListResponse['code'] != 200:
        Govee.log("ERROR", "Got {0} response code. Failed to fetch device list".format(deviceListResponse['code']))
        exit(1)

    Govee.setDeviceList(deviceListResponse)

    Govee.listControllableDevices()

    try:
        while watch:
            device = input("Please select a device to control: ").lower()
            action = input("Please select the action to take: ").lower()
            argument = input("Please select the argument for the action, if applicable: ").lower()

            deviceList = Govee.getDeviceList()

            for d in deviceList:
                if device == d['deviceName'].lower():
                    if action in d['supportCmds']:
                        print({
                            "device": d['device'],
                            "model": d['model'],
                            "cmd": {
                                "name": action,
                                "value": argument
                            }
                        })
                        Govee.makeRequest('devices/control', {
                            "device": d['device'],
                            "model": d['model'],
                            "cmd": {
                                "name": action,
                                "value": argument
                            }
                        })

    except KeyboardInterrupt:
        Govee.log("INFO", "Quitting. Goodbye!")