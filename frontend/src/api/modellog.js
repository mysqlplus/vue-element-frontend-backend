/*
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
* create:2018-09
* desc: modellog对象 api
*/
import request from '@/utils/request'

const LogSentryUrl = '/modellog/logsentrys'
const ModelUrl = '/modellog/models'

export const LogSentry = {
  get(id) {return request.get(`${LogSentryUrl}/${id}/`).then(response => {return response.data})},
  list(params) {return request.get(`${LogSentryUrl}/`, {params: params}).then(response => {return response.data})},
}

export const Model = {
  get(id) {return request.get(`${ModelUrl}/${id}/`).then(response => {return response.data})},
  list(params) {return request.get(`${ModelUrl}/`, {params: params}).then(response => {return response.data})},
}
