/**
* author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
* create:2018-09
 * 获取form表结构常量参数
 */

export const DIC = {
  VAILD: [{
    label: '是',
    value: true
  }, {
    label: '否',
    value: false
  }],
}

export const tableOpitonSearchM = {
  addBtn: true,
  searchBtn: true,
  selection: true,
  border: true,
  page: true,
  align: 'center',
  menuAlign: 'center',
  menuWidth: 272,
  searchMenuSpan: 6,
  viewBtn: true,
  column: [
    {
      prop: 'u8',
      search: true
    },
  ]
}

export const tableOpitonSearchMenuM = {
  addBtn: true,
  searchBtn: true,
  selection: true,
  border: true,
  page: true,
  viewBtn: true,
  align: 'center',
  menuAlign: 'center',
  menuWidth: 100,
  searchMenuSpan: 6,
  menuType: 'menu',
  column: [
    {
      prop: 'u8',
      search: true
    },
  ]
}

export const tableOptNoEditSearchM = {
  addBtn: false,
  editBtn: false,
  delBtn: false,
  viewBtn: true,
  searchBtn: true,
  selection: true,
  border: true,
  page: true,
  align: 'center',
  menuAlign: 'center',
  menuWidth: 100,
  searchMenuSpan: 6,
  column: [
    {
      prop: 'u8',
      search: true
    },
  ]
}
export const tableNoOptAdExtMenuSearchM = {
  addBtn: false,
  editBtn: false,
  delBtn: false,
  searchBtn: true,
  selection: true,
  border: true,
  page: true,
  align: 'center',
  menuAlign: 'center',
  menuWidth: 180,
  searchMenuSpan: 6,
  viewBtn: false,
  column: [
    {
      prop: 'u8',
      search: true
    },
  ]
}
export const tableNoOptNoMenuSearchM = {
  addBtn: false,
  editBtn: false,
  delBtn: false,
  searchBtn: true,
  selection: true,
  border: true,
  page: true,
  align: 'center',
  searchMenuSpan: 6,
  menu: false,
  viewBtn: false,
  column: [
    {
      prop: 'u8',
      search: true
    },
  ]
}
export const tableOpitonM = {
  addBtn: true,
  searchBtn: false,
  selection: true,
  border: true,
  page: true,
  align: 'center',
  menuAlign: 'center',
  menuWidth: 272,
  searchMenuSpan: 6,
  viewBtn: true,
  column: []
}

export const tableOptNoEditM = {
  addBtn: false,
  editBtn: false,
  delBtn: false,
  viewBtn: true,
  searchBtn: true,
  selection: true,
  border: true,
  page: true,
  align: 'center',
  menuAlign: 'center',
  menuWidth: 100,
  searchMenuSpan: 6,
  column: []
}

export function getfilterMethod(objName) {
  return [
    {
      filterMethod: function (value, row, column) {
        return row[objName] === value;
      }
    }]
}

export const cRemoveListDef = ['id', "create_time", "update_time"]
export const uRemoveListDef = ['id', "create_time", "update_time"]
export const afterListDef = ['remark', "create_time", "update_time"]


