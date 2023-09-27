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
    relayController(1,0) --> switch off the Relay
    relayController(1,1) --> switch on the Relay 
"""


class RelayControl:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        # # Bulb wireing is inverted
        # GPIO.output(5, GPIO.HIGH)
        # GPIO.output(6, GPIO.HIGH)
        # GPIO.output(13, GPIO.HIGH)
        # GPIO.output(16, GPIO.HIGH)
        # GPIO.output(19, GPIO.HIGH)
        # GPIO.output(20, GPIO.HIGH)

    def relayController(self, relayNumber, relayStatus):
        if relayNumber == 1:
            return GPIO.output(24, relayStatus)            
        elif relayNumber == 2:
            return GPIO.output(25, relayStatus)
        elif relayNumber == 3:
            return GPIO.output(8, relayStatus)
        elif relayNumber == 4:
            return GPIO.output(7, relayStatus)
        elif relayNumber == 5:
            return GPIO.output(12, relayStatus)
        elif relayNumber == 6:
            return GPIO.output(16, relayStatus)
        else:
            return False

    def checkRelayStatus(self, relayNumber):
        if relayNumber == 1:
            return GPIO.input(24)
        elif relayNumber == 2:
            return GPIO.input(25)
        elif relayNumber == 3:
            return GPIO.input(8)
        elif relayNumber == 4:
            return GPIO.input(7)
        elif relayNumber == 5:
            return GPIO.input(12)
        elif relayNumber == 6:
            return GPIO.input(16)
        else:
            return False
