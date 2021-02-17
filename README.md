# Cloudflare APP

> 软件名称：Cloudflare（或Cloudflare APP）
>
> 开发者 ：cxbsoft
>
> 适用平台 ：Android ， iOS ， 微信小程序
>
> 使用服务 ： [Cloudflare](https://cloudflare.com)
>
> 联系QQ ：3319066174
>
> QQ群 : 982909521
>
> Telegram : [@cxbsoft](https://t.me/cxbsoft)
>
> E-mail : cxbsoft@bsot.cn

## 应用介绍

本应用大部分功能通过调用Cloudflare官方API进行操作，能够实现以下功能：

1. 解析管理（添加、删除、修改），批量添加解析
2. 自定义安全规则（如加入黑名单等）
3. 更改防御等级（基本上没有、低、中、高、Under Attack 、关闭）（关闭功能仅限高级版本）
4. 一键将所有域名Under Attack,一键恢复
5. Cloudflare防火墙，可以自行搭建在自己服务器上进行防护，APP端管理
6. 访问数据统计
7. 服务器面板，集成服务器信息管理、计划任务、文件管理、Cloudflare防火墙
8. 下载管理，可以看到已从服务器下载的内容

还有功能在开发中 ...

## 安装方法

从Git仓库拿到server ：https://github.com/cxb-soft/cloudlfare_app

1. 打开安装目录

   ```bash
   sh install.sh
   ```

2. 等待依赖安装完成（pip3,python3的flask）

3. 根据```install.sh```安装向导完成安装

## 使用方法

1. 打开安装目录

2. 启动server.py

   ```shell
   python3 server.py
   ```

3. 服务端口为安装时输入的端口，连接密码是安装时输入的密码

#### Tip:

1. 若要开机启动请自行配置开机启动脚本，将```python3 server.py```放入
2. 防火墙日志文件在log.txt里（只有触发防火墙才会记录日志）
3. 如果无法访问服务器，请在系统防火墙放行配置的端口

> ### 使用方式
>
> 1.搭配Cloudflare APP使用
>
> 2.查看server.py有关api



---

### 更新说明
---

v1.1.0

1. 新增服务器面板功能

2. 服务器面板功能与Firewall功能合并

3. 新增计划任务功能（in 服务器面板）

4. 新增文件管理功能（查看、上传、删除、下载）(in 服务器面板)

5. 新增服务器监控功能(in 服务器面板)

6. 帮助文档更新(服务器面板部分，包括Firewall)

7. 新增下载管理

Server(最新版本下这个) : https://github.com/cxb-soft/cloudflare_app


---

v1.0.5

1. Cloudflare Firewall功能（服务器运行服务端，APP端连接）

2. 新增统计功能（统计请求状态码、国家访问次数、程序语言分类等）

3. 帮助文档(Firewall部分)

4. Cloudflare Firewall同步功能（从本地同步到账户、从账户同步到本地）

5.  用户页面更友好

6. 取消了一定要登录才能进入APP的设定

Firewall Github : https://github.com/cxb-soft/cloudflare_firewall

---

v 1.0.4

1. 新增Cloudflare防火墙服务，自行搭建服务端，APP端进行连接管理
---
v 1.0.1

1. 解析管理（添加、删除、修改），批量添加解析

2. 自定义安全规则（如加入黑名单等）

3. 更改防御等级（基本上没有、低、中、高、Under Attack 、关闭）（关闭功能仅限高级版本）

4. 一键将所有域名Under Attack,一键恢复