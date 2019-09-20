<p align="center">
  <img width="320" src="https://wpimg.wallstcn.com/ecc53a42-d79b-42e2-8852-5126b810a4c8.svg">
</p>

<p align="center">
  <a href="https://github.com/vuejs/vue">
    <img src="https://img.shields.io/badge/vue-2.5.10-brightgreen.svg" alt="vue">
  </a>
  <a href="https://github.com/ElemeFE/element">
    <img src="https://img.shields.io/badge/element--ui-2.3.2-brightgreen.svg" alt="element-ui">
  </a>
  <a href="https://travis-ci.org/PanJiaChen/vue-element-admin" rel="nofollow">
    <img src="https://github.com/DevOpsUnionTop/vue-element-frontend-backend?branch=master" alt="Build Status">
  </a>
  <a href="https://github.com/PanJiaChen/vue-element-admin/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="license">
  </a>
</p>

[简体中文](./README_CN.md) | [English](./README.md)

## Introduction

[vue-element-frontend-backend](https://github.com/DevOpsUnionTop/vue-element-frontend-backend) is a production-ready front-end and back-end solution for admin interfaces.It based on [vue-element-admin](https://panjiachen.github.io/vue-element-admin/) and Back-end self-development[python+django+restful). Development and Improvement of Front Section Technology Based on vue-element-admin，the back-end code is developed with Python + Django and designed with restful architecture.

Privilege management：
	Back-end： Using RBAC mode，Using RBAC mode, Cooperating with Restful url + Method Operation to do back-end privilege authentication
	前段权限： according to the url list returned by the backend userinfo url,matching menu for front-end menu display or not,whether there is deletion inside or not, and updating permissions is mainly based on the specific URL permissions of the back end

demo example：
	cmdb demo： 
		front-end：Using avue build front-end Table management
		back-end：get_table_info api return avue arch, and  get list real datas
		Combination of the two to synthesize a table's add, delete, check, import and export functions with minimal code.


## Preparation

You need to install node and python3.6 locally. The project is based on [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin)-[vue,vuex,vue-router,vue-cli,axios,element-ui,avue], all request data is simulated using backend-python+django. Understanding and learning this knowledge in advance will greatly help the use of this project.

 <p align="center">
  <img width="900" src="https://wpimg.wallstcn.com/a5894c1b-f6af-456e-82df-1151da0839bf.png">
</p>

## Features

```
- Login / Logout and Third party login

- Multi-environment build
  - dev sit stage prod
- Global Features
  - I18n
  - Multiple dynamic themes
  - Dynamic sidebar (supports multi-level routing)
  - Dynamic breadcrumb
  - Tags-view (Tab page Support right-click operation)
  - Svg Sprite
  - Mock data
  - Screenfull
  - Responsive Sidebar

- Excel
  - Export Excel
  - Upload Excel

- Table
  - General table CRUD

- Error Page
  - 401
  - 404

- Components
  - Avatar Upload
  - Back To Top
  - Drag Dialog
  - Drag Select
  - Drag Kanban
  - Drag List
  - SplitPane
  - Dropzone
  - Sticky
  - CountTo
```

## Install Docs
[中文安装文档](./INSTALL_CN.md)
[English Docs](./INSTALL_EN.md)
