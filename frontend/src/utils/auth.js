/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  cookie 设置
 */
import Cookies from 'js-cookie'

var param = {path: '/', domain: document.domain.match(/[^\.]+\.[^\.]+$/)[0]}
export function getToken() {
  var tokenName = Cookies.get('token_name', param)
  if(tokenName){
    return Cookies.get(tokenName,param)
  }else{
    return false
  }
}
