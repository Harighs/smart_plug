import RPi.GPIO as GPIO

"""
 This class is responsible to handle all the operations done in Raspberry Pi Zero.
 - Accessing the specific GPIO 
 - Triggering the GPIO
"""


# Enabling relay socket on GPIO 5
def enable_relay1():
    GPIO.output(5, GPIO.LOW)


# Disabling relay socket on GPIO 5
def disable_relay1():
    GPIO.output(5, GPIO.HIGH)


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


def relay_switch_controller(relay_switch_number, relay_switch_status):
    if relay_switch_number == 1:
        GPIO.output(5, relay_switch_status)
    elif relay_switch_number == 2:
        GPIO.output(6, relay_switch_status)


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
        # Relay wiring is inverted
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
