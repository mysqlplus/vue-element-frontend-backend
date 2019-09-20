<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
-->
<template>
  <div class="login-container">

    <el-form
      ref="resetpwdForm"
      :model="resetpwdForm"
      :rules="resetpwdRules"
      class="login-form"
      auto-complete="on"
      label-position="left">

      <div class="title-container">
        <h3 class="title">{{ $t('resetpwd.title') }}</h3>
        <lang-select class="set-language"/>
      </div>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password"/>
        </span>
        <el-input
          :type="passwordType"
          v-model="resetpwdForm.password"
          :placeholder="$t('resetpwd.password')"
          name="password"
          auto-complete="on" @keyup.enter.native="handleResetPwd"/>
        <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye"/>
        </span>
      </el-form-item>
      <el-form-item prop="confirm_password">
        <span class="svg-container">
          <svg-icon icon-class="password"/>
        </span>
        <el-input
          :type="passwordType"
          v-model="resetpwdForm.confirm_password"
          :placeholder="$t('resetpwd.confirmPassword')"
          name="confirm_password"
          auto-complete="on"
          @keyup.enter.native="handleResetPwd"/>
        <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye"/>
        </span>
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        style="width:100%;margin-bottom:30px;"
        @click.native.prevent="handleResetPwd">{{ $t('resetpwd.resetpwd') }}
      </el-button>
    </el-form>
  </div>
</template>

<script>
  import {isvalidUsername, isvalidPhone, isvalidResetPassword} from '@/utils/validate'
  import LangSelect from '@/components/LangSelect'
  import SocialSign from './login/socialsignin'
  import {User} from '@/api/user'

  export default {
    name: 'resetpwd',
    components: {LangSelect, SocialSign},
    data() {
      const validatePassword = (rule, value, callback) => {
        if (!isvalidResetPassword(value)) {
          callback(new Error('密码必须8到16位，包含字母大写 小写，数字等字符'))
        } else {
          callback()
        }
      }
      const validateConfirmPwd = (rule, value, callback) => {
        if (value != this.resetpwdForm.password) {
          callback(new Error('两次密码不一致！'))
        } else {
          callback()
        }
      }
      return {
        resetpwdForm: {
          password: '',
          confirm_password: ''
        },
        resetpwdRules: {
          password: [{required: true, trigger: 'blur', validator: validatePassword}],
          confirm_password: [{required: true, trigger: 'blur', validator: validateConfirmPwd}],
        },
        passwordType: 'password',
        loading: false,
        showDialog: false,
        redirect: '/login?redirect=/dashboard',
      }
    },
    methods: {
      showPwd() {
        if (this.passwordType == 'password') {
          this.passwordType = ''
        } else {
          this.passwordType = 'password'
        }
      },
      handleResetPwd() {
        var token = this.$route.query.token
        this.$refs['resetpwdForm'].validate(valid => {
          if (valid) {
            if (token == null || token == undefined || token == '') {
              this.$message({
                message: 'token不能为空',
                type: 'error',
                duration: 2000
              })
              return false;
            }
            this.loading = true
            User.reset_password(token, this.resetpwdForm).then(response => {
              this.loading = false
              this.$message({
                message: '重置成功',
                type: 'success',
                duration: 2000
              })
              this.$router.push({path: this.redirect})
            }).catch(error => {
              this.loading = false
            })
          } else {
            return false
          }
        })
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
      height: 47px;
      width: 85%;
      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
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
      padding: 6px 5px 6px 15px;
      color: $dark_gray;
      vertical-align: middle;
      width: 30px;
      display: inline-block;
    }
    .title-container {
      position: relative;
      .title {
        font-size: 26px;
        color: $light_gray;
        margin: 0px auto 40px auto;
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
    .thirdparty-button {
      position: absolute;
      right: 35px;
      bottom: 28px;
    }
    .register-button {
      position: absolute;
    }
  }
</style>
