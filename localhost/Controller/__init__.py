import json
f = open(__path__[0]+'/controller.json')
controller_list = json.load(f)
__import__(__name__,  globals=globals(), fromlist=controller_list)
f.close()