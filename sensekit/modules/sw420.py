import RPi.GPIO as GPIO

def sw420(gpiopin):
    return GPIO.input(gpiopin)
