/**
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
* create:2018-07
 *  异步统一request封装
 */
import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'
import router from '@/router'
import {getDomain} from '@/utils'

const service = axios.create({
  baseURL: getDomain() + '/api/v1', // api 的 base_url
  timeout: 10000, // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // Do something before request is sent
    if (store.getters.token) {
      // 让每个请求携带token-- ['X-Token']为自定义key 请根据实际情况自行修改
      // config.headers['X-Token'] = getToken()
      config.headers['Authorization'] = 'JWT ' + getToken()
    }
    return config
  },
  error => {
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => response,
  error => {
    var message = ''
    console.log("=====>",error.response.status)
    switch (error.response.status) {
      case 401:
        message = '未授权，请登录!'
        break
      case 403:
        message = '无权限!'
        break
      case 400:
        if (error.response.config.url.indexOf('/login') >= 0) {
          message = '用户名密码错误!'
        } else {
          for(var key in error.response.data){//遍历json对象的每个key/value对,p为key
            message=error.response.data[key][0]
          }
        }
        break
      case 404:
        message = '请求不存在!'
        break
      case 500:
        var errmsg=""
        if(error.response.hasOwnProperty("detail")){
          errmsg=error.response.hasOwnProperty("detail")
        }
        message = '服务异常:'+errmsg
        break
      case 502:
        var errmsg=""
        if(error.response.hasOwnProperty("detail")){
          errmsg=error.response.hasOwnProperty("detail")
        }
        message = '服务异常:'+errmsg
        break
      default:
        message = 'Oops, 出错啦!'
    }
    Message({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
