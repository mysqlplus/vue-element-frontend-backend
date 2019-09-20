---

## Description

This is an example of demo application that uses **django & django rest framework** as a backend and **vue.js** as a frontend.

demo from  open_galaxy application.  open_galaxy url(http://www.bdkry.com/open_galaxy/en/)


##author
 laoseng(QQ:1572665580),feilong(hhr66@qq.com)


## Environment

```
Centos 6
Python 3.6.1
mysql-server 5.6.21
node 9.4.0
Django==2.1.4
djangorestframework==3.9.0
```

## How to run

Clone the repository:

```zsh
    git clone git@github.com:DevOpsUnionTop/vue-element-frontend-backend.git
```

Create and activate virtualenv:

```zsh
➜  cd vue-element-frontend-backend
➜  virtualenv -p python3 env
➜  source env/bin/activate
```

Run scripts from Makefile that install all dependencies, run migrations and start dev server.

```zsh
(env) ➜  mysql -uroot -p -e "create database open_galaxy default charset utf8;"
(env) ➜  cp galaxy_demo/.env_example galaxy_demo/.env  @you will modify install_dir and port
(env) ➜  make init
(env) ➜  make dev
(env) ➜  make build-prod
(env) ➜  make start
```

Nginx config

```
product  use   demo.opengalaxy.com.conf
dev  use    demo.dev.opengalaxy.com.conf
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

username：admin   password：admin@123
