class Event:
    def __init__(self, config, mqtt_publish_action):
        self.target = config['target']
        self.action = config['action']
        self.mqtt_publish_action = mqtt_publish_action

    def trigger_action(self):
        self.mqtt_publish_action(self.target, self.action)