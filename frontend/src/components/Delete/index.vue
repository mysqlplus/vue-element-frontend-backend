
<template>
  <div>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="delVisible" width="300px">
      <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="delVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteData()">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>

  export default {
    name: 'DeleteT',
    data() {
      return {}
    },
    props: {
      delVisible: {
        type: Boolean,
        required: true
      },
      id: {
        type: Number,
        required: true
      },
      masterApi: {
        type: Object,
        required: true
      },
    },
    methods: {
      deleteData() {
        this.delVisible = false
        masterApi.delete(id).then(() => {
          this.getList()
          this.$notify({
            title: '成功',
            message: '删除成功',
            type: 'success',
            duration: 2000
          })
        })
      },
    }
  }
</script>

<style>
  .sl-table .cell > span {
    word-break: normal;
  }
</style>
<style>
  .demo-table-expand {
    font-size: 0;
  }

  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
