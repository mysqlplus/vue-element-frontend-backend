/**
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * 路由 index
 */

import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/views/layout/Layout'
import userRouter from './modules/user'
import cmdbRouter from './modules/cmdb'
import modellogRouter from './modules/modellog'
/** note: Submenu only appear when children.length>=1
 *  detail see  https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 **/

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']     will control the page roles (you can set multiple roles)
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
    noCache: true                if true ,the page will no be cached(default is false)
  }
 **/
export const constantRouterMap = [
 {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/user/login/index'),
    hidden: true
  },

  {
    path: '/resetpwd',
    component: () => import('@/views/user/resetpwd'),
    hidden: true
  },
  {
    path: '/user',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/user/resetpwd',
        component: () => import('@/views/user/pwdreset'),
        name: 'resetPassword',
        meta: {title: 'userResetPwd'}
      },
      {
        path: '/user/changepwd',
        component: () => import('@/views/user/pwdchange'),
        name: 'changePassword',
        meta: {title: 'userChangePwd'}
      },
      {
        path: '/user/info',
        component: () => import('@/views/user/info'),
        name: 'userinfo',
        meta: {title: 'userInfo'}
      },
    ]
  },


  {
    path: '/auth-redirect',
    component: () => import('@/views/user/login//authredirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/errorPage/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/errorPage/401'),
    hidden: true
  },
  {
    path: '/502',
    component: () => import('@/views/errorPage/502'),
    hidden: true
  },
  {
    path: '',
    component: Layout,
    redirect: 'dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: {title: 'dashboard', icon: 'dashboard', noCache: true}
      }
    ]
  }
]

export default new Router({
  scrollBehavior: () => ({y: 0}),
  routes: constantRouterMap
})

export const asyncRouterMap = [
  cmdbRouter,
  userRouter,
  modellogRouter,
  {path: '*', redirect: '/404', hidden: true}
]
