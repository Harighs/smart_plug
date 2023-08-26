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
                elif switchNumber == 3:
                        return GPIO.input(13)
                elif switchNumber == 4:
                        return GPIO.input(16)
                elif switchNumber == 5:
                        return GPIO.input(19)
                elif switchNumber == 6:
                        return GPIO.input(20)
                else:
                        return False
        
        def check_socket_status(self, switchNumber):
                if switchNumber == 1:
                        return GPIO.input(5)
                elif switchNumber == 2:
                        return GPIO.input(6)
                elif switchNumber == 3:
                        return GPIO.input(13)
                elif switchNumber == 4:
                        return GPIO.input(16)
                elif switchNumber == 5:
                        return GPIO.input(19)
                elif switchNumber == 6:
                        return GPIO.input(20)
                else:
                        return False