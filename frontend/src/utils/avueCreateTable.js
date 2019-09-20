/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2019-01
 *  获取form表结构
 */
const renderer = require('./index')
const tableConst = require('./avueTableConst')

export function getTableInfoB(that) {
  that.masterApi.get_table_info(that.masterUri).then(response => {
    that.tableOpiton.column = getTableColumns1(that, response)
  })
}

function getTableColumns1(that, respRet) {
  var fields = respRet.fields
  var dictNameList = {}
  var valueDefaultList = []

  //type
  var selectColsNameList = []
  var selectMultipleNameList = []
  var textareaColsNameList = []
  var radioColsNameList = []
  var datetimeNameList = []
  var dateNameList = []
  var timeNameList = []

  //required
  var rulesColsNameList = []

  //visdiplay	全部是否可见
  var noVisdiplayColsNameList = []

  //表单编辑是否可见
  var editVisNodiplayList = []
  var addVisNodiplayList = []

  //sort
  var sortableColsNameList = []

  // 顺序 vue 优先，后端其次,其次默认
  var afterList = []
  var showCols = []

  //表格列隐藏
  var hiddenCols = []

  //password
  var passwordColsList = []

  //search
  var searchList = []
  var searchMList = []

  //规则 必须且只能在页面中写js
  var selectCols = that.selectCols
  var radioCols = that.radioCols
  var rulesCols = that.rulesCols
  var noSearchList = that.noSearchList

  for (var key in respRet) {
    //select kv
    if (key == "field_select_kv") {
      for (var i = 0; i < respRet[key].length; i++) {
        for (var selectKV in respRet[key][i]) {
          var d = {}
          d["dictData"] = renderer.conver2KV(['value', 'label'], respRet[key][i][selectKV])
          d["filters"] = renderer.conver2KV(['value', 'text'], respRet[key][i][selectKV])
          dictNameList[selectKV] = d
        }
      }
    } else if (key == 'field_default') {
      valueDefaultList = respRet[key]
    } else if (key == 'field_type') {
      for (var typeKey in respRet[key]) {
        if (typeKey == 'select') {
          selectColsNameList = respRet[key][typeKey]
        } else if (typeKey == 'textarea') {
          textareaColsNameList = respRet[key][typeKey]
        } else if (typeKey == 'radio') {
          radioColsNameList = respRet[key][typeKey]
        } else if (typeKey == 'datetime') {
          datetimeNameList = respRet[key][typeKey]
        } else if (typeKey == 'date') {
          dateNameList = respRet[key][typeKey]
        } else if (typeKey == 'time') {
          timeNameList = respRet[key][typeKey]
        } else if (typeKey == 'select_mul') {
          selectMultipleNameList = respRet[key][typeKey]
        }
      }
    } else if (key == "field_required") {
      rulesColsNameList = respRet[key]
    } else if (key == "field_add_remove") {
      that.cRemoveList = respRet[key]

    } else if (key == "field_update_remove") {
      that.uRemoveList = respRet[key]
    } else if (key == "field_add_novis") {
      editVisNodiplayList = respRet[key]
      addVisNodiplayList = respRet[key]
    } else if (key == "field_edit_novis") {
      editVisNodiplayList = respRet[key]

      // search
    } else if (key == "field_search") {
      searchList = respRet[key]
    } else if (key == "field_search_mul") {
      searchMList = respRet[key]
    } else if (key == "field_password") {
      passwordColsList = respRet[key]
    } else if (key == "field_show_order") {
      showCols = respRet[key]
    } else if (key == "field_after_order") {
      afterList = respRet[key]
    } else if (key == "field_hidden") {
      hiddenCols = respRet[key]
    } else if (key == "field_no_visdiplay") {
      noVisdiplayColsNameList = respRet[key]
    }
  }

  if (addVisNodiplayList.length < 1) {
    if (that.hasOwnProperty("addVisNodiplayList")) {
      addVisNodiplayList = that.addVisNodiplayList
    } else {
      addVisNodiplayList = tableConst.cRemoveListDef
    }
  }
  if (editVisNodiplayList.length < 1) {
    if (that.hasOwnProperty("editVisNodiplayList")) {
      editVisNodiplayList = that.editVisNodiplayList
    } else {
      editVisNodiplayList = tableConst.uRemoveListDef
    }
  }
  if (searchList.length < 1) {
    if (that.hasOwnProperty("searchList")) {
      searchList = that.searchList
    }
  }
  if (that.hasOwnProperty("searchMList") && that.searchMList > 0) {
    searchMList = that.searchMList
  }
  if (passwordColsList.length < 1) {
    if (that.hasOwnProperty("passwordColsList")) {
      passwordColsList = that.passwordColsList
    }
  }
  if (afterList.length < 1) {
    if (that.hasOwnProperty("afterList")) {
      afterList = that.afterList
    } else {
      afterList = tableConst.afterListDef
    }
  }
  //顺序 vue优先
  if (that.hasOwnProperty("showCols") && that.showCols.length > 0) {
    showCols = that.showCols
  }
  if (that.hasOwnProperty("hiddenCols") && that.hiddenCols.length > 0) {
    hiddenCols = that.hiddenCols
  }
  //不显示
  if (that.hasOwnProperty("noVisdiplayColsNameList") && that.noVisdiplayColsNameList.length > 0) {
    noVisdiplayColsNameList = that.noVisdiplayColsNameList
  }
  if (noVisdiplayColsNameList.length < 1 && addVisNodiplayList > 0) {
    noVisdiplayColsNameList = addVisNodiplayList
  }

  //start deal fields
  var afterColumns = []
  var tableColumns = []
  for (var key in fields) {
    var column = {}
    //select
    if (renderer.isInArray(selectColsNameList, key)) {
      var num = renderer.isInArrayNum(selectCols, key)
      if (num >= 0) {
        column = selectCols[num]
      } else {
        column = tableConst.getfilterMethod(key)[0]
      }

      for (var k in dictNameList) {
        if (key == k) {
          column.dicData = dictNameList[k]["dictData"]
          column.filters = dictNameList[k]["filters"]
        }
      }
      column.type = 'select'
      column.filterable = true
    }
    if (column.type == 'select' && renderer.isInArray(selectMultipleNameList, key)) {
      column.multiple = true
    }


    if (renderer.isInArray(radioColsNameList, key)) {
      var flag = 0
      for (var h = 0; h < radioCols.length; h++) {
        if (key == radioCols[h].prop) {
          flag = 1
          column = radioCols[h]
          break;
        }
      }
      if (flag == 0) {
        column.dicData = tableConst.DIC.VAILD
        column.mock = {"type": "dic"}
      }
      column.type = 'radio'
    }

    column.label = fields[key]
    column.prop = key
    if (column.type != 'select' && renderer.isInArray(datetimeNameList, column.prop)) {
      column.type = 'datetime'
      column.format = 'yyyy-MM-dd HH:mm:ss'
      column.valueFormat = 'yyyy-MM-dd HH:mm:ss'
      column.mock = {
        'type': 'datetime',
        'format': 'yyyy-MM-dd HH:mm:ss',
        'now': true,
      }
    }
    if (column.type != 'select' && renderer.isInArray(dateNameList, column.prop)) {
      column.type = 'date'
      column.format = 'yyyy-MM-dd'
      column.valueFormat = 'yyyy-MM-dd'
      column.mock = {
        'type': 'date',
        'format': 'yyyy-MM-dd',
        'now': true,
      }
    }

    if (column.type != 'select' && renderer.isInArray(timeNameList, column.prop)) {
      column.type = 'time'
      column.valueFormat = "HH:mm:ss"
    }
    if (renderer.isInArray(rulesColsNameList, column.prop)) {
      var flag = false
      if (rulesCols.length > 0) {
        for (var j = 0; j < rulesCols.length; j++) {
          if (rulesCols[j].prop == column.prop) {
            column.rules = rulesCols[j].rules
            flag = true
            break
          }
        }
      }
      if (!flag) {
        column.rules = [{
          "required": true,
          "message": "please input " + column.prop,
          "trigger": "blur"
        }]
      }
    }

    if (renderer.isInArray(passwordColsList, column.prop)) {
      column.type = 'password'
    }

    if (renderer.isInArray(noVisdiplayColsNameList, column.prop)) {
      column.visdiplay = false
    }
    if (renderer.isInArray(sortableColsNameList, column.prop)) {
      column.sortable = true
    }
    if (renderer.isInArray(searchList, column.prop) && !renderer.isInArray(noSearchList, column.prop)) {
      column.search = true
    }
    if (renderer.isInArray(searchMList, column.prop)) {
      column.searchDefault = []
      column.searchMmultiple = true
    }
    if (renderer.isRealArr(showCols)) {
      if (!renderer.isInArray(showCols, key)) {
        column.hide = true
      }
    }
    if (renderer.isRealArr(hiddenCols) && renderer.isInArray(hiddenCols, key)) {
      column.hide = true
    }

    //默认值
    if (valueDefaultList != null && valueDefaultList != undefined && valueDefaultList.length > 0) {
      for (var l = 0; l < valueDefaultList.length; l++) {
        for (var vdefault in valueDefaultList[l]) {
          if (vdefault == column.prop) {
            column.valueDefault = valueDefaultList[l][vdefault]
            break
          }
        }
      }
    }

    //是否是 textarea
    if (renderer.isInArray(textareaColsNameList, column.prop)) {
      column.type = "textarea"
    }

    if (renderer.isInArray(afterList, column.prop)) {
      afterColumns.push(column)
    } else {
      tableColumns.push(column)
    }
    if (renderer.isInArray(editVisNodiplayList, column.prop)) {
      column.editVisdiplay = false
    }
    if (renderer.isInArray(addVisNodiplayList, column.prop)) {
      column.addVisdiplay = false
    }
  }

  for (var i = 0; i < afterColumns.length; i++) {
    tableColumns.push(afterColumns[i])
  }

  //排序重新
  if (renderer.isRealArr(showCols)) {
    var frontColList = []
    var frontColNameList = []
    var endColList = []
    var endColNameList = []
    for (var i = 0; i < showCols.length; i++) {
      for (var k = 0; k < tableColumns.length; k++) {
        if (showCols[i] == tableColumns[k].prop && !renderer.isInArray(frontColNameList, tableColumns[k].prop)) {
          frontColList.push(tableColumns[k])
          break
        } else if (!renderer.isInArray(endColNameList, tableColumns[k].prop) && !renderer.isInArray(showCols, tableColumns[k].prop)) {
          endColNameList.push(tableColumns[k].prop)
          endColList.push(tableColumns[k])
        }
      }
    }
    for (var k = 0; k < tableColumns.length; k++) {
      if (!renderer.isInArray(showCols, tableColumns[k].prop) && !renderer.isInArray(endColNameList, tableColumns[k].prop)) {
        endColNameList.push(tableColumns[k].prop)
        endColList.push(tableColumns[k])
      }
    }
    tableColumns = frontColList.concat(endColList)
  }

  return tableColumns
}

