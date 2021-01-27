import json
f = open(__path__[0]+'/service.json')
service_dict = json.load(f)
f.close()
service_list = [service_dict[s] for s in service_dict]
__import__(__name__,  globals=globals(), fromlist=service_list)