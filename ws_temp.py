import asyncio
import websockets
import spidev

# Configuration for MCP3008
SPI_CHANNEL = 0
ADC_MAX_VALUE = 1023
ADC_REF_VOLTAGE = 3.3
TEMP_SENSOR_VREF = 3.3
TEMP_SENSOR_OFFSET = 500  # Offset in mV
TEMP_SENSOR_SCALE = 10  # Scale factor (10mV/°C)

# Create SPI object
spi = spidev.SpiDev()
spi.open(0, SPI_CHANNEL)
spi.max_speed_hz = 1350000

async def get_temperature():
    adc_value = spi.xfer2([1, (8 + SPI_CHANNEL) << 4, 0])
    adc_value = ((adc_value[1] & 3) << 8) + adc_value[2]
    voltage = (adc_value / ADC_MAX_VALUE) * ADC_REF_VOLTAGE
    temperature = ((voltage * 1000) - TEMP_SENSOR_OFFSET) / TEMP_SENSOR_SCALE
    return temperature

async def handle_connection(websocket, path):
    print("Client connected")
    try:
        while True:
            temperature = await get_temperature()
            print(f"Sending temperature: {temperature}°C")
            await websocket.send(f"{temperature:.2f}")
            await asyncio.sleep(1)  # Send data every 1 second
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

async def main():
    server = await websockets.serve(handle_connection, "0.0.0.0", 8765)
    print("WebSocket server running on ws://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        spi.close()
