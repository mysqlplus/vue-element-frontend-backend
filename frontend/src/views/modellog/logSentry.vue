<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  日志管理
-->
<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.action_flag" :placeholder="'操作类型'" clearable class="filter-item" style="width: 20%!important;" @change="handleFilter" filterable>
        <el-option v-for="item in ActionOptions" :key="item.key" :label="item.display_name" :value="item.key"/>
      </el-select>
      <el-select v-model="listQuery.content_type" :placeholder="'数据库表名'" clearable class="filter-item" style="width: 20%!important;"  @change="handleFilter" filterable>
        <el-option v-for="item in models" :key="item.id" :label="item.model" :value="item.id"/>
      </el-select>
      <el-input v-model="listQuery.search" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">{{ $t('table.search') }}</el-button>
    </div>

    <el-table
      v-loading="listLoading"
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange">
      <el-table-column :label="$t('table.id')" prop="id" sortable="custom" align="center" width="65">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作时间" width="180">
        <template slot-scope="scope">
          <span class="link-type" @click="handleDetail(scope.row)">{{ scope.row.time_added }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户" width="120">
        <template slot-scope="scope">
          <span>{{ scope.row.user }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作类型" width="100">
        <template slot-scope="scope">
          <span>{{ scope.row.action }}</span>
        </template>
      </el-table-column>
      <el-table-column label="数据库表名" width="100">
        <template slot-scope="scope">
          <span>{{ scope.row.model }}</span>
        </template>
      </el-table-column>
      <el-table-column label="日志记录">
        <template slot-scope="scope">
          <span>{{ scope.row.message }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.pagesize" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="100px" style="width: 80%; margin-left:50px;">
        <el-form-item label="操作时间" prop="time_added">
          <el-input v-model="temp.time_added"/>
        </el-form-item>
        <el-form-item label="用户" prop="user">
          <el-input v-model="temp.user"/>
        </el-form-item>
        <el-form-item label="操作类型" prop="action">
          <el-input v-model="temp.action"/>
        </el-form-item>
        <el-form-item label="数据库表名" prop="model">
          <el-input v-model="temp.model"/>
        </el-form-item>
        <el-form-item label="日志记录" prop="message">
          <el-input type="textarea" rows=5 v-model="temp.message"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('table.cancel') }}</el-button>
        <el-button v-show="dialogStatus!='detail'" type="primary" @click="dialogStatus==='create'?createData():updateData()">{{ $t('table.confirm') }}</el-button>
      </div>
    </el-dialog>

    <!-- 删除提示框 -->
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
import { LogSentry, Model } from '@/api/modellog'
import waves from '@/directive/waves' // Waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination
import {ActionOptions} from '@/utils/dict'

const calendarTypeOptions = [
]
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'modellog_logsentry',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        pagesize: 10,
        name: undefined,
        ordering: '-id',
        search: '',
        action_flag: '',
        content_type: '',
      },
      models: '',
      ActionOptions,
      calendarTypeOptions,
      temp: {
        id: undefined,
        time_added: '',
        user: '',
        action: '',
        message: '',
        model: '',
      },
      dialogFormVisible: false,
      delVisible: false,
      dialogStatus: '',
      textMap: {
        update: this.$t('dialog.update'),
        create: this.$t('dialog.create'),
        delete: this.$t('dialog.delete'),
        detail: this.$t('dialog.detail'),
      },
      rules: {
        name: [{ required: true, message: 'name is required', trigger: 'blur' }],
        cname: [{ required: true, message: 'cname is required', trigger: 'blur' }],
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    this.getModelList()
  },
  methods: {
    getList() {
      this.listLoading = true
      LogSentry.list(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count

        setTimeout(() => {
          this.listLoading = false
        }, 1 * 1000)
      })
    },
    getModelList() {
        Model.list().then(response => {
          this.models = response;
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    resetTemp() {
      this.temp = {
        time_added: '',
        user: '',
        action: '',
        message: '',
        model: '',
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          Role.create(this.temp).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDetail(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.message = JSON.stringify(this.temp.message)
      this.dialogStatus = 'detail'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          Role.patch(this.temp.id, this.temp).then(() => {
            for (const v of this.list) {
              if (v.id === this.temp.id) {
                const index = this.list.indexOf(v)
                this.list.splice(index, 1, this.temp)
                break
              }
            }
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(id) {
      this.dialogStatus = 'delete'
      this.temp.id = id
      this.delVisible = true
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = [this.$t('table.name'), this.$t('table.cname'), this.$t('table.description')]
        const filterVal = ['name', 'cname', 'description']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'role-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'date_joined') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.ordering = 'id'
      } else {
        this.listQuery.ordering = '-id'
      }
      this.handleFilter()
    },
    deleteData() {
      this.delVisible = false
      Role.delete(this.temp.id).then(() => {
        this.getList()
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
      })
    }
  }
}
</script>
