import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

# GPIO setup
switch = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN)

# MQTT setup
mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

mqttc.on_connect = on_connect

mqttc.connect("broker.mqtt-dashboard.com", 1883)

# Start the MQTT client loop
mqttc.loop_start()

try:
    while True:
        if GPIO.input(switch) == GPIO.HIGH:
            mqttc.publish("switch65070131", "ON")
        elif GPIO.input(switch) == GPIO.LOW:
            mqttc.publish("switch65070131", "OFF")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting gracefully")

finally:
    GPIO.cleanup()
    mqttc.loop_stop()
    mqttc.disconnect()

