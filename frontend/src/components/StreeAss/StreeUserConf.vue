<template>
  <div class="app-container" style="padding: 10px;">
    <span>{{ $t('stree.charge_person') }}</span>
    <el-table
      v-loading="listLoading"
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;font-size: 11px">
      <el-table-column :label="$t('table.username')">
        <template slot-scope="scope">
          <span>{{ scope.row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('userconf.isvoice')">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.enable_voice"
            class="switchinner"
            active-color="#00A854"
            active-text="ON"
            inactive-color="#F04134"
            inactive-text="OFF"
            @change="changeSwitch('voice',scope.row)"
            v-bind:disabled="scope.row.ismine"
          />
        </template>
      </el-table-column>
      <el-table-column :label="$t('userconf.issms')">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.enable_sms"
            class="switchinner"
            active-color="#00A854"
            active-text="ON"
            inactive-color="#F04134"
            inactive-text="OFF"
            @change="changeSwitch('sms',scope.row)"
            v-bind:disabled="scope.row.ismine"/>
        </template>
      </el-table-column>
      <el-table-column :label="$t('userconf.isemail')">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.enable_mail"
            class="switchinner"
            active-color="#00A854"
            active-text="ON"
            inactive-color="#F04134"
            inactive-text="OFF"
            @change="changeSwitch('email',scope.row)"
            v-bind:disabled="scope.row.ismine"
          />
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.pagesize"
                @pagination="getlist" :page-size="5"/>
  </div>
</template>
<script>
  import {StreeUserConfs} from '@/api/stree'
  import Pagination from '@/components/Pagination'

  export default {
    name: 'StreeUserConf',
    components: {Pagination},
    directives: {waves},
    props: {
      isLeafShow: true,
      treeid: "",
      treename: "",
      treepid: "",
      nodelevel: '',
      showCicd: false,
    },
    data() {
      return {
        textMap: {
          update: this.$t('dialog.update'),
          create: this.$t('dialog.create'),
          delete: this.$t('dialog.delete'),
          detail: this.$t('dialog.detail'),
        },
        userConfTemp: {
          enable_mail: '',
          enable_sms: '',
          enable_voice: '',
          tree: '',
          user: '',
        },
        dialogStatus: 'create',
        dialogFormVisible: false,
        list: [],
        listLoading: '',
        total: 0,
      }
    },
    created() {
      this.init()
    },
    methods: {
      getlist() {
        this.listLoading = true
        var params = {}
        params.tree = this.treeid
        StreeUserConfs.find_by_tree(params).then(response => {
          var ucList = []
          for (var i = 0; i < response.length; i++) {
            var userconf = response[i]
            if (userconf.username == this.$store.getters.username) {
              userconf.ismine = false
            } else {
              userconf.ismine = true
            }
            ucList.push(userconf)
          }
          this.list = ucList
          this.listLoading = false
        })
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 2000)
      },
      init() {
        this.getlist()
      },
      changeSwitch(type, row) {
        if (row.id == -1) {
          StreeUserConfs.create(row).then(response => {
            this.$notify({
              title: 'Success',
              message: this.$t('notice.updatesuccess'),
              type: 'success',
              duration: 2000
            })
            this.init()
          })
        } else {
          StreeUserConfs.update(row.id, row).then(response => {
            this.$notify({
              title: 'Success',
              message: this.$t('notice.updatesuccess'),
              type: 'success',
              duration: 2000
            })
            this.init()
          })
        }
      },
    }
  }
</script>
