<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  url vue
-->
<template>
    <AvueTable :tableOpiton="tableOpiton"
             :masterApi="masterApi"
             :masterUri="masterUri"
             :listQueryExtra="listQueryExtra"
             :isExportS="false"
             :isExportA="false"
             :isUpload="false"
  />
</template>

<script>
  import {ApiBase} from '@/api/apibase'
  import {tableOpitonSearchM} from '@/utils/avueTableConst'
  import AvueTable from '@/components/AvueTable'

  export default {
    name: 'users_urls',
    components: {AvueTable},
    data() {
      return {
        masterApi: ApiBase,
        masterUri: "/users/urls",
        //开关规则字段
        radioCols: [],
        //自定义规则
        rulesCols: [],
        tableOpiton: tableOpitonSearchM,
        //配合上边一起搜索使用
        listQueryExtra: ['method__in', 'user_type__in']
      }
    },
  }
</script>
