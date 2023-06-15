comp_configs = {
    "hc-sr04": {
        "name": "",
        "library": "gpiozero",
        "type": "sensor",
        "model": "hc-sr04",
        "parameters": {
            "trigger": None,
            "echo": None
        },
        "data": ["distance"],
        "options": {
            "freq": None
        },
    },
    "d-sun": {
        "name": "",
        "library": "gpiozero",
        "type": "sensor",
        "model": "d-sun",
        "parameters": {
            "pin": None
        },
        "data": ["motion"],
        "options": {
            "freq": None
        },
    },
    "ldr": {
        "name": "",
        "library": "gpiozero",
        "type": "sensor",
        "model": "ldr",
        "parameters": {
            "pin": None
        },
        "data": ["value"],
        "options": {
            "freq": None
        },
    },
    "dht11": {
        "name": "",
        "library": "adafruit_dht",
        "type": "sensor",
        "model": "DHT11",
        "parameters": {
            "pin": None
        },
        "data": ["temperature", "humidity"],
        "options": {
            "freq": None
        },
    },
    "led": {
        "name": "",
        "library": "gpiozero",
        "type": "output",
        "model": 'led',
        "parameters": {
            "pin": None
        }
    },
    "buzzer": {
        "name": "",
        "library": "gpiozero",
        "type": "output",
        "model": 'buzzer',
        "parameters": {
            "pin": None
        }
    },
    "camera": {
        "name": "",
        "library": "camera",
        "type": "sensor",
        "parameters": {}
    }
}

data = {
    'distance': 'Distance',
    'temperature': 'Temperature',
    'humidity': 'Humidity',
    'value': 'Luminous'
}

icons = {
    'led': 'bi bi-lightbulb',
    'hc-sr04': 'bi bi-rulers',
    'ldr': 'bi bi-brightness-high',
    'dht11': 'bi bi-thermometer-sun',
    'camera': 'bi bi-camera',
    'buzzer': 'bi bi-bell',
    'd-sun': 'bi bi-cpu-fill'
}