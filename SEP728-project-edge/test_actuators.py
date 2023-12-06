import RPi.GPIO as GPIO
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback,PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
import pubnub
import time
from ADCDevice import *
import json
#from gpiozero import Servo
from iot_data_mysql import update_iot_device_status

servo_pin = 29
motoRPin1 = 13
motoRPin2 = 11
enablePin = 15
pumpRPin1 = 16
pumpRPin2 = 18
enablePin2 = 22
heater = 36
light = 37
global p
global p2
global servo
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin,GPIO.OUT)   
GPIO.setup(motoRPin1,GPIO.OUT)   # set pins to OUTPUT mode
GPIO.setup(motoRPin2,GPIO.OUT)
GPIO.setup(pumpRPin1,GPIO.OUT)   # set pins to OUTPUT mode
GPIO.setup(pumpRPin2,GPIO.OUT)
GPIO.setup(enablePin,GPIO.OUT)
GPIO.setup(enablePin2,GPIO.OUT)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(heater, GPIO.OUT)
GPIO.output(motoRPin1,GPIO.HIGH)
GPIO.output(motoRPin2,GPIO.LOW)
GPIO.output(pumpRPin1,GPIO.HIGH)
GPIO.output(pumpRPin2,GPIO.LOW)
#servo = Servo(servo_pin)
p = GPIO.PWM(enablePin,1000) # creat PWM and set Frequence to 1KHz
p2 = GPIO.PWM(enablePin2,1000)
servo = GPIO.PWM(servo_pin,50)
servo.start(0)

pnconf = PNConfiguration() # create pubnub_configuration_object
pnconf.publish_key = 'pub-c-27131f89-98ae-4ee4-98d8-ee4b8581676f' # set pubnub publish_key
pnconf.subscribe_key = 'sub-c-3197c041-8ef6-4ad6-98c1-27de68282e21' # set pubnub subscibe_key
pnconf.user_id = 'haihttran'
pubnub = PubNub(pnconf) # create pubnub_object
channel='iot-command' # provide pubnub channel_name
data = { # data to be published
'message': 'test greenhouse command'
}
my_listener = SubscribeListener() # object to read the msg from the Broker/Server
pubnub.add_listener(my_listener) # add object to pubnub_object to subscribe it
pubnub.subscribe().channels(channel).execute() # subscribe the channel
my_listener.wait_for_connect() # wait for the obj to connect to the channel
print('connected') # print confirmation msg
pubnub.publish().channel(channel).message(data).sync() # publish to channel

def start_fan(p, speed):
	p.start(speed)
	update_iot_device_status("fan_1", "actuator", 1)

def stop_fan(p):
	p.stop()
	update_iot_device_status("fan_1", "actuator", 0)
	
def start_heater(heater):
	GPIO.output(heater,GPIO.HIGH)
	update_iot_device_status("heater_1", "actuator", 1)
	
def stop_heater(heater):
	GPIO.output(heater,GPIO.LOW)
	update_iot_device_status("heater_1", "actuator", 0)

def start_light(light):
	GPIO.output(light,GPIO.HIGH)
	update_iot_device_status("light_bulb_1", "actuator", 1)
	
def stop_light(light):
	GPIO.output(light,GPIO.LOW)
	update_iot_device_status("light_bulb_1", "actuator", 0)
	
def start_pump(p2, speed):
	p2.start(speed)
	update_iot_device_status("pump_1", "actuator", 1)

def stop_pump(p2):
	p2.stop()
	update_iot_device_status("pump_1", "actuator", 0)
	
def open_servo(servo):
	servo.ChangeDutyCycle(7.5)
	update_iot_device_status("drainage_servo_1", "actuator", 1)

def close_servo(servo):
	servo.ChangeDutyCycle(12.5)
	update_iot_device_status("drainage_servo_1", "actuator", 0)
	
def main():	
	stop_fan(p)
	stop_pump(p2)
	stop_light(light)
	stop_heater(heater)
	close_servo(servo)
	
	try:
		while True:			
			result = my_listener.wait_for_message_on(channel) # Read msg on channel
			cmd = result.message
			print(result.message)
			if('start_fan' in cmd):
				start_fan(p, 100)
				print('Now Fan On')
			elif('stop_fan' in cmd):
				stop_fan(p)
				print('Now Fan Off')
			elif('start_light' in cmd):
				start_light(light)
				print('Now Light On')
			elif('stop_light' in cmd):
				stop_light(light)
				print('Now Light Off')
			elif('start_heater' in cmd):
				start_heater(heater)
				print('Now Heater On')        
			elif('stop_heater' in cmd):
				stop_heater(heater)
				print('Now Heater Off')
			elif('open_drainage_servo' in cmd):
				open_servo(servo)
				print('Now drainage servo open')        
			elif('close_drainage_servo' in cmd):
				close_servo(servo)
				print('Now drainage servo closed')
			elif('start_pump' in cmd):
				start_pump(p2, 99)
				print('Now Pump On')        
			elif('stop_pump' in cmd):
				stop_pump(p2)
				print('Now Pump Off')			

	except KeyboardInterrupt:		
		print("cleaning up.")
		p.stop()
		p2.stop()
		servo.stop()
		GPIO.cleanup()
    
if __name__ == '__main__':
	main()

