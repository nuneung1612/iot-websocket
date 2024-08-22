import paho.mqtt.client as mqtt
import time

mqttc = mqtt.Client()
mqttc.connect("broker.mqtt-dashboard.com", 1883)

while True:
        mqttc.publish("mytopic", "Hello from raspi")
        time.sleep(2)
