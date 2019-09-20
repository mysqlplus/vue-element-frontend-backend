<template>
  <div class="app-container" style="padding: 10px;">
    <span>{{$t('stree.falconlist') }}</span>
    <span><el-button class="filter-item" type="primary"
                     @click="handleAddFalcon">{{ $t('table.add') }}</el-button></span>
    <el-table
      v-loading="falconListLoading"
      :key="falconTableKey"
      :data="falconlist"
      border
      fit
      highlight-current-row
      style="width: 100%;margin-top: 5px;font-size: 11px">
      <el-table-column :label="$t('stree.falcon_model_name')">
        <template slot-scope="scope">
          <span>{{ scope.row.tpl_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('stree.falcon_band_user')">
        <template slot-scope="scope">
          {{scope.row.creator}}
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.actions')" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" @click="handleDel(scope.row)" v-if="scope.row.can_del">{{ $t('table.delete') }}</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="绑定" :visible.sync="dialogFormVisible" width="800">
      <el-form ref="dataForm" :model="falconTemp" label-position="left" label-width="100px"
               style="width: 80%; margin-left:50px;">
        <el-form-item :label="$t('stree.falcon_model_name')" prop="template">
          <el-select v-model="falconTemp.tpl_id" filterable>
            <el-option v-for="item in fctemplatelist" :key="item.value" :value="item.value"
                       :label="item.label"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('table.cancel') }}</el-button>
        <el-button type="primary" @click="createData()">
          {{ $t('table.confirm') }}
        </el-button>
      </div>
    </el-dialog>
    <!-- 删除提示框 -->
    <DeleteBase :delVisible="delVisible" @deleteData="deleteData" @deleteCancel="deleteCancel"/>
  </div>
</template>
<script>
  import waves from '@/directive/waves' // Waves directive
  import {MFalconStreeTpls as masterApi} from '@/api/mfalcon'
  import DeleteBase from '@/components/DeleteBase'
  import {conver2KV} from '@/utils'

  export default {
    name: 'StreeMfalcon',
    directives: {waves},
    components: {DeleteBase},
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
    data() {
      return {
        falconTemp: {
          tpl_id: undefined,
          stree:undefined,
          creator:undefined
        },
        falconlist: [],
        fctemplatelist: [],
        dialogFormVisible: false,
        falconTableKey: 0,
        falconListLoading: false,
        falcontotal: 0,
        delVisible:false,
        currId:undefined,
      }
    },
    created() {
      this.init()
    },
    methods: {
      init() {
        masterApi.templates({"stree_id": this.treeid}).then(response => {
          this.falconlist = response
          this.falconListLoading = false
        })
        setTimeout(() => {
          this.falconListLoading = false
        }, 1 * 2000)
      },
      resetTmp(){
        this.falconTemp={
           tpl_id: undefined,
          stree:this.treeid,
          creator:this.$store.getters.user_id
        }
      },
      handleAddFalcon() {
        this.resetTmp()
        this.fctemplatelist=[]
        masterApi.get_table_info().then(response => {
          this.fctemplatelist = conver2KV(['value', 'label'], response["templates"])
          this.dialogFormVisible = true
        })
      },
      handleDel(row) {
        this.currId=row.id
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
        masterApi.create(this.falconTemp).then(() => {
          this.$notify({
            title: 'Success',
            message: this.$t('notice.updatesuccess'),
            type: 'success',
            duration: 2000
          })
          this.dialogFormVisible = false
          this.init()
        })
      },
      deleteCancel(){
        this.delVisible=false
      },
    }
  }
</script>
