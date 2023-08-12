import RPi.GPIO as GPIO

class BulbControl:
        def __init__(self):
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(5, GPIO.OUT)
                GPIO.setup(6, GPIO.OUT)
                GPIO.setup(13, GPIO.OUT)
                GPIO.setup(16, GPIO.OUT)
                GPIO.setup(19, GPIO.OUT)
                GPIO.setup(20, GPIO.OUT)
                # Bulb wireing is inverted
                GPIO.output(5, GPIO.HIGH)
                GPIO.output(6, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)
                GPIO.output(16, GPIO.HIGH)
                GPIO.output(19, GPIO.HIGH)
                GPIO.output(20, GPIO.HIGH)
                
        # Turning on bulb 1
        def bulb_on(self):
                GPIO.output(5, GPIO.LOW) #Wire is inverted

        def bulb_off(self):
                GPIO.output(5, GPIO.HIGH) # Wire is inverted
        
        def socket_controller(self, switchNumber, switchStatus):
                if switchNumber == 1:
                        GPIO.output(5, switchStatus)
                elif switchNumber == 2:
                        GPIO.output(6, switchStatus)