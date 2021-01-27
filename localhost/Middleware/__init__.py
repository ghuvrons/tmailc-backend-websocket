import json
f = open(__path__[0]+'/middleware.json')
middleware_list = json.load(f)
__import__(__name__,  globals=globals(), fromlist=middleware_list)
f.close()