import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

# GPIO setup
led = 4  # GPIO pin where the LED is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

# Initialize PWM on the LED pin with a frequency of 1000Hz
pwm = GPIO.PWM(led, 1000)
pwm.start(0)  # Start PWM with 0% duty cycle (LED off)

# MQTT setup
mqttc = mqtt.Client()

# Callback function for successful connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ws/led/65070131")  # Subscribe to the topic

# Callback function for receiving a message
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print(f"Received message: {message} on topic {msg.topic}")
    try:
        brightness = int(message)
        if 0 <= brightness <= 100:
            pwm.ChangeDutyCycle(brightness)  # Update the LED brightness
        else:
            print("Received value out of range (0-100)")
    except ValueError:
        print("Received non-integer message")

mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect to the broker
mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)

# Start the MQTT client loop to process incoming messages
mqttc.loop_start()

try:
    while True:
        time.sleep(1)  # Keep the main loop running
except KeyboardInterrupt:
    print("Exiting gracefully")
finally:
    pwm.stop()  # Stop PWM
    GPIO.cleanup()
    mqttc.loop_stop()
    mqttc.disconnect()
