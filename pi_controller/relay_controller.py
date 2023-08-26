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

    def relayController(self, relayNumber, relayStatus):
        if relayNumber == 1:
            return GPIO.output(5, relayStatus)
        elif relayNumber == 2:
            return GPIO.output(6, relayStatus)
        elif relayNumber == 3:
            return GPIO.output(13, relayStatus)
        elif relayNumber == 4:
            return GPIO.output(16, relayStatus)
        elif relayNumber == 5:
            return GPIO.output(19, relayStatus)
        elif relayNumber == 6:
            return GPIO.output(20, relayStatus)
        else:
            return False

    def checkRelayStatus(self, relayNumber):
        if relayNumber == 1:
            return GPIO.input(5)
        elif relayNumber == 2:
            return GPIO.input(6)
        elif relayNumber == 3:
            return GPIO.input(13)
        elif relayNumber == 4:
            return GPIO.input(16)
        elif relayNumber == 5:
            return GPIO.input(19)
        elif relayNumber == 6:
            return GPIO.input(20)
        else:
            return False
