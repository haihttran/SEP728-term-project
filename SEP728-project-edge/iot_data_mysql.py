from sqlalchemy import create_engine, text
import mysql
import datetime

def update_iot_data(data):

    connection_string = "mysql+mysqlconnector://db_user:mysql@3.149.252.18:3306/greenhouse"
    engine = create_engine(connection_string, echo=True)

    with engine.connect() as connection:
        query = "INSERT INTO  iot_data (sensor_id ,sensor_type , value , time) VALUES(:sensor_id ,:sensor_type , :value , :time)"
        connection.execute(text(query),data)
        connection.commit()

