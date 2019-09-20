<template>
  <div class="app-container" style="padding: 10px;">
    <span>{{$t('stree.demandlist') }}</span>
    <span><el-button class="filter-item" type="primary"
                     @click="handleCreate">{{ $t('table.add') }}</el-button></span>
    <el-table
      v-loading="listLoading"
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;margin-top: 5px;font-size: 11px">
      <el-table-column :label="$t('stree.demand_title')">
        <template slot-scope="scope">
          <span>{{ scope.row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('stree.demand_content')">
        <template slot-scope="scope">
          {{scope.row.content|truncateFilter}}
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.developers')">
        <template slot-scope="scope">
          {{scope.row.developers_detail}}
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.testers')">
        <template slot-scope="scope">
          {{scope.row.testers_detail}}
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.actions')" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" @click="handleDel(scope.row)">{{
            $t('table.delete') }}
          </el-button>
          <el-button size="mini" type="primary" @click="handleUpdate(scope.row)">{{
            $t('table.edit') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="800">
      <el-form ref="dataForm" :model="temp" :rules="rules" label-position="left" label-width="100px"
               style="width: 80%; margin-left:50px;">
        <el-form-item :label="$t('stree.demand_title')" prop="title">
          <el-input v-model="temp.title" placeholder="需求功能标题，请尽量简洁!"/>
        </el-form-item>
        <el-form-item :label="$t('stree.demand_content')" prop="content">
          <el-input :autosize="{ minRows: 5, maxRows: 20}" v-model="temp.content" type="textarea"
                    placeholder="需求内容，请尽量详细填写!"/>
        </el-form-item>
        <el-form-item :label="$t('table.developers')" prop="developers">
          <el-select v-model="temp.developers" filterable multiple placeholder="需求功能开发人员!">
            <el-option v-for="item in users" :key="item.id" :value="item.id" :label="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('table.testers')" prop="testers">
          <el-select v-model="temp.testers" filterable multiple placeholder="需求功能测试人员!">
            <el-option v-for="item in users" :key="item.id" :value="item.id" :label="item.username"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('table.cancel') }}</el-button>
        <el-button v-show="dialogStatus!='detail'" type="primary"
                   @click="dialogStatus==='create'?createData():updateData()" size="mini" v-no-more-click>{{
          $t('table.confirm') }}
        </el-button>
      </div>
    </el-dialog>
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.pagesize"
                @pagination="getList" :page-size="5"/>
    <!-- 删除提示框 -->
    <DeleteBase :delVisible="delVisible" @deleteData="deleteData" @deleteCancel="deleteCancel"/>
  </div>
</template>
<script>
  import waves from '@/directive/waves' // Waves directive
  import {StreeDemands as masterApi} from '@/api/stree'
  import DeleteBase from '@/components/DeleteBase'
  import {conver2KV, trancateStr, getKeyValueAttArr} from '@/utils'
  import Pagination from '@/components/Pagination'

  export default {
    name: 'StreeDemand',
    directives: {waves},
    components: {DeleteBase, Pagination},
    props: {
      treeid: "",
    },
    watch: {
      treeid: {
        handler() {
          this.init()
        },
        immediate: true
      }
    },
    filters: {
      truncateFilter(str) {
        return trancateStr(str, 200)
      },
    },
    data() {
      return {
        temp: {
          title: undefined,
          content: undefined,
          developers: [],
          testers: [],
          tree: this.treeid,
          id:undefined,
        },
        list: [],
        userlist: [],
        dialogFormVisible: false,
        tableKey: 0,
        listLoading: false,
        total: 0,
        delVisible: false,
        currId: undefined,
        listQuery: {
          page: 1,
          pagesize: 10,
          ordering: '-id',
          search: '',
        },
        rules: {
          title: [{required: true, message: 'title is required', trigger: 'blur'}],
          content: [{required: true, message: 'content is required', trigger: 'blur'}],
          developers: [{required: true, message: 'developers is required', trigger: 'blur'}],
        },
        users: [],
        textMap: {
          update: 'Edit',
          create: 'Create',
          delete: 'Delete'
        },
        curid: undefined,
        dialogStatus: 'create',
      }
    },
    created() {
      this.init()
    },
    methods: {
      init() {
        this.getList()
      },
      getList() {
        masterApi.list({"stree_id": this.treeid}).then(response => {
          var list = []
          for (var i = 0; i < response.results.length; i++) {
            var obj = response.results[i]
            if (obj.hasOwnProperty("testers") && obj["testers"].length > 0) {
              var t_str = "["
              for (var j = 0; j < response.results[i]["testers"].length; j++) {
                if (j == 0) {
                  t_str = t_str + response.results[i]["testers"][j]["username"]
                } else {
                  t_str = t_str + "," + response.results[i]["testers"][j]["username"]
                }
              }
              obj["testers_detail"] = t_str + "]"
            }
            if (obj.hasOwnProperty("developers") && obj["developers"].length > 0) {
              var t_str = "["
              for (var j = 0; j < response.results[i]["developers"].length; j++) {
                if (j == 0) {
                  t_str = t_str + response.results[i]["developers"][j]["username"]
                } else {
                  t_str = t_str + "," + response.results[i]["developers"][j]["username"]
                }
              }
              obj["developers_detail"] = t_str + "]"
            }
            list.push(obj)
          }
          this.list = list
          this.total = response.count
          this.listLoading = false
        })
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 4000)
      },
      resetTemp() {
        this.temp = {
          title: undefined,
          content: undefined,
          developers: [],
          testers: [],
          tree: this.treeid,
          id:undefined,
        }
        this.users = []
      },
      handleCreate() {
        this.resetTemp()
        masterApi.get_table_info().then(response => {
          this.users = response.users
        })
        this.dialogFormVisible = true
        this.dialogStatus = 'create'
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },

      handleUpdate(row) {
        this.currId = row.id
        this.resetTemp()
        masterApi.get_table_info().then(response => {
          this.users = response.users
          // this.temp = Object.assign({}, row) // copy obj

          this.temp["developers"] = getKeyValueAttArr(row, "developers", "id")
          this.temp["testers"] = getKeyValueAttArr(row, "testers", "id")
          this.temp["title"] = row["title"]
          this.temp["content"] = row["content"]

          this.dialogStatus = 'update'
          this.dialogFormVisible = true
          this.$nextTick(() => {
            this.$refs['dataForm'].clearValidate()
          })
        })
      },

      handleDel(row) {
        this.currId = row.id
        this.delVisible = true
      },
      deleteData() {
        masterApi.delete(this.currId).then(() => {
          this.$notify({
            title: 'Success',
            message: this.$t('notice.delsuccess'),
            type: 'success',
            duration: 2000
          })
          this.delVisible = false
          this.init()
        })
      },
      createData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            masterApi.create(this.temp).then(() => {
              this.dialogFormVisible = false
              this.getList()
              this.$notify({
                title: 'Success',
                message: this.$t('notice.createsuccess'),
                type: 'success',
                duration: 2000
              })
            })
            setTimeout(() => {
              this.listLoading = false
            }, 1 * 6000)
          }
        })
      },
      updateData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            const tempData = Object.assign({}, this.temp)
            tempData["id"]=this.currId
            masterApi.update(this.currId, tempData).then(() => {
              this.dialogFormVisible = false
              this.getList()
              this.$notify({
                title: 'Success',
                message: this.$t('notice.updatesuccess'),
                type: 'success',
                duration: 2000
              })
            })
          }
        })
      },
      deleteCancel() {
        this.delVisible = false
      },


    }
  }
</script>
