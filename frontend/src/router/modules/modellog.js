/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * 日志页面路由
 */

import Layout from '@/views/layout/Layout'

const modellogRouter = {
  path: '/modellog',
  component: Layout,
  redirect: '/modellog/logsentry',
  name: 'Modellog',
  meta: {
    title: 'modellog',
    icon: 'log_1'
  },
  children: [
    {
      path: 'logsentrys',
      component: () => import('@/views/modellog/logSentry'),
      name: 'logSentryList',
      meta: { title: 'logSentryList' }
    }
  ]
}
export default modellogRouter
