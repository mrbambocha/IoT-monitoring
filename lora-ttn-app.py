import time
import ttn
import json
import datetime
import os
from influxdb import InfluxDBClient
import paho.mqtt.client as mqttClient

# TTN connection
APP_ID = os.environ.get('TTN_APP_ID')
ACCESS_KEY = os.environ.get('TTN_ACCESS_KEY')

# influxdb connection
influxdbHost = os.environ.get('INFLUXDB_HOST')
influxdbPort = os.environ.get('INFLUXDB_PORT')
influxdbUser = os.environ.get('INFLUXDB_USER')
influxdbPswd = os.environ.get('INFLUXDB_PSWD')
influxdbName = os.environ.get('INFLUXDB_NAME')
influxdbClient = InfluxDBClient(influxdbHost, influxdbPort, influxdbUser, influxdbPswd)

def uplink_callback(msg, client):
	print("\nMessage object : "+str(msg))
	devID = str(msg.dev_id)
	hardwareSerial = str(msg.hardware_serial)
	if (devID.upper() == "A81758FFFE0459FD") or (devID.upper() == "A81758FFFE0459FE"): #EL2 Devices
		print("Processing data received from ELT2 device : "+devID)
		try:
			payloadAccMotion = str(msg.payload_fields.accMotion)
			print("accMotion="+payloadAccMotion)
			payloadExternalTemperature = str(msg.payload_fields.externalTemperature)
			print("externalTemperature="+payloadExternalTemperature)
			payloadHumidity = str(msg.payload_fields.humidity)
			print("humidity="+payloadHumidity)
			payloadPressure = str(msg.payload_fields.pressure)
			print("pressure="+payloadPressure)
			payloadTemperature = str(msg.payload_fields.temperature)
			print("temperature="+payloadTemperature)
			payloadVdd = str(msg.payload_fields.vdd)
			print("vdd="+payloadVdd)
			payloadX = str(msg.payload_fields.x)
			print("x="+payloadX)
			payloadY = str(msg.payload_fields.y)
			print("y="+payloadY)
			payloadZ = str(msg.payload_fields.z)
			print("z="+payloadZ)
			lineForDB = devID+",hardware_serial="+hardwareSerial
			lineForDB = lineForDB+" accMotion="+payloadAccMotion+",externalTemperature="+payloadExternalTemperature+",humidity="+payloadHumidity+",pressure="+payloadPressure+",temperature="+payloadTemperature
			lineForDB = lineForDB+",vdd="+payloadVdd+",x="+payloadX+",y="+payloadY+",z="+payloadZ
			print("Line Object created to be sent to DB : "+str(lineForDB))
			influxdbClient.write([lineForDB],{'db':influxdbName},204,'line')
			print("Data inserted to DB")
		except:
			print("Exception while processing data received from EL2 device")
	elif (devID.upper() == "A81758FFFE045FA4") or (devID.upper() == "A81758FFFE045FA5"): #ERS_CO2 devices
		print("Processing data received from ERS_CO2 device : "+devID)
		try:
			payloadCo2 = str(msg.payload_fields.co2)
			print("co2="+payloadCo2)
			payloadHumidity = str(msg.payload_fields.humidity)
			print("humidity="+payloadHumidity)
			payloadLight = str(msg.payload_fields.light)
			print("light="+payloadLight)
			payloadMotion = str(msg.payload_fields.motion)
			print("motion="+payloadMotion)
			payloadTemperature = str(msg.payload_fields.temperature)
			print("temperature="+payloadTemperature)
			payloadVdd = str(msg.payload_fields.vdd)
			print("vdd="+payloadVdd)
			lineForDB = devID+",hardware_serial="+hardwareSerial
			lineForDB = lineForDB+" co2="+payloadCo2+",humidity="+payloadHumidity+",light="+payloadLight+",motion="+payloadMotion+",temperature="+payloadTemperature+",vdd="+payloadVdd
			print("Line Object created to be sent to DB : "+str(lineForDB))
			influxdbClient.write([lineForDB],{'db':influxdbName},204,'line')
			print("Data inserted to DB")
		except:
			print("Exception while processing data received from ERS_CO2 device")

handler = ttn.HandlerClient(APP_ID, ACCESS_KEY)
# using mqtt client
mqttClient = handler.data()
mqttClient.set_uplink_callback(uplink_callback)
# create database in influxdb if it's not there
dbList = str(influxdbClient.get_list_database())
print("Current List of Databases : "+dbList)
dataDBEntry = "{'name': '"+influxdbName+"'}"
if(dbList.find(dataDBEntry) != -1):
	print("Database ("+influxdbName+") found")
else:
	print("Database ("+influxdbName+") not found. Trying to create it...")
	try:
		influxdbClient.create_database(influxdbName)
		dbList = str(influxdbClient.get_list_database())
		print("Updated List of Databases : "+dbList)
	except:
		print("Unable to create ("+influxdbName+") database")
while True:
	mqttClient.connect()
	print(f"Connected to: {APP_ID} => {ACCESS_KEY}")
	print("Waiting for messages...")
	time.sleep(300)


