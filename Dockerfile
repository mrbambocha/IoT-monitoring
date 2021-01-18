FROM python:3
ADD lora-ttn-app.py /
RUN pip install ttn
RUN pip install paho-mqtt
RUN pip install influxdb
CMD [ "python3", "./lora-ttn-app.py" ]
