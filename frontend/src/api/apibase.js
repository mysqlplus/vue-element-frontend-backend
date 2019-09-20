/*
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
* create:2018-09
* desc: 基础共用 api
*/

import request from '@/utils/request'

export const ApiBase = {
  create(uri,params) {return request.post(`${uri}/`, params).then(response => {return response.data})},
  delete(uri,id) {return request.delete(`${uri}/${id}/`)},
  update(uri,id, params) {return request.put(`${uri}/${id}/`, params).then(response => {return response.data})},
  patch(uri,id, params) {return request.patch(`${uri}/${id}/`, params).then(response => {return response.data})},
  get(uri,id) {return request.get(`${uri}/${id}/`).then(response => {return response.data})},
  list(uri,params) {return request.get(`${uri}/`, {params: params}).then(response => {return response.data})},
  get_table_info(uri) {return request.get(`${uri}/get_table_info/`).then(response => {return response.data})},
}
