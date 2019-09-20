<!--
  * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
-->
<template>
  <div class="login-container">

    <div class="title-container">
      <h3 class="title">{{ $t('login.title') }}</h3>
      <lang-select class="set-language"/>
    </div>
    <div class="test">
      <div class="testNav">
        <div :class="{'selected':tab === 1,'testTitle':true}" @click="toTab(1)">{{ $t('login.loginpwdtitle') }}</div>
        <div :class="{'selected':tab === 2,'testTitle':true}" @click="toTab(2)">{{ $t('login.loginphonetitle') }}</div>
      </div>
      <div class="container">
        <keep-alive>
          <div v-if="tab === 1">
            <el-form
              ref="loginForm"
              :model="loginForm"
              :rules="loginRules"
              class="login-form"
              auto-complete="on"
              label-position="left">

              <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user"/>
        </span>
                <el-input
                  v-model="loginForm.username"
                  :placeholder="$t('login.username')"
                  name="username"
                  type="text"
                  auto-complete="on"
                />
              </el-form-item>

              <el-form-item prop="password">
                <span class="svg-container">
                  <svg-icon icon-class="password"/>
                </span>
                <el-input
                  :type="passwordType"
                  v-model="loginForm.password"
                  :placeholder="$t('login.password')"
                  name="password"
                  auto-complete="on"
                  @keyup.enter.native="handleLogin"/>
                <span class="show-pwd" @click="showPwd">
                    <svg-icon icon-class="eye"/>
                  </span>
              </el-form-item>

              <el-button
                :loading="loading"
                type="primary"
                style="width:100%;margin-bottom:30px;"
                @click.native.prevent="handleLogin">{{ $t('login.logIn') }}
              </el-button>

              <el-button class="resetpwd-button" type="primary" @click="showResetPwdDialog=true">
                {{ $t('login.resetPwd') }}
              </el-button>

              <el-button class="register-button" type="primary" @click="showRegisterDialog=true">
                {{ $t('login.register') }}
              </el-button>
              <el-button class="thirdparty-button" type="primary" @click="showDialog=true">
                {{ $t('login.thirdparty') }}
              </el-button>
            </el-form>
          </div>
          <div v-else>
            <el-form
              ref="loginPhoneForm"
              :model="loginPhoneForm"
              :rules="loginPhoneRules"
              class="login-form"
              auto-complete="on"
              label-position="left">

              <el-form-item prop="phone">
                <el-input
                  v-model="loginPhoneForm.phone"
                  :placeholder="$t('login.phone')"
                  name="username"
                  type="text"
                  auto-complete="on" style="height: 35px;"
                />
              </el-form-item>

              <el-form-item prop="sms_code">
                <el-col style="width: 56%">
                  <el-input
                    v-model="loginPhoneForm.sms_code"
                    name="sms_code"
                    type="text"
                    auto-complete="on"
                  />
                </el-col>
                <el-col style="width: 16%;">
                  <el-button :disabled="logindisabled" type="primary" @click="handleLoginSmsCode" style="width: 200px;">
                    {{ loginbtntxt }}
                  </el-button>
                </el-col>
              </el-form-item>

              <el-button
                :loading="phoneloading"
                type="primary"
                style="width:100%;margin-bottom:30px;"
                @click.native.prevent="handlePhoneLogin">{{ $t('login.logIn') }}
              </el-button>

              <el-button class="resetpwd-button" type="primary" @click="showResetPwdDialog=true">
                {{ $t('login.resetPwd') }}
              </el-button>

              <el-button class="register-button" type="primary" @click="showRegisterDialog=true">
                {{ $t('login.register') }}
              </el-button>
              <el-button class="thirdparty-button" type="primary" @click="showDialog=true">
                {{ $t('login.thirdparty') }}
              </el-button>
            </el-form>
          </div>
        </keep-alive>
      </div>
    </div>


    <el-dialog :title="$t('login.thirdparty')" :visible.sync="showDialog" append-to-body>
      <social-sign/>
      <br>
      <br>
      <strong>{{ $t('login.thirdpartyTips') }}</strong>
    </el-dialog>
    <el-dialog :title="$t('login.register')" :visible.sync="showRegisterDialog" append-to-body>
      <div class="app-container">
        <el-form ref="registerForm" :model="registerForm" :rules="registerRules" label-width="120px" class="login-form">
          <el-form-item prop="cname" label="姓名">
            <el-input
              v-model="registerForm.cname"
              name="cname"
              type="text"
              auto-complete="on"
            />
          </el-form-item>
          <el-form-item prop="email" label="邮箱">
            <el-input
              v-model="registerForm.email"
              name="email"
              type="text"
              auto-complete="on"
            />
          </el-form-item>
          <el-form-item prop="phone" label="手机号">
            <el-input
              v-model="registerForm.phone"
              name="phone"
              type="text"
              auto-complete="on"
            />
          </el-form-item>
          <el-form-item label="验证码" prop="sms_code">
            <el-col :span="16">
              <el-input
                v-model="registerForm.sms_code"
                name="sms_code"
                type="text"
                auto-complete="on"
              />
            </el-col>
            <el-col :span="8">
              <el-button :disabled="disabled" type="primary" @click="handleSmsCode">
                {{ btntxt }}
              </el-button>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-button
              :loading="loading"
              type="primary"
              style="width:100%;margin-bottom:30px;"
              @click.native.prevent="handleRegister">
              注册
            </el-button>
            <span style="color: red">注册成功后帐号以及密码会发送至您的邮箱，请查看邮箱!</span>
          </el-form-item>

        </el-form>
      </div>
    </el-dialog>
    <el-dialog :title="$t('login.resetPwd')" :visible.sync="showResetPwdDialog" append-to-body>
      <div class="app-container">
        <el-form ref="resetpwdForm" :model="resetpwdForm" :rules="resetPwdRules" label-width="120px" class="login-form">
          <el-form-item prop="email" label="邮箱">
            <el-input
              v-model="resetpwdForm.email"
              name="email"
              type="text"
              auto-complete="on"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              :loading="loading"
              type="primary"
              style="width:100%;margin-bottom:30px;"
              @click.native.prevent="handleResetPwd">
              提交
            </el-button>
            <span style="color: red">提交后重置密码链接会发送至您的邮箱，请查看邮箱!</span>
          </el-form-item>

        </el-form>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {isvalidUsername, isvalidPhone, validateEmail} from '@/utils/validate'
  import LangSelect from '@/components/LangSelect'
  import SocialSign from './socialsignin'
  import {User} from '@/api/user'

  export default {
    name: 'Login',
    components: {LangSelect, SocialSign},
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
          callback(new Error('Please enter the correct cname'))
        } else {
          callback()
        }
      }
      const validatePassword = (rule, value, callback) => {
        if (value.length < 6) {
          callback(new Error('The password can not be less than 6 digits'))
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
      const validateSmsCode = (rule, value, callback) => {
        if (value.length == 0) {
          callback(new Error('Please enter the correct code'))
        } else {
          callback()
        }
      }
      return {
        tab: 1,
        loginForm: {
          username: '',
          password: '',
        },

        loginRules: {
          username: [{required: true, trigger: 'blur', validator: validateUsername}],
          password: [{required: true, trigger: 'blur', validator: validatePassword}]
        },
        loginPhoneForm: {
          phone: '',
          sms_code: '',
          action: 'login',
        },
        loginPhoneRules: {
          phone: [{required: true, trigger: 'blur', validator: validatePhone}],
          sms_code: [{required: true, trigger: 'blur', validator: validateSmsCode}]
        },

        passwordType: 'password',
        loading: false,
        phoneloading: false,
        showRegisterDialog: false,
        showResetPwdDialog: false,
        showDialog: false,
        redirect: undefined,
        btntxt: '获取短信验证码',
        loginbtntxt: '获取短信验证码',
        disabled: false,
        logindisabled: false,
        time: 0,
        logintime: 0,
        registerForm: {
          cname: '',
          phone: '',
          email: '',
          sms_code: '',
          action: 'register',
        },
        resetpwdForm: {
          email: '',
        },
        registerRules: {
          cname: [{required: true, trigger: 'blur', validator: validateCname}],
          phone: [{required: true, trigger: 'blur', validator: validatePhone}],
          email: [{required: true, trigger: 'blur', validator: rvalidateEmail}],
          sms_code: [{required: true, trigger: 'blur', validator: validateSmsCode}]
        },
        resetPwdRules: {
          email: [{required: true, trigger: 'blur', validator: rvalidateEmail}],
        }
      }
    },
    watch: {
      $route: {
        handler: function (route) {
          this.redirect = route.query && route.query.redirect
        },
        immediate: true
      }
    },
    methods: {
      toTab(index) {
        if (index == 1 && this.$refs['loginPhoneForm'] !== undefined) {
          this.$refs['loginPhoneForm'].clearValidate()
        }
        else if (this.$refs['loginForm'] !== undefined) {
          this.$refs['loginForm'].clearValidate()
        }
        this.tab = index;
        //重置表单
      },
      showPwd() {
        if (this.passwordType == 'password') {
          this.passwordType = ''
        } else {
          this.passwordType = 'password'
        }
      },
      handleLogin() {
        this.$refs['loginForm'].validate(valid => {
          if (valid) {
            this.loading = true
            this.$store.dispatch('LoginByUsername', this.loginForm).then(() => {
              this.loading = false
              if (this.redirect.indexOf('http') == 0) {
                window.location.href = this.redirect
              } else {
                this.$router.push({path: this.redirect || '/'})
              }

            }).catch(() => {
              this.loading = false
            })
          } else {
            return false
          }
        })
      },
      handleRegister() {
        this.$refs['registerForm'].validate(valid => {
          if (valid) {
            this.loading = true
            this.$store.dispatch('RegisterUser', this.registerForm).then(() => {
              this.loading = false
              this.$message({
                title: '注册',
                message: '注册成功',
                type: 'success',
                duration: 2000
              })
              this.showRegisterDialog = false
            }).catch(() => {
              this.loading = false
            })
          } else {
            return false
          }
        })
      },
      handleResetPwd() {
        this.$refs['resetpwdForm'].validate(valid => {
          if (valid) {
            this.loading = true
            this.$store.dispatch('EmailResetPwd', this.resetpwdForm).then(() => {
              this.loading = false
              this.$message({
                title: '重置',
                message: '重置邮件已经发送，请查看邮箱!',
                type: 'success',
                duration: 2000
              })
              this.showResetPwdDialog = false
            }).catch(() => {
              this.loading = false
            })
          } else {
            return false
          }
        })
      },

      handlePhoneLogin() {
        this.$refs['loginPhoneForm'].validate(valid => {
          if (valid) {
            this.loading = true
            this.$store.dispatch('LoginPhone', this.loginPhoneForm).then(() => {
              this.loading = false
              if (this.redirect.indexOf('http') == 0) {
                window.location.href = this.redirect
              } else {
                this.$router.push({path: this.redirect || '/'})
              }

            }).catch(() => {
              this.loading = false
            })
          } else {
            return false
          }
        })
      },
      handleLoginSmsCode: function () {
        if (this.loginPhoneForm.phone == '' || !isvalidPhone(this.loginPhoneForm.phone)) {
          this.$message({
            title: '登录',
            message: '请输入手机号',
            type: 'error',
            duration: 2000
          })
          return
        }
        User.send_sms_code(this.loginPhoneForm).then(response => {
          this.logintime = 60
          this.logindisabled = true
          this.logintimer()
        }).catch(error => {
          console.log(error)
        })
      },
      handleSmsCode: function () {
        if (this.registerForm.phone == '' || !isvalidPhone(this.registerForm.phone)) {
          this.$message({
            title: '注册',
            message: '请输入手机号',
            type: 'error',
            duration: 2000
          })
          return
        }
        User.send_sms_code(this.registerForm).then(response => {
          this.time = 60
          this.disabled = true
          this.timer()
        }).catch(error => {
          console.log(error)
        })
      },
       timer: function () {
        if (this.time > 0) {
          this.time--
          this.btntxt = this.time + 's,已发短信验证码'
          setTimeout(this.timer, 1000)
        } else {
          this.time = 0
          this.btntxt = '获取短信验证码'
          this.disabled = false
        }
      },
       logintimer: function () {
        if (this.logintime > 0) {
          this.logintime--
          this.loginbtntxt = this.logintime + 's,已发短信验证码'
          setTimeout(this.logintimer, 1000)
        } else {
          this.logintime = 0
          this.loginbtntxt = '获取短信验证码'
          this.logindisabled = false
        }
      },

    }
  }
</script>

<style rel="stylesheet/scss" lang="scss">

  $bg: #283443;
  $light_gray: #eee;
  $cursor: #fff;

  @supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input {
      color: $cursor;
      &::first-line {
        color: $light_gray;
      }
    }
  }

  /* reset element-ui css */
  .login-container {
    .el-input {
      display: inline-block;
      height: 35px;
      width: 85%;
      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 35px;
        caret-color: $cursor;
        &:-webkit-autofill {
          -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: $cursor !important;
        }
      }
    }
    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
  }
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #eee;

  .login-container {
    position: fixed;
    height: 100%;
    width: 100%;
    background-color: $bg;
    .login-form {
      position: absolute;
      left: 0;
      right: 0;
      width: 520px;
      max-width: 100%;
      padding: 35px 35px 15px 35px;
      margin: 120px auto;
    }
    .tips {
      font-size: 14px;
      color: #fff;
      margin-bottom: 10px;
      span {
        &:first-of-type {
          margin-right: 16px;
        }
      }
    }
    .svg-container {
      padding: 1px 5px 6px 15px;
      color: $dark_gray;
      vertical-align: middle;
      width: 30px;
      height: 35px;
      display: inline-block;
    }
    .title-container {
      position: relative;
      .title {
        font-size: 26px;
        color: $light_gray;
        margin: 40px auto 0px auto;
        text-align: center;
        font-weight: bold;
      }
      .set-language {
        color: #fff;
        position: absolute;
        top: 5px;
        right: 0px;
      }
    }
    .show-pwd {
      position: absolute;
      right: 10px;
      top: 7px;
      font-size: 16px;
      color: $dark_gray;
      cursor: pointer;
      user-select: none;
    }
    /*.resetpwd-button {
      //position: absolute;
    }*/
    .register-button {
      position: absolute;
    }
    .thirdparty-button {
      position: absolute;
      right: 35px;
    }
  }

  .test {
    .testNav {
      position: absolute;
      left: 0;
      right: 0;
      width: 450px;
      max-width: 100%;
      padding: 35px 35px 5px 35px;
      margin: 45px auto;
      line-height: 60px;
      display: flex;
      border-bottom: 1px solid #2d3a4b;
      .testTitle {
        flex: 1;
        text-align: center;
      }
      .selected {
        color: #eeefff;
      }
    }
  }
</style>
