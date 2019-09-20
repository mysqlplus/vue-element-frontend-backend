<!--
/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 导入导出 删除 查询
 */
-->
<template>
  <span v-if="isSearch">
    <el-input v-model="search1" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter"/>
    <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">{{
      $t('table.search') }}
    </el-button>
    <el-button v-waves :loading="exportLoading" class="filter-item" type="primary" icon="el-icon-download"
               v-if="isExportSelect"
               @click="handleExport('selected')">{{ $t('table.export') }}
    </el-button>
    <el-button v-waves :loading="exportAllLoading" class="filter-item" type="primary" icon="el-icon-download"
               v-if="isExportAll"
               @click="handleExport('all')">{{ $t('table.exportall') }}
    </el-button>
    <el-button class="filter-item" type="primary" icon="el-icon-upload" @click="handleUpload" v-if="isUpload">{{
      $t('table.upload') }}
    </el-button>

    <el-dialog :title="'导入数据'" :visible.sync="dialogUploadFormVisible">
      <el-upload
        ref="uploadData"
        class="upload-demo"
        drag
        :action="uploadUrl"
        list-type="text"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传xls文件</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closeUpload()">{{ $t('table.cancel') }}</el-button>
      </div>
    </el-dialog>
  </span>
</template>

<script>
  import waves from '@/directive/waves' // Waves directive
  export default {
    name: 'SearchEUpload',
    directives: {waves},
    data() {
      return {
        search1: '',
        exportLoading: false,
        exportAllLoading: false,
        dialogUploadFormVisible: false,
      }
    },
    props: {
      isSearch: {
        type: Boolean,
        required: true
      },
      exportUrl: {
        type: String,
        required: false
      },
      multipleSelection: {
        type: Array,
        required: false
      },
      isExportSelect: {
        type: Boolean,
        required: false
      },
      isExportAll: {
        type: Boolean,
        required: false
      },
      isUpload: {
        type: Boolean,
        required: false
      },
      uploadUrl: {
        type: String,
        required: false
      },
    },
    methods: {
      handleFilter() {
        this.$emit("handleFilter", this.search1, 1)
      },
      handleUpload() {
        this.dialogUploadFormVisible = true
      },
      handleUploadSuccess(res, file) {
        var str = ""
        if (res != null && res != undefined) {
          str = file.name + " <br>插入：" + res.new + " 更新:" + res.update + " 忽略:" + res.skip + " 错误：" + res.error
        }
        this.$message({
          title: '成功',
          dangerouslyUseHTMLString: true,
          message: str,
          type: 'success',
          duration: 2000
        })
      },
      handleUploadError(err, file, fileList) {
        console.log(err,file,fileList)
        console.log(JSON.stringify(err))
        var errmsg=err+""
        console.log(errmsg)
        this.$message({
          title: '成功',
          message: "上传失败:" + err,
          type: 'error',
          duration: 3000
        })
      },
      closeUpload() {
        this.dialogUploadFormVisible = false
        this.$refs.uploadData.clearFiles()
      },
      handleExport(scope) {
        if (scope == "all") {
          this.exportAllLoading = true
        } else {
          this.exportLoading = true
        }
        var downloadUrl = this.exportUrl + "?scope=" + scope
        if (scope === 'selected') {
          if (this.multipleSelection.length == 0) {
            this.$notify({title: '提示信息', message: '未勾选需要导出的数据', type: 'warning', duration: 2000})
            this.exportLoading = false
            return
          } else {
            var ids = []
            for (var i = 0; i < this.multipleSelection.length; i++) {
              ids.push(this.multipleSelection[i]['id'])
            }
            var idsStr = ids.join()
            downloadUrl += '&ids=' + idsStr
          }
        }
        window.location.href = downloadUrl;
        if (scope == "all") {
          this.exportAllLoading = false
        } else {
          this.exportLoading = false
        }
      },
    },
  }
</script>
