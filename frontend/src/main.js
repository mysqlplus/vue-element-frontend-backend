/**
 * init from panjiachen
 * author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
 * create:2018-07
 */
import Vue from 'vue'

import Cookies from 'js-cookie'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import '@/styles/index.scss' // global css

import App from './App'
import router from './router'
import store from './store'
import formCreate from "form-create/element"
import i18n from './lang' // Internationalization
import './icons' // icon
import './errorLog' // error log
import './permission' // permission control

import * as filters from './filters' // global filters

import Avue from '@smallwei/avue';
import '@/styles/index_avue.css';

Vue.use(Avue, { size: 'mini'});

import VCharts from 'v-charts'
Vue.use(VCharts)

Vue.use(Element, {
  size: Cookies.get('size') || 'mini', // set element-ui default size
  i18n: (key, value) => i18n.t(key, value)
})

Vue.use(formCreate)


// register global utility filters.

Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false


Vue.directive('noMoreClick', {
  inserted(el, binding) {
    el.addEventListener('click', e => {
      el.classList.add('is-disabled');
      el.disabled = true;
      setTimeout(() => {
        el.disabled = false;
        el.classList.remove('is-disabled');
      }, 3000)
    })
  }
});

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: h => h(App)
})
