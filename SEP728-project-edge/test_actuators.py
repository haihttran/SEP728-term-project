import RPi.GPIO as GPIO
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback,PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
import pubnub
import time
from ADCDevice import *
import json

motoRPin1 = 13
motoRPin2 = 11
enablePin = 15
heater = 36
light = 37
global p
GPIO.setmode(GPIO.BOARD)   
GPIO.setup(motoRPin1,GPIO.OUT)   # set pins to OUTPUT mode
GPIO.setup(motoRPin2,GPIO.OUT)
GPIO.setup(enablePin,GPIO.OUT)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(heater, GPIO.OUT)
GPIO.output(motoRPin1,GPIO.HIGH)
GPIO.output(motoRPin2,GPIO.LOW)
p = GPIO.PWM(enablePin,1000) # creat PWM and set Frequence to 1KHz

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

def stop_fan(p):
	p.stop()
	
def start_heater(heater):
	GPIO.output(heater,GPIO.HIGH)
	
def stop_heater(heater):
	GPIO.output(heater,GPIO.LOW)

def start_light(light):
	GPIO.output(light,GPIO.HIGH)
	
def stop_light(light):
	GPIO.output(light,GPIO.LOW)
	
def main():
	stop_fan(p)
	stop_light(light)
	stop_heater(heater)
	try:
		while True:
			result = my_listener.wait_for_message_on(channel) # Read msg on channel
			print(result.message)
			if(result.message == '{"command":"start_fan"}'):
				start_fan(p, 100)
				print('Now Fan On')
			elif(result.message == '{"command":"stop_fan"}'):
				stop_fan(p)
				print('Now Fan Off')
			elif(result.message == '{"command":"start_light"}'):
				start_light(light)
				print('Now Light On')
			elif(result.message == '{"command":"stop_light"}'):
				stop_light(light)
				print('Now Light Off')
			elif(result.message == '{"command":"start_heater"}'):
				start_heater(heater)
				print('Now Heater On')        
			elif(result.message == '{"command":"stop_heater"}'):
				stop_heater(heater)
				print('Now Heater Off')			
		 
	finally:
		print("cleaning up.")
		p.stop()
		GPIO.cleanup()
    
if __name__ == '__main__':
	main()

