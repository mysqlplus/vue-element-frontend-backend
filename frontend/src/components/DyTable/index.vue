<!--
@param:
	tableData: 表格数据列表
	tableKey: 表格对应名称和关键字
	isExpand: 是否显示展开行(true or false)
	isExpandOne: 展开行是否只显示一行(true of false)
	isSelect: 是否显示勾选框(true or false)
	isIndex: 是否显示索引列(true or false)
	fixedHeight: 固定高度

	@sub param
		operate: 是否使用template模板(true or false)
		name: 对应列名
		value: 对应列的关键字
		width: 宽度
		minWidth: 最小宽度
		fixed: 是否固定列(left or right)
		sortable: 是否启用排序(ture or false or 'custom'=>服务器排序)
@method:
	CellClick: 表格点击
	sortChange: 排序
	SelectChange: 勾选变化
	handleExpandRow: 展开行

@example
<sl-table :tableData="tableData" :tableKey="tableKey">
	<template slot="option" slot-scope="scope">
		<el-button size="small" type="text" @click="handleRowEdit(scope.$index,scope.row)">编辑</el-button>
	</template>
</sl-table>

tableKey: [{
	operate:false,
	name: 'ID',
	value: 'Id'
},{
	operate: false,
	name: '名称',
	value: 'name'
},{
	operate: false,
	name: '排序',
	value: 'sort'
},{
	operate: true,
	name: '操作',
	value: 'option'
}]
 -->

<template>
  <div>
    <div class="sl-table">
      <el-table :data="tableData" border ref="raw_table"
                :stripe="true"
                :height="fixedHeight"
                @cell-click="CellClick"
                @sort-change="sortChange"
                @selection-change="handleSelectionChange"
                @expand-change="handleExpandRow"
                @filter-change="handleFilterChange"

      >
        <!-- expand -->
        <el-table-column v-if="isExpand" type="expand">
          <template slot-scope="scope">
            <slot name="expand" :$index="scope.$index" :row="scope.row"></slot>
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item v-for="(item,index) in tableColumns" v-if="item.operate!=3"
                            :key="index"
                            :label="item.name"
              >
                <span>{{ scope.row[item.value]}} </span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>

        <!-- selection -->
        <el-table-column v-if="isSelect" type="selection" min-width="35%" align="center"></el-table-column>
        <!-- index -->
        <el-table-column v-if="isIndex" type="index" min-width="35%" align="center"></el-table-column>
        <!-- table head -->
        <el-table-column v-for="(item,key) in tableColumns"
                         :key="key"
                         align="center"
                         v-if="item.operate==1 && excludeColumns.indexOf(item.value)<0 "
                         :prop="item.value"
                         :label="item.name"
                         :width="item.width"
                         :min-width="item.minWidth"
                         :fixed="item.isfixed"
                         :sortable="item.sortable"
                         :show-overflow-tooltip="true"
                         :tranfer="item.tranfer"
                         :filters="item.filter"
                         :filter-multiple="item.filtermulable==undefined?false:item.filtermulable"
        ></el-table-column>

        <el-table-column :label="item.name" v-else-if="item.operate==2 && excludeColumns.indexOf(item.value)<0">
          <template slot-scope="scope">
            <slot :name="item.value" :$index="scope.$index" :row="scope.row"></slot>
          </template>
        </el-table-column>
        <!-- oparation -->
        <el-table-column v-else-if="item.operate==3 && excludeColumns.indexOf(item.value)<0"
                         :label="item.name"
                         :prop="item.value"
                         align="center"
                         :width="item.width"
                         :min-width="item.minWidth"
                         :fixed="item.isfixed"
                         :sortable="item.sortable" v-if="action">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">{{ $t('table.edit') }}
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row.id)">{{$t('table.delete') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>

  export default {
    name: 'Dytable',
    data() {
      return {
        multipleSelection:[],
      }
    },
    props: {
      tableData: {
        type: Array,
        required: true
      },
      tableColumns: {
        type: Array,
        required: true
      },
      action: {
        type: Boolean,
        required: false
      },
      excludeColumns: {
        type: Array,
        required: false,
        default: [],
      },
      exportUrl: {
        type: String,
        required: false
      },
      isSelect: {
        type: Boolean,
        required: false
      },
      isExpand: {
        type: Boolean,
        required: false
      },
      isExpandOne: {
        type: Boolean,
        required: false
      },
      isIndex: {
        type: Boolean,
        required: false
      },
      fixedHeight: {
        type: [Number, String],
        required: false
      },
    },
    methods: {
      handleUpdate(row) {
        console.log(row)
        this.$emit("handleUpdate", row)
      },
      handleDelete(id) {
        console.log(id)
        this.$emit("handleDelete", id)
      },
      sortChange(argu) {
        this.$emit("sortChange", argu)
      },
      CellClick(row, col, cell) {
        this.$emit("CellClick", {row, col, cell})
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
        this.$emit("handleSelectionChange", val)
      },
      handleExpandRow(row, expandRows) {
        if (this.isExpandOne) {
          this.$refs.raw_table.store.states.expandRows = expandRows.length !== 0 ? [row] : []
        } else {
        }
      },
      handleFilterChange(filters) {
        var num = 0
        var filterValues = []
        for (var p in filters) {
          var arr = p.split("_")
          num = parseInt(arr[arr.length - 1])
          filterValues = filters[p]
        }
        num--
        if (this.isExpand) {
          num--
        }
        if (this.isSelect) {
          num--
        }
      },
    },
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
