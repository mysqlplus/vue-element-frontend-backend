
/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * 用户页面路由
 */

import Layout from '@/views/layout/Layout'

const userRouter = {
  path: '/users',
  component: Layout,
  redirect: '/user/info',
  name: 'User',
  meta: {
    title: 'user',
    icon: 'user'
  },
  children: [
    {
      path: 'users',
      component: () => import('@/views/user/user'),
      name: 'userList',
      meta: { title: 'userList' }
    },
    {
      path: 'roles',
      component: () => import('@/views/user/role'),
      name: 'roleList',
      meta: { title: 'roleList' }
    },
    {
      path: 'urls',
      component: () => import('@/views/user/url'),
      name: 'urlList',
      meta: { title: 'urlList' }
    },
  ]
}
export default userRouter
