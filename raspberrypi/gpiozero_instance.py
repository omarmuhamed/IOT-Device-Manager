from gpiozero import *


class Instance:
    def __init__(self, config):
        if config['type'] == 'sensor':
            self.type = 'sensor'
            self.model = config['model']
            self.data = config['data']
            if config['model'] == 'hc-sr04':
                self.instance = DistanceSensor(echo=config['parameters']['echo'], trigger=config['parameters']['trigger'])
            elif config['model'] == 'ldr':
                self.instance = LightSensor(pin=config['parameters']['pin'])
            elif config['model'] == 'd-sun':
                self.instance = MotionSensor(pin=config['parameters']['pin'])

        elif config['type'] == 'output':
            self.type = 'output'
            self.comp = config['model']
            if config['model'] == 'led':
                self.instance = LED(pin=config['parameters']['pin'])
            elif config['model'] == 'pwmled':
                self.instance = PWMLED(pin=config['parameters']['pin'], frequency=config['parameters']['freq'])
            elif config['model'] == 'rgpled':
                self.instance = RGBLED(red=config['parameters']['red'], green=config['parameters']['green'], blue=config['parameters']['blue'])
            elif config['model'] == 'buzzer':
                self.instance = Buzzer(pin=config['parameters']['pin'])

    def read(self):
        if self.type == 'sensor':
            resp = {}
            for attr in self.data:
                if hasattr(self.instance, attr):
                    resp[attr] = getattr(self.instance, attr)
                    if attr == 'distance':
                        resp[attr] *= 100
                        resp[attr] = int(resp[attr])
                else:
                    resp[attr] = self.instance.value
            return resp

    def get_instance(self):
        return self.instance
