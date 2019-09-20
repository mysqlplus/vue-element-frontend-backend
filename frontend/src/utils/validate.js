/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 *  校验js
 */

export function isvalidUsername(str) {
  const reg = /^[A-Za-z0-9]+$/
  return reg.test(str)
}

export function isvalidPassword(str) {
  const reg = /^[A-Za-z0-9]+$/
  return reg.test(str)
}


export function isvalidResetPassword(str) {
  const regl = /[a-z].*/
  const regu = /[A-Z].*/
  const regn = /[0-9].*/
  if (str.length < 8 || str.length > 16) {
    return false
  }
  if (regl.test(str) && regu.test(str) && regn.test(str)) {
    return true
  } else {
    return false
  }
}


/* 合法uri*/
export function validateURL(textval) {
  const urlregex = /^(https?|ftp|http):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
  return urlregex.test(textval)
}

/* 小写字母*/
export function validateLowerCase(str) {
  const reg = /^[a-z]+$/
  return reg.test(str)
}

/* 大写字母*/
export function validateUpperCase(str) {
  const reg = /^[A-Z]+$/
  return reg.test(str)
}

/* 大小写字母*/
export function validateAlphabets(str) {
  const reg = /^[A-Za-z]+$/
  return reg.test(str)
}

/**
 * validate email
 * @param email
 * @returns {boolean}
 */
export function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return re.test(email)
}

export function isvalidPhone(phone) {
  const re = /^[1][3,4,5,7,8][0-9]{9}$/
  return re.test(phone)
}
