from flask import Flask,send_file,make_response
from urllib.parse import quote
from flask import request
import json
import time
import os
import psutil


def load_json(filename):
    f = open(filename)
    content = json.load(f)
    f.close()
    return content

def download_file(file_path):
    return send_file(file_path,as_attachment=True)


def write_json(filename,content):
    content = json.dumps(content)
    f = open(filename,"w")
    f.write(content)
    f.close()



def delete_crontab_func(command):
    print("going")
    os.system("cp /etc/crontab ./contab_backup")
    crontab = open("/etc/crontab","r")
    content = crontab.read()
    crontab.close()
    content = content.replace(command + "\n\n", "", 1)
    crontab = open('/etc/crontab','w')
    crontab.write(content)
    crontab.close()
    os.system("service cron reload")
    os.system("service crond reload")
    return command



def add_crontab_go(command):
    if(len(command) == 0):
        return command
    os.system("cp /etc/crontab ./contab_backup")
    crontab = open("/etc/crontab","a+")
    crontab.write(command + "\n")
    crontab.write("\n")
    crontab.close()
    os.system("service cron reload")
    os.system("service crond reload")
    return command



def unblock(ip):
    os.system("iptables -D INPUT -s %s -j DROP"%ip)
    configs = load_json("config.json")
    configs['ips'].remove(ip)
    write_json("config.json",configs)



def change_password_func(new_password):
    configs = load_json("config.json")
    configs['password'] = new_password
    write_json("config.json",configs)

def read_file(file_path):
    f = open(file_path,"r")
    content = f.read()
    f.close()
    return content

def get_server_info_uptime():
    f = os.popen("uptime")
    uptime = f.read()
    uptime = uptime[:-1]
    uptime = uptime.strip().split(" up ")
    uptime[1] = uptime[1].split(",")
    j = 0
    uptime1 = uptime[1]
    for item in uptime1:
        uptime[1][j] = item.strip().split(" ")
        if(uptime[1][j][0] == "load"):
            uptime[1][j][0] = uptime[1][j][2]
        j += 1
    return uptime



def time_change_func(newtime):
    configs = load_json("config.json")
    configs['time'] = newtime
    write_json("config.json",configs)



def get_info_function():
    f = os.popen("cat /proc/meminfo")
    content = f.read().split("\n")
    content.pop()
    x = 0
    data = {}
    for item in content:
        item = item.split(":")
        item[1] = item[1].strip()
        key = item[0]
        value = item[1]
        if("kB" in value):
            value = value.split(" ")
            value[0] = int(value[0])/1000
            value[1] = "MB"
        data[key] = value
        x += 1
    data['DETAIL'] = get_server_info_uptime()
    data['cpu'] = get_cpu()
    data['netio'] = get_net_io()
    data['crontab'] = get_crontab()
    return data



def get_net_io():
    info = psutil.net_io_counters()
    sentio = round(info.bytes_sent/1000/1000,2)
    recvio = round(info.bytes_recv/1000/1000,2)
    return {
        "sent" : sentio,
        "recv" : recvio
    }



def get_crontab():
    crontab = open("/etc/crontab","r")
    content = crontab.read().split("\n")
    crontab.close()

    x = 0
    j = 0
    for item in content:
        if("# *  *  *  *  *" in item):
            j = x
        if(len(item) == 0):
            content.remove(item)
        x += 1
    content = content[j+1:-1]
    return content



def get_cpu():
    cpu = os.popen("top -bi -n 2 -d 0.02")
    cpu = cpu.read().strip().split("\n")
    cpu[2] = cpu[2].strip().split(" ")
    x = 0
    for data in cpu[2]:
        if(data == ""):
            cpu[2].pop(x)
        x += 1
    cpu[2][0] = cpu[2].index("id,") - 1
    return cpu
    
def delete_file_func(filepath):
    os.remove(filepath)
    return filepath

def status(method):
    configs = load_json("config.json")
    if(method == "start"):
        if(configs['status'] == "on"):
            pass
        else:
            configs['status'] = "on"
            write_json("config.json",configs)
            os.system("nohup python3 main.py &")
    else:
        if(configs['status'] == "off"):
            pass
        else:
            configs['status'] = "off"
    write_json("config.json",configs)


def filepath_get_func(target):
    result_file = []
    result_pack = []
    result_file_nohide = []
    result_pack_nohide = []
    for filename in os.listdir(target):
        isfile = os.path.isfile(target + "" + filename)
        if(isfile == True):
            if(filename[0] == '.'):
                pass
            else:
                result_file.append(
                    {
                        "filename" : filename,
                        "path_type" : isfile
                    }
                )
            result_file_nohide.append(
                {
                    "filename" : filename,
                    "path_type" : isfile
                }
            )
        else:
            if(filename[0] == '.'):
                pass
            else:
                result_pack.append(
                    {
                        "filename" : filename,
                        "path_type" : isfile
                    }
                )
            result_pack_nohide.append(
                {
                    "filename" : filename,
                    "path_type" : isfile
                }
            )
        
    return {
        "file" : result_file,
        "pack" : result_pack,
        "file_nohide" : result_file_nohide,
        "pack_nohide" : result_pack_nohide
    }


app = Flask(__name__)



configs = load_json("config.json")
port = configs['port']



# Ping check online
@app.route('/online',methods=['GET'])
def online():
    return {
        "success" : True,
        "online" : True
    }



# Set config
@app.route('/config',methods=['POST'])
def config():
    postdata = request.form['config']
    postdata = json.loads(postdata)
    write_json("config.json",postdata)
    print(postdata)
    return postdata



# 获取当前配置
@app.route('/config_read',methods=['GET'])
def config_read():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        return {
            "success" : True,
            "detail" : configs
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



# 开启防火墙服务
@app.route('/start',methods=['GET'])
def start():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        status("start")
        return {
            "success" : True,
            "msg" : "Firewall is start now"
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



# 关闭防火墙服务
@app.route('/stop',methods=['GET'])
def stop():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        status("stop")
        return {
            "success" : True,
            "msg" : "Firewall is stop now"
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



# 改密码
@app.route('/change_password',methods=['GET'])
def change_password():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    newpassword = request.args.get("newpassword")
    if(reqpass == password):
        change_password_func(newpassword)
        return {
            "success" : True,
            "msg" : "Password change successful ."
        }
    else:
        return {
            "success" : False,
            "error" : "Old password incorrect ."
        }



# 改防火墙检测时间
@app.route('/time_change',methods=['GET'])
def time_change():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        newtime = request.args.get("newtime")
        newtime = int(newtime)
        time_change_func(newtime)
        return {
            "success" : True,
            "msg" : "Time changed ."
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



# 解封IP
@app.route('/unblock_ip',methods=['GET'])
def unblock_ip():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        unblock_target = request.args.get("ip")
        unblock(unblock_target)
        return {
            "success" : True,
            "ip" : unblock_target
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



# 读取服务器数据
@app.route('/get_info',methods=['GET'])
def get_info():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        return {
            "success" : True,
            "msg" : get_info_function(),
            
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



# 添加Crontab
@app.route('/add_crontab',methods=['GET'])
def add_crontab():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        command = request.args.get('command')
        return {
            "success" : True,
            "command" : add_crontab_go(command)
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



# 删除Crontab
@app.route('/delete_crontab',methods=['GET'])
def delete_crontab():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        target = request.args.get('command')
        return {
            "success" : True,
            "target" : delete_crontab_func(target)
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }

# -----------------------------------------------------------------------------------
# 文件管理
# -----------------------------------------------------------------------------------

# 获取目录
@app.route('/filepath_get',methods=['GET'])
def filepath_get():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        target = request.args.get('file_path')
        return {
            "success" : True,
            "result" : filepath_get_func(target)
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }

# 读取文件
@app.route('/file_read',methods=['GET'])
def file_read():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        target = request.args.get('file_path')
        return {
            "success" : True,
            "result" : read_file(target)
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }


# 下载文件
@app.route('/download',methods=['GET'])
def download():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        target = request.args.get('file_path')
        target_list = target.split("/")
        filename = target_list[-1]
        response = make_response(send_file(target))
        response.headers["Content-Disposition"] = "attachment; filename={0}; filename*=utf-8''{0}".format(
            quote(filename))
        return response
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }


# 上传文件
@app.route('/upload_file',methods=['GET','POST'])
def upload_file():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        #files = request.files
        #files = 124
        files = request.files['file']
        filepath = request.args.get('file_path')
        files.save(filepath)
        return {
            "success" : True,
            "result" : filepath
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }


# 删除文件
@app.route('/delete_file',methods=['GET'])
def delete_file():
    configs = load_json("config.json")
    password = configs['password']
    reqpass = request.args.get("password")
    if(reqpass == password):
        filepath = request.args.get('filepath')
        return {
            "success" : True,
            "result" : delete_file_func(filepath)
        }
    else:
        return {
            "success" : False,
            "error" : "Auth error : Password incorrect!"
        }



if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=port)