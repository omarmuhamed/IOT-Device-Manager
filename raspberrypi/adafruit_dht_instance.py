from adafruit_dht import DHT11, DHT22
import board


class Instance:
    def __init__(self, config):
        if config['model'] == "DHT11":
            self.dht = DHT11(getattr(board, 'D' + str(config['parameters']['pin'])))
        else:
            self.dht = DHT22(getattr(board, 'D' + str(config['parameters']['pin'])))
        self.data = config['data']

    def read(self):
        resp = {}
        for attr in self.data:
            resp[attr] = getattr(self.dht, attr)
        return resp
