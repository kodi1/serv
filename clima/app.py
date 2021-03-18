#!/usr/bin/env python3
# author(s):
__author__ = "William van Beek"
__copyright__ = ""
__credits__ = ["William van Beek"]
__license__ = "GPL-3.0-only"
__version__ = "1.2"
__maintainer__ = "William van Beek"
__email__ = ""
__status__ = "Testing"

import paho.mqtt.client as mqtt
import time, os, sys, yaml, json
from dohpc import dohpc

#####
# This is a work in progress, as it needs to be rewritten to the new style.
#####

class dohpcmqtt():

    def __init__(self, config_file):
        self.config = ""
        self.config_file = config_file
        self._read_config(self.config_file)
        self._reconect = 0
        # Update to the latest data in the yml file.
        daikin_heat_pump = dohpc(self.config_file)

        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            #print("Connected with result code "+str(rc))
            client.subscribe(
                [
                    ("DHPW/json", 2),
                    ("DHPW/setpower/1", 2),
                    ("DHPW/setpower/2", 2)
                ]
            )
            client.publish("DHPW/LWT", "Online", 1, True)
            client.connected_flag = True

        def push_data():
            try:
                daikin_heat_pump.UpdateValeus
            except:
                print("error exception in dohpc get")
                self._reconect += 1
                pass

            # Read YML file again
            self._read_config(self.config_file)

            client.publish("DHPW/WarningState", self.config["p1_p2_devices"][1]["unitstatusData"]["WarningState"])
            client.publish("DHPW/LeavingWaterTemperatureCurrent", self.config["p1_p2_devices"][1]["sensorData"]["LeavingWaterTemperatureCurrent"])
            client.publish("DHPW/OutdoorTemperature", self.config["p1_p2_devices"][1]["sensorData"]["OutdoorTemperature"])
            client.publish("DHPW/OperatingMode", self.config["p1_p2_devices"][1]["OperationData"]["OperationMode"])
            client.publish("DHPW/LeavingWaterTemperatureAuto", self.config["p1_p2_devices"][1]["OperationData"]["LeavingWaterTemperatureAuto"])
            client.publish("DHPW/DomesticHotWaterTemperatureHeating", self.config["p1_p2_devices"][2]["OperationData"]["DomesticHotWaterTemperatureHeating"])
            client.publish("DHPW/TankTemperature", self.config["p1_p2_devices"][2]["sensorData"]["TankTemperature"])
            client.publish("DHPW/power/1", self.config["p1_p2_devices"][1]["OperationData"]["Power"])
            client.publish("DHPW/power/2", self.config["p1_p2_devices"][2]["OperationData"]["Power"])

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, message):
            if self.config['basics']['debug'] == True:
                print("topic: %s\nmsg: %s" % (message.topic, message.payload.decode("utf-8")))
            if message.topic == "DHPW/json":
                try:
                    data = json.loads(message.payload.decode("utf-8"))
                except ValueError:
                    print("wrong json payload")
                    pass

            elif message.topic == "DHPW/setpower/1":
                data = {
                            "key": "1",
                            "subject": "Power",
                            "msg": message.payload.decode("utf-8").lower()
                        }
            elif message.topic == "DHPW/setpower/2":
                data = {
                            "key": "2",
                            "subject": "Power",
                            "msg": message.payload.decode("utf-8").lower()
                        }
            #elif message.topic == "DHPW/RecvUpdateSchedule":
            #    SH.sendHPvalues("S", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
            #elif message.topic == "DHPW/RecvChangeSchedule":
            #    SH.sendHPvalues("I", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
            else:
                pass

            try:
                daikin_heat_pump.ChangeTemp(data["key"], data["subject"], data["msg"])
            except:
                print("error exception in dohpc set")
                self._reconect += 1
                pass

            time.sleep(0.3)
            push_data()

        start_program = True
        times_send = 0
        client = mqtt.Client("DHPW")
        client.connected_flag = False
        client.on_connect = on_connect
        client.on_message = on_message
        client.will_set("DHPW/LWT", "Offline", 1, True)
        client.username_pw_set(self.config["mqtt"]["user"], self.config["mqtt"]["pass"])
        client.connect(self.config["mqtt"]["broker"], port=1883, keepalive=60)

        # Start the loop, and wait for a connection
        client.loop_start()
        while client.connected_flag == False:
            if self.config['basics']['debug'] == True:
                print("We are not yet connected, please hold (2)")
            time.sleep(2)

        # Here we enter a while loop that can be terminated with a new file (graceful) or a key stroke (non graceful)
        try:
            while not os.path.exists(self.config["mqtt"]["exit_file"]):

                if self.config['basics']['debug'] == True:
                    print("Reading data")

                push_data()
                if self.config['basics']['debug'] == True:
                    print("Data read")

                if times_send == int(self.config["mqtt"]["data_timeout"]) or start_program == True:
                    # reset counter
                    times_send = 0
                    start_program = False

                    client.publish("DHPW/ErrorState", self.config["p1_p2_devices"][1]["unitstatusData"]["ErrorState"])
                    client.publish("DHPW/WarningState", self.config["p1_p2_devices"][1]["unitstatusData"]["WarningState"])
                    client.publish("DHPW/EmergencyState", self.config["p1_p2_devices"][1]["unitstatusData"]["EmergencyState"])

                if self.config['basics']['debug'] == True:
                    print("post data")
                # recieving data always runs on the background
                # Sleep for the spefified amount of time by the user
                time.sleep(int(self.config["mqtt"]["temp_timeout"]))
                times_send = times_send + 1

                if self._reconect > 3:
                    self._reconect = 0
                    del daikin_heat_pump
                    daikin_heat_pump = dohpc(self.config_file)
                    print("error exception in dohpc resart conection")

        except KeyboardInterrupt:
            print(" I was brutally interrupted, tis but a scratch!")

        # We reached the end, we can stop the loop
        client.loop_stop()

    def _read_config(self, config_file):
        """
        Read the config file.
        """
        with open(r'%s' % config_file) as file:
            self.config = yaml.full_load(file)
        return self.config

if __name__ == "__main__":
    dohpcmqtt("/data/start.yml")

# {"key": "1", "subject": "LeavingWaterTemperatureHeating", "msg": 45}
# {"key": "1", "subject": "Power", "msg": "on"}
# {"key": "1", "subject": "Power", "msg": "standby"}
# {"key": "1", "subject": "OperationMode", "msg": "auto"}
# {"key": "1", "subject": "OperationMode", "msg": "cooling"}
# {"key": "1", "subject": "OperationMode", "msg": "heating"}
# {"key": "2", "subject": "DomesticHotWaterTemperatureHeating", "msg": 49}
