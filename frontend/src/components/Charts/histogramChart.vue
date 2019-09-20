<template>
  <div style="margin-top: 5px">
    <ve-histogram :data="chartData"  :width="width" :height="height" :chartSettings="chartSettings"/>
  </div>
</template>

<script>
  import VeHistogram from 'v-charts/lib/histogram.common'

  export default {
    components: {VeHistogram},
    props: {
      width: {
        type: String,
        default: '100%'
      },
      height: {
        type: String,
        default: '200px'
      },
      chartData: {
        type: Object,
        require:true,
      },
      chartSettings: {
        type: Object,
        require:true,
      }
    },
    data() {
      return {
        chartData1: {
          columns: ['日期', '访问用户'],
          rows: [
            {'日期': '2019-01-01', '访问用户': 1393},
            {'日期': '2019-01-02', '访问用户': 3530},
            {'日期': '2019-01-03', '访问用户': 2923},
          ]
        }
      }
    },
    mounted() {
      console.log("----->", this.width, this.height)
    },
  }
</script>
