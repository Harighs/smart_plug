import RPi.GPIO as GPIO


# Enabling relay socket on GPIO 5
def enable_relay1():
    GPIO.output(5, GPIO.LOW)


# Disabling relay socket on GPIO 5
def disable_relay1():
    GPIO.output(5, GPIO.HIGH)

"""
 This class is responsible to handle all the operations done in Raspberry Pi Zero.
 - Accessing the specific GPIO 
 - Triggering the GPIO
"""

"""
Dynamic relay switching technique
Getting parameter from API

Parameters: 
    relaySwitchNumber: defines the relay switch (1-6)
    relaySwitchStatus: defines the relay switch status (0 - ON / 1 - OFF)

Results:
    Passes the signal via GPIO and Switch ON/OFF the relays

Examples:
    relay_switch_controller(1,0) --> switch the Relay 1
    relay_switch_controller(1,1) --> switch off the Relay 1
"""
class RelayControl:
        def __init__(self):
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(5, GPIO.OUT)
                GPIO.setup(6, GPIO.OUT)
                GPIO.setup(13, GPIO.OUT)
                GPIO.setup(16, GPIO.OUT)
                GPIO.setup(19, GPIO.OUT)
                GPIO.setup(20, GPIO.OUT)
                # # Bulb wireing is inverted
                # GPIO.output(5, GPIO.HIGH)
                # GPIO.output(6, GPIO.HIGH)
                # GPIO.output(13, GPIO.HIGH)
                # GPIO.output(16, GPIO.HIGH)
                # GPIO.output(19, GPIO.HIGH)
                # GPIO.output(20, GPIO.HIGH)

        def socket_controller(self, switchNumber, switchStatus):
                if switchNumber == 1:
                        GPIO.output(5, switchStatus)
                elif switchNumber == 2:
                        GPIO.output(6, switchStatus)
                elif switchNumber == 3:
                        GPIO.output(13, switchStatus)
                elif switchNumber == 4:
                        GPIO.output(16, switchStatus)
                elif switchNumber == 5:
                        GPIO.output(19, switchStatus)
                elif switchNumber == 6:
                        GPIO.output(20, switchStatus)
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