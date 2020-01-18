# _____ _____ _____ __ __ _____ _____ 
#|     |   __|     |  |  |     |     |
#|  |  |__   |  |  |_   _|  |  |  |  |
#|_____|_____|_____| |_| |_____|_____|
#
# Use Raspberry Pi to get temperature/humidity from DHT11 sensor
#  
import time
import dht11
import RPi.GPIO as GPIO

Temp_sensor=14

def get_results():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       
  instance = dht11.DHT11(pin = Temp_sensor)
  while True:
    #get DHT11 sensor value
    result = instance.read()
    if (result.temperature != 0) or (result.humidity != 0): 
      return result      

