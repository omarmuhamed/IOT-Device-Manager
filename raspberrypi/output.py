from mqtt import MQTT
from component import Component
from importlib import __import__
import json
from time import sleep


class OutputDevice(Component):
    def __init__(self, config):
        super().__init__(config)
        self.name = config['name']
        if config['library'] == 'gpiozero':
            self.instance = __import__(config['library'] + '_instance').Instance(config)
        else:
            self.instance = __import__(config['library']).Instance(config)
        self.mqtt = MQTT(config['name'])
        self.mqtt.subscribe(self.action_callback)
        self.mqtt.update_shadow({'state': self.instance.get_instance().value})
        self.prev_val = None
        self.run = True

    def action_callback(self, _, userdata, data):
        data = json.loads(data.payload)
        action = data['action']
        getattr(self.instance.get_instance(), action)()
        try:
            self.mqtt.update_shadow({'state': self.instance.get_instance().value})
        except:
            pass
