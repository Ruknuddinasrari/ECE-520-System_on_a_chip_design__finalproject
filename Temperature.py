# Import necessary modules
import machine
from machine import Pin, ADC, I2C
import time
import math
import fonts_file
from lcd_driver import lcd128_32

# Set up ADC with GPIO pin 26
adc = ADC(26)

# I2C configuration settings
clock_pin = 21
data_pin = 20
bus = 0
i2c_addr = 0x3f
use_i2c = True

# Function to scan I2C bus for devices and print their addresses
def scan_for_devices():
    # Create I2C object with specified pins and bus
    i2c = machine.I2C(bus, sda=machine.Pin(data_pin), scl=machine.Pin(clock_pin))
    # Scan the bus for connected devices
    devices = i2c.scan()
    # If devices are found, print their addresses
    if devices:
        for d in devices:
            print(hex(d))
    # Otherwise, print a message indicating no devices are connected
    else:
        print('no i2c devices')

# Check if I2C is to be used, and if so, scan for devices and initialize LCD object
if use_i2c:
    scan_for_devices()
    # Initialize the LCD object with specified pins, bus, and address
    lcd = lcd128_32(data_pin, clock_pin, bus, i2c_addr)

try:
    # Enter an infinite loop to continuously read the temperature and display it on the LCD
    while True:
        # Read the ADC value from the specified pin
        adcValue = adc.read_u16()
        # Convert the ADC value to a voltage reading
        voltage = adcValue / 65535.0 * 3.3
        # Calculate the resistance of the thermistor
        Rt = 10 * voltage / (3.3 - voltage)
        # Steinhart-Hart equation relates temperature to the resistance of a thermistor
        # The equation is: 1/T = 1/T0 + 1/B * ln(R/R0)
        # where T0 is the reference temperature (usually 25°C), 
        # B is the beta value of the thermistor, 
        # R0 is the resistance at T0, and 
        # R is the resistance at the measured temperature
        tempK = (1 / (1 / (273.15 + 25) + (math.log(Rt / 10)) / 3950))
        # Convert the temperature from Kelvin to Celsius
        tempC = int(tempK - 273.15)

        # Clear the LCD screen
        lcd.Clear()
        # Display a welcome message on the LCD
        lcd.Cursor(0, 4)
        lcd.Display("Hello ]")
        lcd.Cursor(1, 0)
        lcd.Display("Welcome To CSUN")
        lcd.Cursor(2, 0)
        lcd.Display("ECE 520 By P.Saba")
        # Display the temperature reading on the LCD
        lcd.Cursor(3, 0)
        lcd.Display("Temperature:")
        lcd.Cursor(3, 13)
        lcd.Display(str(tempC))
        lcd.Cursor(3, 16)
        lcd.Display("C")

        # Wait 1.5 seconds before repeating the loop
        time.sleep(1.5)

# If an exception occurs, exit 
except:
    pass
