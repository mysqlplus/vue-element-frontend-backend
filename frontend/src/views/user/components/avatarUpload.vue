<template>
  <div class="avatar-main">
    <code style="padding: 3px 20px">修改用户头像
    </code>

    <pan-thumb :image="image" style="position: absolute; bottom: 40%; margin-left: 30%;"/>

    <el-button type="primary" icon="upload" style="position: absolute;bottom: 7%;margin-left: 35%;"
               @click="imagecropperShow=true">{{ $t('common.changeavatar') }}
    </el-button>

    <image-cropper
      v-show="imagecropperShow"
      :width="100"
      :height="100"
      :key="imagecropperKey"
      url="/users/user/upload_avatar/"
      lang-type="en"
      @close="close"
      @crop-upload-success="cropSuccess"/>
  </div>
</template>

<script>
  import ImageCropper from '@/components/ImageCropper'
  import PanThumb from '@/components/PanThumb'
  import {Message} from 'element-ui'
  export default {
    name: 'AvatarUpload',
    components: {ImageCropper, PanThumb},
    data() {
      return {
        imagecropperShow: false,
        imagecropperKey: 0,
        image: this.$store.getters.avatar
      }
    },
    methods: {
      cropSuccess(resData) {
        this.imagecropperShow = false
        this.imagecropperKey = this.imagecropperKey + 1
        this.image = resData.avatar
        this.$store.dispatch('ChangeAvatar', this.image).then(() => {
          Message({message: '更新成功!', type: 'success', duration: 2 * 1000})
        }).catch(() => {
          Message({message: '更新失败!', type: 'error', duration: 2 * 1000})
        })
      },
      close() {
        this.imagecropperShow = false
      }
    }
  }
</script>
