/**
 * author:laoseng,feilong
 * create:2018-07
 *  user信息存储
 */
import {Login, logout, registerUser, updateUser, User} from '@/api/user'
import {getToken} from '@/utils/auth'

const user = {
  state: {
    user: '',
    status: '',
    code: '',
    token: getToken(),
    name: '',
    username: '',
    id: '',
    avatar: '',
    introduction: '',
    roles: [],
    urls: [],
    setting: {
      articlePlatform: []
    }
  },

  mutations: {
    SET_ID: (state, id) => {
      state.id = id
    },
    SET_CODE: (state, code) => {
      state.code = code
    },
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_INTRODUCTION: (state, introduction) => {
      state.introduction = introduction
    },
    SET_SETTING: (state, setting) => {
      state.setting = setting
    },
    SET_STATUS: (state, status) => {
      state.status = status
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_USERNAME: (state, username) => {
      state.username = username
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_URLS: (state, urls) => {
      state.urls = urls
    },
    SET_USER: (state, user) => {
      state.user = user
    }
  },

  actions: {
    // 用户名登录
    LoginByUsername({commit}, userInfo) {
      return new Promise((resolve, reject) => {
        User.login(userInfo).then(response => {
          const data = response
          commit('SET_TOKEN', data.token)
          //setToken(data.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    LoginPhone({commit}, userInfo) {
      return new Promise((resolve, reject) => {
        User.phone_login(userInfo).then(response => {
          const data = response
          commit('SET_TOKEN', data.token)
          //setToken(data.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    RegisterUser({commit}, userInfo) {
      return new Promise((resolve, reject) => {
        User.create(userInfo).then(response => {
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    UpdateUser({commit}, userInfo) {
      return new Promise((resolve, reject) => {
        User.modify(userInfo).then(response => {
          const data = response
          commit('SET_USER', userInfo)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 获取用户信息
    GetUserInfo({commit}) {
      return new Promise((resolve, reject) => {
        User.info().then(response => {
          const data = response
          commit('SET_ROLES', data.roles)
          // if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
          //   commit('SET_ROLES', data.roles)
          // } else {
          //   reject('getInfo: roles must be a non-null array !')
          // }
          var j = 0
          var urls = []
          for (; j < data.urls.length; j++) {
            urls.push(data.urls[j].url)
          }
          commit('SET_URLS', urls)
          // if (data.urls && data.urls.length > 0) { // 验证返回的roles是否是一个非空数组
          //   var j=0
          //   var urls=[]
          //   for(;j<data.urls.length;j++){
          //     urls.push(data.urls[j].url)
          //   }
          //   commit('SET_URLS', urls)
          // } else {
          //   reject('getInfo: urls must be a non-null array !')
          // }
          commit('SET_USERNAME', data.username)
          commit('SET_ID', data.id)
          commit('SET_AVATAR', data.avatar)
          commit('SET_INTRODUCTION', data.introduction)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },
    LogOut({commit},paramstr) {
      return new Promise((resolve, reject) => {
          commit('SET_TOKEN', '')
          commit('SET_ROLES', [])
        User.logout(paramstr).then(response => {
          //removeToken()
          resolve()
        })
      })
    },
    // 前端 登出
    FedLogOut({commit}) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        //removeToken()
        resolve()
      })
    },

    // 动态修改权限
    ChangeRoles({commit, dispatch}, role) {
      return new Promise(resolve => {
        //commit('SET_TOKEN', role)
        //setToken(role)
        User.info(role).then(response => {
          const data = response.data
          commit('SET_ROLES', data.roles)
          commit('SET_NAME', data.name)
          commit('SET_AVATAR', data.avatar)
          commit('SET_INTRODUCTION', data.introduction)
          dispatch('GenerateRoutes', data) // 动态修改权限后 重绘侧边菜单
          resolve()
        })
      })
    },
    ChangeAvatar({commit}, avatar) {
      return new Promise(resolve => {
        commit('SET_AVATAR', avatar)
        resolve()
      })
    },
    EmailResetPwd({commit}, userInfo) {
      return new Promise((resolve, reject) => {
        User.email_reset_password(userInfo).then(response => {
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
  }
}


export default user
