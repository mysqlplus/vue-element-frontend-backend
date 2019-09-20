<!--
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  idc管理页面
-->
<template>
    <AvueTable :tableOpiton="tableOpiton" :masterApi="masterApi" :masterUri="masterUri" :listQueryExtra="listQueryExtra" />
</template>

<script>
  import {ApiBase} from '@/api/apibase'
  import {tableOpitonM} from '@/utils/avueTableConst'
  import AvueTable from '@/components/AvueTable'

  export default {
    name: 'cmdb_idc',
    components: {AvueTable},
    data() {
      return {
        masterApi: ApiBase,
        masterUri:"/cmdb/idcs",
        //开关规则字段
        radioCols: [],
        //自定义规则
        rulesCols: [],
        tableOpiton:tableOpitonM,
        //配合上边一起搜索使用
         listQueryExtra: []
      }
    },
  }
</script>
