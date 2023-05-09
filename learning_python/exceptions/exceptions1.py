import traceback

try:
    json_sample = {'token': 'This is your token',
                   'number': 123}
    TOKEN = json_sample['token1']

except KeyError as e:
    print(traceback.format_exc())
    print(repr(e))