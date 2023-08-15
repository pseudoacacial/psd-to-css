psd_location = 'test/example.psd'
scheme = [
    {'selector': '.logo', 'name': 'logo', },
    {'selector': '.text-1', 'name': 'text here'},
    {'selector': '.text-2', 'name': 'text positioned relatively to other layer/group', 'frame': 'Group 1'},
    {'selector': '.button', 'name': '^cta', 'text': True, 'border': True},
    {'selector': '.kv', 'name': 'surprisedPikachu', 'export': {'extension': 'png'}},
    {'selector': False, 'name': 'photo', 'export': {'name': 'bg', 'extension': 'png', 'clip': True}}
]
