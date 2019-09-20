<!---
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 *desc 跳转，或者标签切换使用
-->
<script>
export default {
  beforeCreate() {
    const { params, query } = this.$route
    const { path } = params
    this.$router.replace({ path: '/' + path, query })
  },
  render: function(h) {
    return h() // avoid warning message
  }
}
</script>
