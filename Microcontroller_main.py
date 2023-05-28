import machine
from machine import I2C, Pin, UART
import utime as time
from pico_i2c_lcd import I2cLcd

# set up serial Bluetooth
uart = UART(0, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

# set up LCD screen
i2c = I2C(id=1, scl=Pin(19), sda=Pin(18), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

while True:
    # read sensor data
    adc = machine.ADC(26)
    conversion_factor = 100 / (65535)
    moisture = 130 - (adc.read_u16() * conversion_factor)
    print("Moisture: ", round(moisture, 1), "% - ")
    
    # display data on LCD screen
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr('Moisture:')
    lcd.move_to(0, 1)
    lcd.putstr(str(round(moisture, 1)) + " %")

    # wait for 5 seconds before reading data again
    time.sleep(5)

    # send data via serial Bluetooth
    data = str(moisture)
    data2= data+'$'
    uart.write(data2)
    print(data2)

    # wait for 1 second before sending data again
time.sleep(1)





