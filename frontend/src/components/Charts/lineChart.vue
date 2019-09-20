<template>
  <div>
    <ve-line :data="chartData" :settings="chartSettings"></ve-line>
  </div>
</template>

<script>
  import VeLine from 'v-charts/lib/line.common'

  export default {
    components: {VeLine},
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
  }
</script>
