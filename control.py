import RPi.GPIO as GPIO
import serial
import os
import can
from can import Message
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)

GPIO.output(5,GPIO.LOW)
GPIO.output(6,GPIO.LOW)
GPIO.output(13,GPIO.LOW)
GPIO.output(16,GPIO.LOW)
GPIO.output(19,GPIO.LOW)
GPIO.output(20,GPIO.LOW)


while True:
	switch = input("<switch>: ")
	func = input("0|1: ")
	switch=int(switch)
	func = int(func)

	if switch == 1:
		if func==0:
			GPIO.output(5,GPIO.LOW)
		elif func==1:
			GPIO.output(5,GPIO.HIGH)
		else:
			pass

	elif switch == 2:
		if func==0:
			GPIO.output(6,GPIO.LOW)
		elif func==1:
			GPIO.output(6,GPIO.HIGH)
		else:
			pass

GPIO.cleanup()
