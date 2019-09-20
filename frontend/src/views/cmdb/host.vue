<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  主机页面
-->
<template>
    <AvueTable :tableOpiton="tableOpiton" :masterApi="masterApi" :masterUri="masterUri" :listQueryExtra="listQueryExtra" />
</template>

<script>
  import {ApiBase} from '@/api/apibase'
  import {tableOpitonSearchMenuM} from '@/utils/avueTableConst'
  import AvueTable from '@/components/AvueTable'

  export default {
    name: 'cmdb_hosts',
    components: {AvueTable},
    data() {
      return {
        masterApi: ApiBase,
        masterUri:"/cmdb/hosts",
        //开关规则字段
        radioCols: [],
        //自定义规则
        rulesCols: [],
        tableOpiton:tableOpitonSearchMenuM,
        //配合上边一起搜索使用
         listQueryExtra: ["host_type","salt_status","run_status","use_status","idc"]
      }
    },
  }
</script>
