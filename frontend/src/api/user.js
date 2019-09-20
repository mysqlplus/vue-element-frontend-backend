/*
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
* create:2018-09
* desc: 用户对象 api
*/
import request from '@/utils/request'

const UserUrl = '/users/user'
const UsersUrl = '/users/users'
const RolesUrl = '/users/roles'
const OtpsUrl = '/users/otps'

export const User = {
  info() {return request.get(`${UserUrl}/info/`).then(response => {return response.data})},
  create(params) {return request.post(`${UserUrl}/`, params).then(response => {return response.data})},
  modify(params) {return request.put(`${UserUrl}/modify/`, params).then(response => {return response.data})},
  patch(params) {return request.patch(`${UserUrl}/`, params).then(response => {return response.data})},
  change_password(params) {return request.put(`${UserUrl}/change_password/`, params).then(response => {return response.data})},
  email_reset_password(params) {return request.post(`${UserUrl}/email_reset_password/`, params).then(response => {return response.data})},
  reset_password(token, params) {return request.post(`${UserUrl}/reset_password/?token=${token}`, params).then(response => {return response.data})},
  send_sms_code(params) {return request.post(`${UserUrl}/send_sms_code/`, params).then(response => {return response.data})},
  login(params) {return request.post(`${UserUrl}/login/`, params).then(response => {return response.data})},
  phone_login(params) {return request.post(`${UserUrl}/phone_login/`, params).then(response => {return response.data})},
  logout(paramstr) {return request.get(`${UserUrl}/logout/?${paramstr}`).then(response => {return response.data})},
  //第三方
  social() {return request.get(`${UserUrl}/social/`).then(response => {return response.data})},
  del_social(params) {return request.post(`${UserUrl}/del_social/`, params).then(response => {return response.data})},
}

export const Users = {
  create(params) {return request.post(`${UsersUrl}/`, params).then(response => {return response.data})},
  delete(id) {return request.delete(`${UsersUrl}/${id}/delete`)},
  leaved(id) {return request.delete(`${UsersUrl}/${id}/leaved`)},
  update(id, params) {return request.put(`${UsersUrl}/${id}/`, params).then(response => {return response.data})},
  patch(id, params) {return request.patch(`${UsersUrl}/${id}/`, params).then(response => {return response.data})},
  get(id) {return request.get(`${UsersUrl}/${id}/`).then(response => {return response.data})},
  list(params) {return request.get(`${UsersUrl}/`, {params: params}).then(response => {return response.data})},
  get_users() {return request.get(`${UsersUrl}/get_users/`).then(response => {return response.data})},
}

export const Role = {
  get(id) {return request.get(`${RolesUrl}/${id}/`).then(response => {return response.data})},
  list(params) {return request.get(`${RolesUrl}/`, {params: params}).then(response => {return response.data})},
  add_user(id,params) {return request.post(`${RolesUrl}/${id}/add_user/`, params).then(response => {return response.data})},
  remove_user(id,params) {return request.post(`${RolesUrl}/${id}/remove_user/`, params).then(response => {return response.data})},
}

export const Otps = {
  create(params) {return request.post(`${OtpsUrl}/`, params).then(response => {return response.data})},
  delete(id) {return request.delete(`${OtpsUrl}/${id}/`)},
  update(id, params) {return request.put(`${OtpsUrl}/${id}/`, params).then(response => {return response.data})},
  patch(id, params) {return request.patch(`${OtpsUrl}/${id}/`, params).then(response => {return response.data})},
  get(id) {return request.get(`${OtpsUrl}/${id}/`).then(response => {return response.data})},
  list(params) {return request.get(`${OtpsUrl}/`, {params: params}).then(response => {return response.data})},
}
