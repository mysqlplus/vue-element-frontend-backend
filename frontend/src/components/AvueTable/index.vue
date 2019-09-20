<!--
/**
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 */
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
      <template slot="menuRight">
      </template>
    </avue-crud>
    <!-- 删除提示框 -->
    <DeleteBase :delVisible="delVisible" @deleteData="delData" @deleteCancel="deleteCancel"/>
  </div>
</template>

<script>
  import {ApiBase} from '@/api/apibase'
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
    name: 'AvueTable',
    components: {SearchEUpload, DeleteBase},
    filters: {
      optionFilter(key, options) {
        return optionUtil(key, options)
      },
    },
    props: {
      masterApi: {
        type: Object,
        required: true
      },
      masterUri: {
        type: String,
        required: true
      },
      tableOpiton: {
        type: Object,
        required: true
      },
      noSearchList: {
        type: Array,
        required: false,
      },
      searchMList: {
        type: Array,
        required: false,
      },
      listQueryExtra: {
        type: Array,
        required: false
      },
      isSearch: {
        type: Boolean,
        required: false,
        default: true,
      },
      isExportS: {
        type: Boolean,
        required: false,
        default: true,
      },
      isExportA: {
        type: Boolean,
        required: false,
        default: true,
      },
      isUpload: {
        type: Boolean,
        required: false,
        default: true,
      },
      //重写方法
      reDel: {
        type: Boolean,
        required: false,
        default: false,
      },
    },
    data() {
      return {
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
        listQuery: {
          ordering: '+id',
          search: '',
        },
      }
    },
    created() {
      if (this.listQueryExtra&&this.listQueryExtra.length>0) {
        for (var i = 0; i < this.listQueryExtra.length; i++) {
          this.listQuery[this.listQueryExtra[i]] = ''
        }
      }
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
        getListB(this)
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
          this.$emit("delData", this.currId,this)
        } else {
          deleteB(this)
        }
      },
      deleteCancel(){
        this.delVisible=false
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
      searchReset(){
        searchResetB(this)
      },
    },
    mounted() {
      if (this.$parent.hasOwnProperty("searchMList")) {
        for (var i = 0; i < this.searchMList.length; i++) {
          this.$refs.abc.searchForm[this.searchMList[i]] = []
        }
      }
    }
  }
</script>
