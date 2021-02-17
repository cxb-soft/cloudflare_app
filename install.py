#install.py

import json

# Init
configs = []

print("Welcome to CX install system - For Cloudflare Firewall") # Welcome

# Config
port = int(input("服务端口(默认65500):"))
connect_password = input("设置连接密码(连接时用):")
cloudflare_username = input("Cloudflare用户邮箱(如不配置将无法使用防火墙的Under Attack式，不配置就留空):")
cloudflare_password = input("Cloudflare密钥(Cloudflare官网获取Global API KEY):")
# Config ok

f = open("config.json","rb")
config = f.read()
f.close()
config = json.loads(config)
if(port != ""):
    config['port'] = port
else:
    config['port'] = 65500
config['cloudflare']['username'] = cloudflare_username
config['cloudflare']['password'] = cloudflare_password
config['password'] = connect_password

f = open("config.json","w")
f.write(json.dumps(config))
f.close()

# Complete

print("Install successfully .")
