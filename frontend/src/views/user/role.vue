<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  角色 vue
-->
<template>
  <div class="app-container">
    <avue-crud :data="tableData" :option="tableOpiton" size="mini" @sort-change="sortChange" :page="page" ref="abc"
               @size-change="sizeChange"
               @current-change="currentChange"
               @selection-change="selectionChange"
               @row-save="insert"
               @row-update="update"
               @row-del="del"
               @refresh-change="refresh"
               @search-change="searchChange"
               @search-reset="searchReset"
    >
      <template slot="menuLeft">
        <SearchEUpload :isSearch="isSearch"
                       :isExportSelect="isExportS"
                       :isExportAll="isExportA"
                       :exportUrl="exportDataUrl"
                       :isUpload="isUpload"
                       :uploadUrl="importDataUrl"
                       :multipleSelection="multipleSelection"
                       @handleFilter="handleFilter"
        />
      </template>
      <template slot-scope="scope" slot="menuBtn">
        <el-dropdown-item divided @click.native="handleGrant(scope.row.id,1)">添加用户
        </el-dropdown-item>
        <el-dropdown-item divided @click.native="handleGrant(scope.row.id,0)">删除用户
        </el-dropdown-item>
      </template>
      <template slot="menuRight">
      </template>
    </avue-crud>
    <!-- 删除提示框 -->
    <DeleteBase :delVisible="delVisible" @deleteData="delData" @deleteCancel="deleteCancel"/>
    <el-dialog :title="granttitle" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="100px"
               style="width: 80%; margin-left:50px;">
        <el-form-item label="用户" prop="users">
          <el-select v-model="temp.users" filterable multiple  @change="">
            <el-option v-for="item in userlist" :key="item.id" :value="item.id"
                       :label="item.username+':'+item.cname"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false" size="mini">{{ $t('table.cancel') }}</el-button>
        <el-button type="primary" @click="handleGrantR()" size="mini" v-no-more-click>{{
          $t('table.confirm') }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {ApiBase} from '@/api/apibase'
  import {Users, Role} from '@/api/user'
  import {optionUtil} from '@/utils'
  import {tableOpitonSearchM} from '@/utils/avueTableConst'
  import {
    getListB,
    getTableInfoB,
    insertB,
    updateB,
    deleteB,
    handleFilterB,
    searchChangeB,
    refreshB,
    sizeChangeB,
    currentChangeB,
    sortChangeB,
    searchResetB
  } from '@/utils/baseOpt'
  import SearchEUpload from '@/components/SearchEUpload'
  import DeleteBase from '@/components/DeleteBase'

  export default {
    name: 'users_roles',
    components: {SearchEUpload, DeleteBase},
    filters: {
      optionFilter(key, options) {
        return optionUtil(key, options)
      },
    },
    data() {
      return {
        masterApi: ApiBase,
        masterUri: "/users/roles",
        tableOpiton: {
          addBtn: true,
          searchBtn: true,
          selection: false,
          border: true,
          page: true,
          align: 'center',
          menuAlign: 'center',
          menuWidth: 100,
          searchMenuSpan: 6,
          viewBtn: true,
          menuType: 'menu',
          column: []
        },
        isSearch: true,
        isExportS: false,
        isExportA: false,
        isUpload: false,
        //分页
        page: {
          currentPage: 1,
          total: 0,
          pageSize: 10
        },
        //table 数据数组
        tableData: [],
        //table 总选项
        radioCols: [],
        //自定义规则
        rulesCols: [],

        multipleSelection: [],

        //其他参数
        importDataUrl: "",
        exportDataUrl: "",
        //删除
        delVisible: false,
        currId: undefined,
        //创建/更新 时候 剔除那些参数不往后端发送
        cRemoveList: [],
        uRemoveList: [],
        noSearchList: [],
        listQuery: {
          ordering: '+id',
          search: '',
        },
        btnloading: false,
        userlist: [],
        textMap: {
          update: this.$t('dialog.update'),
          create: this.$t('dialog.create'),
          delete: this.$t('dialog.delete'),
          detail: this.$t('dialog.detail'),
        },
        temp: {
          users: undefined
        },
        rules: {
          users: [{required: true, message: 'users is required', trigger: 'blur'}],
        },
        dialogFormVisible: false,
        currolelist: [],
        curroleid: undefined,
        granttitle: '添加用户',
        action: 1,
      }

    },
    created() {
      this.init()
    },
    methods: {
      //初始化
      init() {
        this.importDataUrl = process.env.API_PREFIX + this.masterUri + "/import_data/"
        this.exportDataUrl = process.env.API_PREFIX + this.masterUri + "/export_data/"
        this.getList()
        this.getTableInfo()
      },
      // base crud-----------------------------------------------
      getList() {
        let that = this
        var params = Object.assign({}, that.listQuery) // copy obj
        params.page = that.page.currentPage
        params.pagesize = that.page.pageSize
        that.masterApi.list(that.masterUri, params).then(response => {
          this.currolelist = []
          for (var i = 0; i < response.results.length; i++) {
            this.currolelist.push({"id": response.results[i].id, "users": response.results[i]["users"]})
          }
          var list = []
          for (var i = 0; i < response.results.length; i++) {
            var obj = response.results[i]
            var userstr = ""
            for (var j = 0; j < obj["users"].length; j++) {
              if (j == 0) {
                userstr = obj["users"][j]["username"]
              } else {
                userstr = userstr + "," + obj["users"][j]["username"]
              }
            }
            obj["users"] = userstr
            list.push(obj)
          }

          that.tableData = list
          that.page.total = response.count
        })
      },
      getTableInfo() {
        getTableInfoB(this)
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      handleFilter(search, num) {
        handleFilterB(this, search, num)
      },
      insert(form, done, loading) {
        insertB(this, form, done, loading)
      },
      del(form, index) {
        this.currId = form.id
        this.delVisible = true
      },
      delData() {
        if (this.reDel) {
          this.$emit("delData", this.currId, this)
        } else {
          deleteB(this)
        }
      },
      deleteCancel() {
        this.delVisible = false
      },
      update(form, index, done, loading) {
        updateB(this, form, index, done, loading)
      },
      // other opt----------------------------------------------------
      refresh(val) {
        refreshB(this)
      },
      sizeChange(val) {
        sizeChangeB(this, val)
      },
      currentChange(val) {
        currentChangeB(this, val)
      },
      sortChange(val) {
        sortChangeB(this, val)
      },
      selectionChange(list) {
        this.multipleSelection = list
      },
      searchChange(params) {
        searchChangeB(this, params)
      },
      searchReset() {
        searchResetB(this)
      },
      handleGrant(id, flag) {
        this.temp.users=[]
        this.curroleid = id
        this.userlist = []
        this.temp.user_id = undefined
        var excludelist = []
        for (var i = 0; i < this.currolelist.length; i++) {
          if (this.currolelist[i].id == id) {
            excludelist = this.currolelist[i]["users"]
            break
          }
        }
        if (flag == 1) {
          this.action = 1
          this.granttitle = "添加用户"
          Users.list({"page": 1, "pagesize": 5000, "is_active": true}).then(response => {
            var l = []
            for (var i = 0; i < response.results.length; i++) {
              var flag = 0
              for (var j = 0; j < excludelist.length; j++) {
                if (excludelist[j].id == response.results[i].id) {
                  flag = 1
                  break
                }
              }
              if (flag == 0) {
                l.push(response.results[i])
              }
            }
            this.userlist = l
            this.dialogFormVisible = true
          })
        } else {
          this.action = 0
          this.userlist = excludelist
          this.granttitle = "删除用户"
          this.dialogFormVisible = true
        }
      },
      handleGrantR() {
        if (this.action == 1) {
          Role.add_user(this.curroleid, {"users": this.temp.users}).then(response => {
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
            this.getList()
            this.dialogFormVisible = false
            this.temp.users=[]
          })
        } else {
          Role.remove_user(this.curroleid, {"users": this.temp.users}).then(response => {
            this.$notify({
              title: '成功',
              message: '删除成功',
              type: 'success',
              duration: 2000
            })
            this.getList()
            this.dialogFormVisible = false
            this.temp.users=[]
          })
        }

      }
    },
  }
</script>
