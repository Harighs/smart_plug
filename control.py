import RPi.GPIO as GPIO

class BulbControl:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)

        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
    
    # Turning on bulb 1
    def bulb_on(self):
        GPIO.output(5, GPIO.HIGH)

    def bulb_off(self):
        GPIO.output(5, GPIO.LOW)
