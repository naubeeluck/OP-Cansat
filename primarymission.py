import board
import digitalio
import time
import radio
import busio
import adafruit_rfm9x

#define the LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

'''
Set up the BMP280. Pins usd are:
SCL = GP15
SDA = GP14

Then define the temperature, pressure and altitude
'''
i2c = busio.I2C(scl=board.GP15, sda=board.GP14, frequency=440000)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

def read_temperature():
    return bmp280_sensor.temperature

def read_pressure():
    return bmp280_sensor.pressure
  
def read_altitude():
    return bmp280_sensor.altitude

'''
Set the local atmospheric pressure (QNH). This will be used to calculate the altitude. 
Note that sea level pressure can be your local pressure so a local weather report for that day will suffice.
Its important to note that the sensor only infers altitude for the pressure so it will have
inaccuracies.
'''
sensor.sea_level_pressure = 1013.25