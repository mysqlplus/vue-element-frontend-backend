/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * 资产管理路由
 */

import Layout from '@/views/layout/Layout'

const cmdbRouter = {
  path: '/cmdb',
  component: Layout,
  redirect: '/cmdb/idcs/',
  name: 'Cmdb',
  meta: {
    title: 'cmdb',
    icon: 'cmdb'
  },
  children: [
    {
      path: 'idcs',
      component: () => import('@/views/cmdb/idc'),
      name: 'idcList',
      meta: { title: 'idcList' }
    },
     {
      path: 'hosts',
      component: () => import('@/views/cmdb/host'),
      name: 'hostList',
      meta: { title: 'hostList' }
    },
  ]
}
export default cmdbRouter
