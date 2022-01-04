# Write your code here :-)
import board
import busio
import adafruit_bmp280

i2c = busio.I2C(scl=board.GP15, sda=board.GP14)

bmp280_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

def read_temperature():
    return bmp280_sensor.temperature

def read_pressure():
    return bmp280_sensor.pressure

cansat_temperature = bmp280.read_temperature()
print(cansat_temperature)
