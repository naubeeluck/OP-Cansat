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
    return bmp280_sensor.temperature # Return temp readings

def sat_pressure():
    return bmp280_sensor.pressure # Return pressure readings
  
def sat_alt():
    return bmp280_sensor.altitude # Return altitude determined
    
gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # Minimum data and fix data Refer to pg10 of https://cdn-shop.adafruit.com/datasheets/PMTK_A08.pdf

gps.send_command(b'PMTK220,1000') # Output @1Hz Refer to pg7 of https://cdn-shop.adafruit.com/datasheets/PMTK_A08.pdf

last_print = time.monotonic() # Timing in seconds

bmp280.sea_level_pressure = 1034 # Sea level pressure in hPa

  
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0) # set the transmit frequency to 433MHz

def send(message):
    rfm9x.send(message)

while True:

    led.value = not led.value
    Id = "CanSat Example,"
    sat_time = str("%.0f s," % (time.monotonic()))
    temp = str("%.1f C," % (bmp280.temperature))
    pressure = str("%.0f hPa," % (bmp280.pressure))
    altitude = str("%.1f m," % (bmp280.altitude))

    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
                              # Without fix assign dummy values
                              longitude = str("!,")
                              latitude = str("!,")
        else:
                              # With fix assign values
                              latitude = str("%.6f," % (gps.latitude))# + " degrees"
                              longitude = str("%.6f," % (gps.longitude))# + " degrees"
    
        Payload = Id + sat_time + temp + pressure + altitude + latitude + longitude # message payload string
        rfm9x.send(Payload)
        print(Payload)
        
    time.sleep(1)
