import spidev
import time
import paho.mqtt.client as mqtt

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# MQTT setup
mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

mqttc.on_connect = on_connect

# Connect to the MQTT broker
mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)

# Function to read SPI data from MCP3008 chip
def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    while True:
        # Read potentiometer value from MCP3008 CH0 (channel 0)
        adc_value = read_adc(0)
        # Scale the value to 0-100 (MCP3008 is a 10-bit ADC, so max value is 1023)
        pot_value = int((adc_value / 1023.0) * 100)
        print(f"Potentiometer value: {pot_value}")
        

        # Publish the value via MQTT
        mqttc.publish("ws/pot/65070131", pot_value)
        
        time.sleep(1)  # Publish every second
except KeyboardInterrupt:
    print("Exiting gracefully")
finally:
    spi.close()
    mqttc.loop_stop()
    mqttc.disconnect()
