from time import sleep
from component import Component
from importlib import __import__
from mqtt import MQTT
from event import Event
from condition import Condition
from config import SERIAL


class Sensor(Component):
    def __init__(self, config):
        super().__init__(config)
        if config['library'] == 'gpiozero':
            self.instance = __import__(config['library'] + '_instance').Instance(config)
        else:
            self.instance = __import__(config['library']).Instance(config)
        self.freq = int(config['options']['freq'])
        self.mqtt = MQTT(config['name'])
        self.name = config['name']
        self.actions = config['actions']
        self.conditions = []
        self.events = []
        for action in self.actions:
            if action['type'] == 'event':
                e = Event(action, self.mqtt.publish_action)
                self.events.append(e)
                setattr(self.instance.get_instance(), action['data'], e.trigger_action)
            else:
                c = Condition(action, self.mqtt.publish_action)
                self.conditions.append(c)

        self.run = True

    def start(self):
        while self.run:
            try:
                resp = self.instance.read()
            except:
                continue
            for condition in self.conditions:
                condition.check_condition(resp[condition.data_trigger])
            try:
                self.mqtt.publish_data(resp)
            except:
                continue
            sleep(self.freq / 1000)
