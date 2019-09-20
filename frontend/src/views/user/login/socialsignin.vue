<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 * 第三方登录
-->
<template>
  <div class="social-signup-container">
    <div class="sign-btn" @click="handleSocialClick('weibo')">
      <span class="wb-svg-container"><svg-icon icon-class="weibo" class="icon"/></span> 微博
    </div>
     <div class="sign-btn" @click="handleSocialClick('github')">
      <span class="gh-svg-container"><svg-icon icon-class="github" class="icon"/></span> GitHub
    </div>
    <div class="sign-btn" @click="handleSocialClick('weixin')">
      <span class="wx-svg-container"><svg-icon icon-class="weixin" class="icon"/></span> 微信
    </div>
    <div class="sign-btn" @click="handleSocialClick('qq')">
      <span class="qq-svg-container"><svg-icon icon-class="qq" class="icon"/></span> QQ
    </div>
  </div>
</template>

<script>
import {openWindow,getSocialLoginUrl} from '@/utils'
export default {
  name: 'SocialSignin',
  methods: {
    handleSocialClick(thirdpart) {
      const url = getSocialLoginUrl(thirdpart)
      document.location.href = url
    }

  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
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

    .gh-svg-container,
    .wx-svg-container,
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

    }
    .qq-svg-container {
      background-color: #6BA2D6;
      margin-left: 30px;
    }
  }
</style>
