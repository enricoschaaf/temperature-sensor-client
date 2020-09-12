from json import dumps
from math import floor
from os import environ
from time import sleep, time

from adafruit_dht import DHT22
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from board import D4
from dotenv import load_dotenv
from gpiozero import InputDevice

load_dotenv()

InputDevice(4, pull_up=True)
dhtDevice = DHT22(D4, use_pulseio=False)
start_time = time()

myAWSIoTMQTTClient = AWSIoTMQTTClient(environ.get("CLIENT_ID"))
myAWSIoTMQTTClient.configureEndpoint(
    environ.get("HOST_NAME"), int(environ.get("PORT")))
myAWSIoTMQTTClient.configureCredentials(
    "root-CA.crt",
    "temperatureSensor.private.key",
    "temperatureSensor.cert.pem")
myAWSIoTMQTTClient.connect()


def create_reading():
    try:
        if dhtDevice.temperature and dhtDevice.humidity:
            return {
                "clientId": environ.get("CLIENT_ID"),
                "timestamp": floor(
                    time()),
                "temperature": dhtDevice.temperature,
                "humidity": dhtDevice.humidity,
            }
        else:
            print({
                "clientId": environ.get("CLIENT_ID"),
                "timestamp": floor(
                    time()),
                "temperature": dhtDevice.temperature,
                "humidity": dhtDevice.humidity,
            })
            return create_reading()
    except BaseException as exception:
        print(exception)
        return create_reading()


def publish(readings, topic):
    try:
        myAWSIoTMQTTClient.publish(topic, dumps(readings), 1)
    except BaseException as exception:
        print(exception)
        publish(readings, topic)


def main():
    buffer = []
    seconds = 0
    while True:
        if(seconds == 60):
            seconds = 0
            publish(buffer, environ.get("TOPIC"))
            buffer = []
        if(seconds % 2 == 0):
            reading = create_reading()
            buffer.append(reading)
            # publish(reading)
        seconds = seconds + 1
        sleep(1 - (time() - start_time) % 1)


main()
