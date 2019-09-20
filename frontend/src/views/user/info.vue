<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
-->
<template>
  <div class="components-container">
    <split-pane split="vertical" @resize="resize" :default-percent='60'>
      <template slot="paneL">
        <split-pane split="horizontal" :default-percent='53'>
          <template slot="paneL">
            <div class="top-container">
              <code style="padding: 3px 20px">修改用户用戶信息
              </code>
              <el-form ref="form" :model="form" label-width="120px" v-loading="listLoading" style="margin-top:-5px">
                <el-form-item prop="id" label="id" hidden>
                  <el-input
                    v-model="form.id"
                    name="id"
                    type="text"
                  />
                </el-form-item>
                <el-form-item prop="username" label="用户名">
                  <el-input
                    v-model="form.username"
                    name="username"
                    type="text"
                    auto-complete="on"
                    style="width: 50%"
                  />
                </el-form-item>
                <el-form-item prop="name" label="姓名">
                  <el-input
                    v-model="form.cname"
                    name="name"
                    type="text"
                    auto-complete="on"
                    style="width: 50%"
                  />
                </el-form-item>
                <el-form-item prop="email" label="邮箱">
                  <el-input
                    v-model="form.email"
                    name="email"
                    type="text"
                    auto-complete="on"
                    style="width: 50%"
                  />
                </el-form-item>
                <el-form-item prop="phone" label="手机号">
                  <el-input
                    v-model="form.phone"
                    name="phone"
                    type="text"
                    auto-complete="on"
                    style="width: 50%"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleUpdate">编辑</el-button><el-button v-if="form.otp_is_active==false" type="success" @click="handle2FA('on')">启用2FA(双因子认证)</el-button><el-button v-if="form.otp_is_active" type="danger" @click="handle2FA('off')">禁用2FA(双因子认证)</el-button>
                </el-form-item>
              </el-form>
            </div>
          </template>
          <template slot="paneR">
            <div class="bottom-container">
              <div class="top-container">
              <code style="padding: 3px 20px">
                第三方帐号绑定
              </code>
              <h4 class="provider-desc">可以使用以下表格中的第三方进行登录</h4>
              <br>
              <el-table
                v-loading="listLoading"
                :data="list"
                border
                fit
                highlight-current-row
                style="width: 100%;">
                <el-table-column :label="$t('table.id')" prop="id" align="center" width="65">
                  <template slot-scope="scope">
                    <span>{{ scope.row.id }}</span>
                  </template>
                </el-table-column>
                <el-table-column :label="$t('socialTable.provider')" align="center">
                  <template slot-scope="scope">
                    {{ scope.row.provider }}
                  </template>
                </el-table-column>
                <el-table-column :label="$t('socialTable.bindtime')" align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.auth_time }}</span>
                  </template>
                </el-table-column>
                <el-table-column :label="$t('socialTable.details')" align="center">
                  <template slot-scope="scope">
                    <span> <img :src="scope.row.img" style="height: 20px;width: 20px">{{ scope.row.details }} </span>
                  </template>
                </el-table-column>
                <el-table-column :label="$t('table.actions')" class-name="small-padding fixed-width" align="center">
                  <template slot-scope="scope">
                    <el-button type="danger" @click="handleDeleteSocial(scope.row.provider)" style="font-size: 10px">
                      {{ $t('socialTable.unbind') }}
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            </div>
          </template>
        </split-pane>
      </template>
      <template slot="paneR">
        <split-pane split="horizontal"  :default-percent='53'>
          <template slot="paneL">
            <AvatarUpload/>
          </template>
          <template slot="paneR">
            <div class="bottom-container">
              <code style="padding: 3px 20px">
                未绑定第三方
              </code>
              <h4 class="provider-desc">你还可以绑定以下第三方帐号</h4>
              <div class="social-signup-container">
                <div class="sign-btn" @click="handleSocialClick('weibo')" v-if="showweibo">
                  <span class="wb-svg-container"><svg-icon icon-class="weibo" class="icon"/></span> 微博
                </div>
                <div class="sign-btn" @click="handleSocialClick('github')" v-if="showgithub">
                  <span class="gh-svg-container"><svg-icon icon-class="github" class="icon"/></span> GitHub
                </div>
                <div class="sign-btn" @click="handleSocialClick('weixin')" v-if="showweixin">
                  <span class="wx-svg-container"><svg-icon icon-class="wechat" class="icon"/></span> 微信
                </div>
                <div class="sign-btn" @click="handleSocialClick('qq')" v-if="showqq">
                  <span class="qq-svg-container"><svg-icon icon-class="qq" class="icon"/></span> QQ
                </div>
              </div>
            </div>
          </template>
        </split-pane>
      </template>
    </split-pane>
  </div>
</template>

<script>
  import {isvalidUsername, isvalidPhone, validateEmail} from '@/utils/validate'
  import {User, Role} from '@/api/user'
  import {Message} from 'element-ui'
  import {AvatarUpload} from './components'
  import {openWindow, getSocialLoginUrl, formatDateTime} from '@/utils'
  import splitPane from 'vue-splitpane'

  export default {
    components: {
      AvatarUpload, splitPane
    },
    name: 'Login',
    data() {
      const validateUsername = (rule, value, callback) => {
        if (!isvalidUsername(value)) {
          callback(new Error('Please enter the correct user name'))
        } else {
          callback()
        }
      }
      const validateCname = (rule, value, callback) => {
        if (value.length < 2) {
          callback(new Error('Please enter the correct zh_name'))
        } else {
          callback()
        }
      }
      const validatePhone = (rule, value, callback) => {
        if (!isvalidPhone(value)) {
          callback(new Error('Please enter the correct phone'))
        } else {
          callback()
        }
      }
      const rvalidateEmail = (rule, value, callback) => {
        if (!validateEmail(value)) {
          callback(new Error('Please enter the correct email'))
        } else {
          callback()
        }
      }
      return {
        listLoading: true,
        showweibo: true,
        showweixin: true,
        showqq: true,
        showgithub: true,
        list: null,
        form: {
          id: this.$store.getters.user_id,
          username: '',
          cname: '',
          email: '',
          phone: '',
          otp_is_active: false,
        },
        registerRules: {
          cname: [{required: true, trigger: 'blur', validator: validateCname}],
          username: [{required: true, trigger: 'blur', validator: validateUsername}],
          phone: [{required: true, trigger: 'blur', validator: validatePhone}],
          email: [{required: true, trigger: 'blur', validator: rvalidateEmail}],
        }
      }
    },
    created() {
      this.getUser()
      this.getSocialList()
    },
    methods: {
      getUser() {
        this.listLoading = true
        User.info().then(response => {
          var user = response
          this.form.username = user.username
          this.form.cname = user.cname
          this.form.email = user.email
          this.form.phone = user.phone
          this.form.id = user.id
          this.form.otp_is_active = user.otp_is_active
          setTimeout(() => {
            this.listLoading = false
          }, 1 * 1000)
        })
      },
      handleUpdate() {
        this.$refs['form'].validate(valid => {
          if (valid) {
            this.loading = true
            this.$store.dispatch('UpdateUser', this.form).then(() => {
              this.loading = false
              Message({message: '更新成功!', type: 'success', duration: 2 * 1000})
              this.showDialog = false
            }).catch(() => {
              this.loading = false
            })
          } else {
            return false
          }
        })
      },
      handleDeleteSocial(provider) {
        this.listLoading = true
        var params = {}
        params['provider'] = provider
        User.del_social(params).then(response => {
          this.getSocialList()
          setTimeout(() => {
            this.listLoading = false
          }, 1 * 1000)
        })
      },
      handle2FA(action){
      },
      handleSocialClick(thirdpart) {
        const url = getSocialLoginUrl(thirdpart)
        document.location.href = url
      },
      resize() {

      },
      getSocialList() {
        this.listLoading = true
        this.showweibo = true
        this.showweixin = true
        this.showqq = true
        this.showgithub = true
        User.social().then(response => {
          var listtmp = []
          for (var i = 0; i < response.length; i++) {
            var obj = response[i]
            var tpobj = {}
            tpobj.id = obj.id
            tpobj.provider = obj.provider
            if (obj.provider == 'weibo') {
              this.showweibo = false
            } else if (obj.provider == 'weixin') {
              this.showweixin = false
            } else if (obj.provider == 'qq') {
              this.showqq = false
            }else if (obj.provider == 'github') {
              this.showgithub = false
            }
            tpobj.details = ''

            var edarr = obj.extra_data.split(',')

            for (var j = 0; j < edarr.length; j++) {
              if (edarr[j].indexOf("auth_time':") > 0) {
                tpobj.auth_time = formatDateTime(edarr[j].split(":")[1])
              } else if (edarr[j].indexOf("username':") > 0) {
                tpobj.details = edarr[j].split(":")[1].replace(/'/, '').replace(/'/, '')
              } else if (edarr[j].indexOf("profile_image_url':") > 0) {
                tpobj.img = edarr[j].split("':")[1].replace(/'/, '').replace(/'/, '')
              }
            }
            listtmp.push(tpobj)
          }
          this.list = listtmp
          setTimeout(() => {
            this.listLoading = false
          }, 1 * 1000)
        })
      },
    }
  }
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
  h4 {
    font-size: 1.071rem;
  }

  h4.provider-desc {
    margin: 0px;
  }

   info-code {
    padding: 3px 10px
  }


  .social-signup-container {
    margin: 20px 0;
    .sign-btn {
      display: inline-block;
      cursor: pointer;
    }
    .icon {
      color: #fff;
      font-size: 24px;
      margin-top: 8px;
    }
    .wx-svg-container,
    .gh-svg-container,
    .wb-svg-container,
    .qq-svg-container {
      display: inline-block;
      width: 40px;
      height: 40px;
      line-height: 40px;
      text-align: center;
      padding-top: 1px;
      border-radius: 4px;
      margin-bottom: 20px;
      margin-right: 5px;
    }
    .gh-svg-container {
      background-color: #14050f;
      margin-left: 30px;
    }
    .wx-svg-container {
      background-color: #8ada53;
      margin-left: 30px;
    }
    .wb-svg-container {
      background-color: #da0f1c;
      margin-left: 30px;
    }
    .qq-svg-container {
      background-color: #6BA2D6;
      margin-left: 30px;
    }
  }

  .components-container {
    position: relative;
    height: 110vh;
    margin: 10px 20px;
  }

  .left-container {
    height: 100%;
  }

  .right-container {
  }

  .top-container {
    width: 100%;
    height: 100%;
  }

  .bottom-container {
    width: 100%;
    height: 100%;
  }
</style>
