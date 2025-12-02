#!/usr/bin/env python3
# Smart Irrigation System using Raspberry Pi
# Summer Training Project 2021

import time
import RPi.GPIO as GPIO
import spidev

# GPIO Setup
LCD_RS = 4
LCD_E = 17
LCD_D4 = 18
LCD_D5 = 27
LCD_D6 = 22
LCD_D7 = 23
RELAY_PIN = 24
RAIN_SENSOR = 25

# SPI for ADC
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
LCD_WIDTH = 16

# GPIO initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(RAIN_SENSOR, GPIO.IN)

def lcd_init():
    """Initialize LCD display"""
    lcd_byte(0x33, GPIO.LOW)  # Initialize
    lcd_byte(0x32, GPIO.LOW)  # Initialize
    lcd_byte(0x06, GPIO.LOW)  # Cursor move direction
    lcd_byte(0x0C, GPIO.LOW)  # Display On, Cursor Off
    lcd_byte(0x28, GPIO.LOW)  # Data length, lines, font
    lcd_byte(0x01, GPIO.LOW)  # Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    """Send byte to LCD data pins"""
    GPIO.output(LCD_RS, mode)
    
    # High bits
    GPIO.output(LCD_D4, GPIO.LOW)
    GPIO.output(LCD_D5, GPIO.LOW)
    GPIO.output(LCD_D6, GPIO.LOW)
    GPIO.output(LCD_D7, GPIO.LOW)
    
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, GPIO.HIGH)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, GPIO.HIGH)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, GPIO.HIGH)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, GPIO.HIGH)
    
    lcd_toggle_enable()
    
    # Low bits
    GPIO.output(LCD_D4, GPIO.LOW)
    GPIO.output(LCD_D5, GPIO.LOW)
    GPIO.output(LCD_D6, GPIO.LOW)
    GPIO.output(LCD_D7, GPIO.LOW)
    
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, GPIO.HIGH)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, GPIO.HIGH)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, GPIO.HIGH)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, GPIO.HIGH)
    
    lcd_toggle_enable()

def lcd_toggle_enable():
    """Toggle enable pin to send data"""
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    """Display string on LCD"""
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, GPIO.LOW)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), GPIO.HIGH)

def read_adc(channel):
    """Read ADC value from specified channel (0-7)"""
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_temp(data):
    """Convert ADC reading to temperature in Celsius"""
    temp = ((data * 330) / float(1023))
    return round(temp, 2)

def send_sms(message):
    """Send SMS alert using GSM module"""
    # GSM module implementation
    print(f"SMS Alert: {message}")
    # Actual GSM code would use serial communication

def main():
    """Main program loop"""
    lcd_init()
    lcd_string("Smart Irrigation", 0x80)
    lcd_string("System Started", 0xC0)
    time.sleep(2)
    
    while True:
        # Read sensors
        temp_level = read_adc(0)
        temperature = convert_temp(temp_level)
        
        moisture_level = read_adc(1)
        rain_detected = GPIO.input(RAIN_SENSOR)
        
        # Display readings
        lcd_string(f"Temp: {temperature}C", 0x80)
        lcd_string(f"Moisture: {moisture_level}", 0xC0)
        time.sleep(1)
        
        # Control logic
        if temperature > 25 and moisture_level < 100 and not rain_detected:
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            lcd_string("Motor: ON ", 0x80)
            lcd_string("Watering...", 0xC0)
            send_sms("Motor Started - Irrigation Active")
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)
            lcd_string("Motor: OFF", 0x80)
            if rain_detected:
                lcd_string("Rain Detected", 0xC0)
                send_sms("Rain Detected - Motor Off")
            else:
                lcd_string("Conditions OK", 0xC0)
        
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        GPIO.cleanup()
