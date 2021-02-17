import os
import time
import json

def load_json(filename):
    f = open(filename)
    content = json.load(f)
    f.close()
    return content

config = load_json("config.json")
while(config['status'] == "on"):
    os.system("python3 firewall.py")
    time.sleep(config['time'])
    config = load_json("config.json")

print("Shut down")