from sqlalchemy import create_engine, text
import mysql
import datetime

#Insert sensor data into MySQL database
def update_iot_data(data):
    connection_string = "mysql+mysqlconnector://db_user:mysql@3.149.252.18:3306/greenhouse"
    engine = create_engine(connection_string, echo=False)

    with engine.connect() as connection:
        query = "INSERT INTO  iot_data (sensor_id ,sensor_type , value , time) VALUES(:sensor_id ,:sensor_type , :value , :time)"
        connection.execute(text(query),data)
        connection.commit()
        connection.close()
    engine.dispose()

#Update status of IoT devices to MySQL database    
def update_iot_device_status(device_id, device_class, status):
	connection_string = "mysql+mysqlconnector://db_user:mysql@3.149.252.18:3306/greenhouse"
	engine = create_engine(connection_string, echo=False)
	with engine.connect() as connection:
		query = """UPDATE iot_device_status SET status = :status, time = :time 
		WHERE device_id = :device_id and device_class = :device_class"""
		data = {'status' : status, 'time' : str(datetime.datetime.now()), 'device_id' : device_id, 'device_class' : device_class}
		#print(data)
		connection.execute(text(query),data)
		connection.commit()
		connection.close()
	engine.dispose()

