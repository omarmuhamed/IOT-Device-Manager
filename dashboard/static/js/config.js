const conditions = {
    "-1": [],
    0: [
        {
            'name': 'lt',
            'visiblename': 'Less than'
        },
        {
            'name': 'gt',
            'visiblename': 'Greater than'
        },
        {
            'name': 'eq',
            'visiblename': 'Equals'
        },
        {
            'name': 'ne',
            'visiblename': 'Not equals'
        }
    ]
}
const components = {
    "-1": {
        "type": "",

        "parameters": [],
        "options": [],
        "data": [],
        "events": [],
    },
    "camera": {
        'type': 'sensor',
        'data': [
            {
                'name': 'type',
                'visiblename': "Face Detection",
                'type': 1
            }
        ],
        'events': [
        ],
        "options": [],
        "parameters": []
    },
    "hc-sr04": {
        'type': 'sensor',
        "parameters": [
            {
                "name": 'trigger',
                "visiblename": 'Trigger Pin',
            },
            {
                "name": 'echo',
                "visiblename": 'Echo Pin',
            }

        ],
        "data": [
            {
                'name': 'distance',
                'visiblename': 'Distance',
                'type': 0
            }
        ],
        "options": [
            {
                "name": 'freq',
                "visiblename": "Frequency ms",
                "type": 'numerical'
            }
        ],

    },
    "dht11": {
        "type": "sensor",
        "parameters": [
            {
                "name": "pin",
                "visiblename": "Pin",
                "type": "numerical"
            },
        ],
        "data": [
            {
                'name': 'humidity',
                'visiblename': 'Humidity',
                'type': 0
            },
            {
                'name': 'temperature',
                'visiblename': 'Temperature',
                'type': 0
            }
        ],
        "options": [
            {
                "name": 'freq',
                "visiblename": "Frequency ms",
                "type": 'numerical'
            }
        ],
    },
    "led": {
        'type': 'output',
        "parameters": [
            {
                "name": "pin",
                "visiblename": "Pin",
                "type": "numerical"
            }
        ],
        'options': [],
        'data': [],
        'slots': [
            {
                'name': 'on',
                'visiblename': 'Turn On'
            },
            {
                'name': 'off',
                'visiblename': 'Turn Off'
            },
            {
                'name': 'toggle',
                'visiblename': "Toggle"
            }
        ]
    },
    "ldr": {
        "type": "sensor",
        "parameters": [
            {
                "name": "pin",
                "visiblename": "Pin",
                "type": "numerical"
            },
        ],
        "data": [
            {
                'name': 'value',
                'visiblename': 'Luminous',
                'type': 0
            }
        ],
        "options": [
            {
                "name": 'freq',
                "visiblename": "Frequency ms",
                "type": 'numerical'
            }
        ],
        "events": [
            {
                "name": "when_light",
                "visiblename": "Light"
            },
            {
                "name": "when_dark",
                "visiblename": "Dark"
            }
        ]
    },
    "d-sun": {
        "type": "sensor",
        "parameters": [
            {
                "name": "pin",
                "visiblename": "Pin",
                "type": "numerical"
            },
        ],
        "data": [
            {
                'name': 'value',
                'visiblename': 'Motion (0 or 1)',
                'type': 0
            }
        ],
        "options": [
            {
                "name": 'freq',
                "visiblename": "Frequency ms",
                "type": 'numerical'
            }
        ],
        "events": [
            {
                "name": "when_motion",
                "visiblename": "Motion Detected"
            },
            {
                "name": "when_no_motion",
                "visiblename": "No Motion Detected"
            }
        ]
    },
    "buzzer": {
        'type': 'output',
        "parameters": [
            {
                "name": "pin",
                "visiblename": "Pin",
                "type": "numerical"
            }
        ],
        'options': [],
        'data': [],
        'slots': [
            {
                'name': 'on',
                'visiblename': 'Turn On'
            },
            {
                'name': 'off',
                'visiblename': 'Turn Off'
            },
            {
                'name': 'toggle',
                'visiblename': "Toggle"
            }
        ]
    },
}

const icons = {
    'led': 'bi bi-lightbulb',
    'hc-sr04': 'bi bi-rulers',
    'ldr': 'bi bi-brightness-high',
    'dht11': 'bi bi-thermometer-sun',
    'camera': 'bi bi-camera',
    'buzzer': 'bi bi-bell',
    'd-sun': 'bi bi-cpu-fill'
}