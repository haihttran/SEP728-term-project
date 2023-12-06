import RPi.GPIO as GPIO
import Freenove_DHT as DHT
from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback,PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
import pubnub
import datetime
import json
import iot_data_mysql

dht_sensor = 32
#aindrop_sensor = 36
#soil_sensor = 37
#light_sensor = 31

sensor1 = DHT.DHT(dht_sensor)

GPIO.setmode(GPIO.BOARD)
pot = MCP3008(0)
pot1 = MCP3008(1)
pot2 = MCP3008(2)
GPIO.setup(dht_sensor, GPIO.IN)
#GPIO.setup(raindrop_sensor, GPIO.IN)
#GPIO.setup(soil_sensor, GPIO.IN)
#GPIO.setup(light_sensor, GPIO.IN)

pnconf = PNConfiguration() # create pubnub_configuration_object
pnconf.publish_key = 'pub-c-27131f89-98ae-4ee4-98d8-ee4b8581676f' # set pubnub publish_key
pnconf.subscribe_key = 'sub-c-3197c041-8ef6-4ad6-98c1-27de68282e21' # set pubnub subscibe_key
pnconf.user_id = 'haihttran'
pubnub = PubNub(pnconf) # create pubnub_object
channel='iot-data' # provide pubnub channel_name
data = { # data to be published
'message': 'test greenhouse sensors data'
}
my_listener = SubscribeListener() # object to read the msg from the Broker/Server
pubnub.add_listener(my_listener) # add object to pubnub_object to subscribe it
pubnub.subscribe().channels(channel).execute() # subscribe the channel
my_listener.wait_for_connect() # wait for the obj to connect to the channel
print('connected') # print confirmation msg
pubnub.publish().channel(channel).message(data).sync() # publish to channel

while True:
	#print('\n')
	#time.sleep(10)
	multi_key = []
	sensor1.readDHT11()
	#print(sensor1.temperature)
	#print(sensor1.humidity)
	data = []	
	multi_key.append(dict(zip(('sensor_id', 'sensor_type','value','time'),
				('temp_1','temperature',sensor1.temperature,str(datetime.datetime.now())))))
	data.append({'sensor_id' : 'temp_1','sensor_type' : 'temperature','value' : sensor1.temperature, 'time' : str(datetime.datetime.now())})
	
	multi_key.append(dict(zip(('sensor_id', 'sensor_type','value','time'),
				('humidity_1','air_humidity',sensor1.humidity,str(datetime.datetime.now())))))
	data.append({'sensor_id' : 'humidity_1','sensor_type' : 'air_humidity','value' : sensor1.humidity, 'time' : str(datetime.datetime.now())})
	
	multi_key.append(dict(zip(('sensor_id', 'sensor_type','value','time'),
				('light_1','light_intensity',1-pot2.value,str(datetime.datetime.now())))))
	data.append({'sensor_id' : 'light_1','sensor_type' : 'light_intensity','value' : 1-pot2.value, 'time' : str(datetime.datetime.now())})
	
	multi_key.append(dict(zip(('sensor_id', 'sensor_type','value','time'),
				('soil_1','soil_moisture',1-pot.value,str(datetime.datetime.now())))))
	data.append({'sensor_id' : 'soil_1','sensor_type' : 'soil_moisture','value' : 1-pot.value, 'time' : str(datetime.datetime.now())})
	
	multi_key.append(dict(zip(('sensor_id', 'sensor_type','value','time'),
				('raindrop_1','rain_drop',1-pot1.value,str(datetime.datetime.now())))))
	data.append({'sensor_id' : 'raindrop_1','sensor_type' : 'rain_drop','value' : 1-pot1.value, 'time' : str(datetime.datetime.now())})
	
	json_str = json.dumps(multi_key)
	print(json_str)
	iot_data_mysql.update_iot_data(data)
	pubnub.publish().channel(channel).message(json_str).sync()
	
	time.sleep(30)
	#time.sleep(10)
