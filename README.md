# smart-irrigation-system  Using Raspberry Pi
A fully automated smart irrigation system powered by Raspberry pi and field sensors.  

##  Overview
An IoT-based automated irrigation system that monitors soil moisture, temperature, and rainfall to intelligently control water pumps. Designed to reduce water waste by 40-60% while maintaining optimal crop health.

##  Features
- **Intelligent Watering**: Automatically waters plants based on soil moisture levels
- **Weather Adaptive**: Stops watering when rain is detected
- **Real-Time Alerts**: Sends SMS notifications to farmer's mobile
- **Energy Efficient**: Uses Raspberry Pi for low-power operation
- **Easy Monitoring**: 16x2 LCD displays all sensor readings

##  System Architecture

**Sensors**: Soil moisture, temperature, rain
**Controller**: Raspberry Pi 3
**Output**:Water pump, LCD, GSM
**Power**: 5V & 12V supply

##  Hardware Components

 **Raspberry Pi 3**: Main controller 
 **LM35 Sensor**: Temperature monitoring 
 **Soil Moisture Sensor**: Soil water content measurement 
 **Rain Sensor**: Rainfall detection 
 **DC Motor (12V)**: Water pump 
 **GSM Module**: SMS notifications 
 **16x2 LCD**: Status display

## Software Requirements
 Raspberry Pi OS
 Python 3.x
 RPi.GPIO library
 spidev library

## Installation & Setup

### Hardware Connections
1. Connect sensors to Raspberry Pi GPIO pins
2. Connect relay to control water pump
3. Connect LCD display
4. Power up the system

### Software Installation

# Clone repository
git clone https://github.com/ashishjoshi23/Smart-Irrigation-System.git
cd Smart-Irrigation-System

# Install dependencies
pip install -r python/requirements.txt

## Working Logic

if temperature > 25°C AND moisture < 100 AND no_rain:
    motor = ON
    send_sms("Irrigation started")
else:
    motor = OFF
    if rain_detected:
        send_sms("Rain detected - irrigation stopped")

# Run the system
sudo python python/smart_irrigation.py
