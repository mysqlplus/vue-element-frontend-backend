<!--
/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 删除
 */
-->
<template>
  <el-dialog title="Delete" :visible.sync="delVisible" width="300px">
    <div class="del-dialog-cnt">{{ $t('notice.delete') }}</div>
    <span slot="footer" class="dialog-footer">
        <el-button @click="deleteCancel">{{ $t('table.cancel') }}</el-button>
        <el-button type="primary" @click="deleteData()" :loading="delloading">{{$t('table.confirm') }}</el-button>
      </span>
  </el-dialog>
</template>

<script>
  export default {
    name: 'DeleteBase',
    props: {
      delVisible: {
        type: Boolean,
        required: true
      },
    },
    data() {
      return {
        delloading: false,
      }
    },
    methods: {
      deleteData() {
        this.delloading = true
        setTimeout(() => {
          this.delloading = false
        }, 2000)
        this.$emit("deleteData")
      },
      deleteCancel(){
         this.$emit("deleteCancel")
      }
    },
  }
</script>
