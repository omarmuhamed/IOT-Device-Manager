import json
import requests
from config import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from sensor import Sensor
from iot_camera import start
from stoppable_thread import StoppableThread
from output import OutputDevice
client = AWSIoTMQTTClient(SERIAL)

GOT_INIT_DATA = False
threads = {}


def deploy_component(name, config):
    if config['type'] == "sensor":
        if config['library'] == 'camera':
            if config['data']:
                pass
            else:
                start(config['name'])
        else:
            comp = Sensor(config)
            comp.start()
    else:
        comp = OutputDevice(config)


def init_libraries(_, userdata, data):
    global threads
    global GOT_INIT_DATA
    global client
    if not GOT_INIT_DATA:
        GOT_INIT_DATA = True
        data = json.loads(data.payload)
        components = {}
        for key, val in data.items():
            file = requests.get(val).content
            components[key] = json.loads(file)
        for key, val in components.items():
            th = StoppableThread(target=deploy_component, args=(key, val,), name=key)
            threads[key] = th
            th.start()


client.configureEndpoint(ENDPOINT, 8883)
client.configureCredentials('certs/AmazonRootCA1.pem', 'certs/private.pem.key', 'certs/certificate.pem.crt')
client.configureMQTTOperationTimeout(10)
client.connect()

client.publish(f'device/{SERIAL}/init', json.dumps({'serial': SERIAL}), 1)
client.subscribe(f'device/{SERIAL}/init_result', 1, init_libraries)


while 1:
    pass
