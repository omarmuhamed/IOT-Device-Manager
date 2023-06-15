from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from config import ENDPOINT, SERIAL
import json
from time import sleep


class MQTT:
    def __init__(self, client_id):
        self.component = client_id
        self.topic = f'device/{SERIAL}/component/{client_id}'
        self.client = AWSIoTMQTTClient(SERIAL + '_' + client_id)
        self.client.configureEndpoint(ENDPOINT, 8883)
        self.client.configureCredentials('certs/AmazonRootCA1.pem', 'certs/private.pem.key', 'certs/certificate.pem.crt')
        self.client.configureMQTTOperationTimeout(3)
        self.client.connect()

    def update_state(self):
        pass

    def publish_data(self, data):
        self.client.publish(self.topic + '/data', json.dumps(data), 1)

    def publish(self, topic, data):
        self.client.publish(topic, json.dumps(data), 1)

    def subscribe(self, cb):
        self.client.subscribe(self.topic + '/action', 1, cb)

    def publish_action(self, target, action):
        self.publish(f'device/{SERIAL}/component/{target}/action', {'action': action})

    def update_shadow(self, desired):
        self.publish(f"$aws/things/{SERIAL}_{self.component}/shadow/update", {'state': {'desired': desired}})