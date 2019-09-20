/**
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
* create:2018-07
 *  同步统一request封装
 */
import $ from 'jquery'

const requestSync = {
  deal(url, data, method,timeout=2000) {
    var ret = null
    console.log(timeout)
    try {
      $.ajax({
        url: url,
        type: method,
        async: false,
        data: data,
        timeout: timeout,
        beforeSend: function (xhr) {
        },
        success: function (data, textStatus, jqXHR) {
          ret = data
        },
        error: function (xhr, textStatus) {
          ret = null
        },
        complete: function () {
        }
      })
    } catch (err) {
      console.log(err)
    }
    return ret
  },
}
export {requestSync}
