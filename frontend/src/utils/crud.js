/**
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
* create:2018-07
 * crud 真是操作
 */
const indexCrud = require('./index')

export function createData(that, masterApi, form, done, loading) {
  var params = Object.assign({}, form)
  params = indexCrud.removeFromList(params, that.cRemoveList, true)
  masterApi.create(that.masterUri, params).then(() => {
    that.dialogFormVisible = false
    that.getList()
    that.$notify({
      title: 'Success',
      message: that.$t('notice.createsuccess'),
      type: 'success',
      duration: 2000
    })
    done();
  })
  setTimeout(() => {
    loading();
  }, 1000)
}

export function deleteData(that, masterApi) {
  masterApi.delete(that.masterUri, that.currId).then(() => {
    that.delVisible = false
    that.getList()
    that.$notify({
      title: 'Success',
      message: that.$t('notice.delsuccess'),
      type: 'success',
      duration: 2000
    })
  })
}

export function updateData(that, masterApi, form, done, loading) {
  var params = Object.assign({}, form)
  // params = indexCrud.removeFromList(params, that.uRemoveList, true)
  masterApi.update(that.masterUri, params.id, params).then(() => {
    that.$notify({
      title: 'Success',
      message: that.$t('notice.updatesuccess'),
      type: 'success',
      duration: 2000
    })
    that.getList()
    done();
  })
  setTimeout(() => {
    loading();
  }, 1000)
}
