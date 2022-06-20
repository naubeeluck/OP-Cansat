import board
import digitalio
import time
import busio
import adafruit_bmp280
import adafruit_rfm9x
import adafruit_gps

#define the LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(scl=board.GP15, sda=board.GP14)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

RX = board.GP17
TX = board.GP16

uart = busio.UART(TX, RX, baudrate=9600, timeout=30)

def sat_temp():
    return bmp280_sensor.temperature

def sat_pressure():
    return bmp280_sensor.pressure
  
def sat_alt():
    return bmp280_sensor.altitude
    
gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()

bmp280.sea_level_pressure = 1034

  
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0) # set the transmit frequency to 433MHz

def send(message):
    rfm9x.send(message)

while True:

    led.value = not led.value
    Id = "CanSat Example,"
    sat_time = str("%.0f," % (time.monotonic()))# + " s"
    temp = str("%.1f," % (bmp280.temperature))# + " C"
    pressure = str("%.0f," % (bmp280.pressure))# + " hPa"
    altitude = str("%.1f," % (bmp280.altitude))# + " meters"
    latitude = str("%.6f," % (gps.latitude))# + " degrees"
    longitude = str("%.6f," % (gps.longitude))# + " degrees"
    
    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
    
    Payload = Id + sat_time + temp + pressure + altitude + latitude + longitude # message payload string
    rfm9x.send(Payload)
    print(Payload)
    
    time.sleep(1)