<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  用户vue
-->
<template>
  <AvueTable :tableOpiton="tableOpiton"
             :masterApi="masterApi"
             :masterUri="masterUri"
             :listQueryExtra="listQueryExtra"
             :searchMList="searchMList"
             :noSearchList="noSearchList"
             :isExportS="false"
             :isExportA="false"
             :isUpload="false"
             :reDel="true"
             @delData="delData"
  />
</template>

<script>
  import {ApiBase} from '@/api/apibase'
  import {Users} from '@/api/user'
  import {tableOpitonSearchM} from '@/utils/avueTableConst'
  import AvueTable from '@/components/AvueTable'

  export default {
    name: 'users_users',
    components: {AvueTable},
    data() {
      return {
        masterApi: ApiBase,
        masterUri: "/users/users",
        //开关规则字段
        radioCols: [],
        //自定义规则
        rulesCols: [],
        tableOpiton: tableOpitonSearchM,
        //配合上边一起搜索使用
        listQueryExtra: ['is_active', 'is_superuser'],
        searchMList: [],
        noSearchList: ["department", "superior", 'is_staff', "roles", "gender"]
      }
    },
    methods: {
      delData(id, that) {
        Users.leaved(id).then(response => {
          that.delVisible = false
          that.getList()
          that.$notify({
            title: 'Success',
            message: this.$t('notice.delsuccess'),
            type: 'success',
            duration: 2000
          })
        })
      },
    }
  }
</script>
