import operator


class Condition:
    def __init__(self, config, mqtt_publish_action):
        self.condition = config['condition']
        self.target_value = int(config['value'])
        self.data_trigger = config['data']
        self.target_device = config['target']
        self.action = config['action']
        self.mqtt_publish_action = mqtt_publish_action

    def check_condition(self, val):
        try:
            if getattr(operator, self.condition)(val, self.target_value):
                self.trigger_action()
        except:
            pass

    def trigger_action(self):
        self.mqtt_publish_action(self.target_device, self.action)