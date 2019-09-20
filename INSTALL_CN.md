---

## 描述

该项目 是open_galaxy的demo版本，open_galaxy项目使用python+django+vue+restful 技术以及框架。 demo版本是 项目的一个简化版本，技术框架一样。
open_galaxy项目请查看 http://www.bdkyr.com/open_galaxy/cn/

##作者
 老僧(QQ:1572665580),飞龙(hhr66@qq.com)

## 环境

```
Centos 6
Python 3.6.1
mysql-server 5.6.21
node 9.4.0
Django==2.1.4
djangorestframework==3.9.0
```

## 如何运行

Clone the repository:

```zsh
➜ git clone git@gitlab.opengalaxy.com/open_galaxy_demo.git
```

创建 and 激活 virtualenv:

```zsh
➜  virtualenv -p python3 env
➜  source env/bin/activate
```

Run scripts from Makefile that install all dependencies, run migrations and start dev server.

```zsh
(env) ➜  mysql -uroot -p -e "create database open_galaxy default charset utf8;"
(env) ➜  cp galaxy_demo/.env_example galaxy_demo/.env  #可以修改 默认安装目录以及端口
(env) ➜  make init
(env) ➜  make dev
(env) ➜  make build-prod
(env) ➜  make start
```

Nginx 配置文件 --

```
生产  请使用  项目中  demo.opengalaxy.com.conf     配置文件
开发  请使用  项目中  demo.dev.opengalaxy.com.conf 配置文件
```

We are done.

dev

- Frontend: http://localhost:9527/
- Backend: http://localhost:8004/

prod

- Frontend: http://demo.opengalaxy.com/
- Backend: http://demo.opengalaxy.com/api/
- Xadmin: http://demo.opengalaxy.com/xadmin/
- API Docs: http://demo.opengalaxy.com/docs/

默认管理员账号：admin   密码：admin@123
