import os
import json
from datetime import datetime
import requests

def load_json(filename):
    f = open(filename)
    content = json.load(f)
    f.close()
    return content

def change_level(username,password,domain,level):
    
    url = "https://api.cloudflare.com/client/v4/zones/%s/settings/security_level?value=medium"%domain

    payload={
        "value" : "%s"%level
    }
    payload = json.dumps(payload)
    headers = {
    'content-type': 'application/json',
    'X-Auth-Email': username,
    'X-Auth-Key': password,
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response


def write_ip(ip):
    content = load_json("config.json")
    
    content['ips'].append(ip)
    content = json.dumps(content)
    f = open("config.json","w")
    f.write(content)
    f.close()

def fensuo(ip):
    command = "iptables -I INPUT -s %s -j DROP"%ip
    os.system(command)


def log(operate,method,content):
    if(operate =="write"):
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f = open("log.txt","a+")
        writecontent = "%s - %s : %s\n"%(nowtime,method,content)
        f.write(writecontent)
    else:
        f = open("log.txt","rb")
        pass
    f.close()

def get_max_ip():
    f= os.popen("awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr -k1 | head -n 1")
    content = f.read()
    content = content.strip()
    content = content.split("\n")[0]
    content = content.split(" ")[1]
    return content

def get_load():
    f = os.popen("uptime | sed 's/,//g' | awk '{print $11,$12,$13}'")
    str_aver_load = f.read().strip().split(" ")[1].strip()
    return str_aver_load

config = load_json("config.json")
load = config['load']
mode = config['mode']
method = config['method']
ips = config['ips']
cloudflare = config['cloudflare']

if(mode == "load"):
    max_load = load['max_value']
    print("Load mode activated")
    nowload = get_load()
#    log("write","INFO","当前负载 : %s"%(nowload))
    if(nowload >= max_load):
        dirt = float(nowload) - float(max_load)
        log("write","WARNING","超出负载值 : %.2f"%(dirt))
        if(method == "ip"):
            maxip = get_max_ip()
            if(maxip in ips):
                pass
            else:
                fensuo(maxip)
                log("write","INFO","威胁IP : %s，已封禁"%(maxip))
                write_ip(maxip)
        elif(method == "under_attack"):
            username = cloudflare['username']
            password = cloudflare['password']
            domains = config['protect_domains']
            print(cloudflare)
            for domain in domains:
                change_level(username,password,domain,"under_attack")
            log("write","INFO","开启Under Attack模式")

