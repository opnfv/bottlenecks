// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import '../node_modules//bootstrap/dist/css/bootstrap.min.css'
import '../node_modules/font-awesome/css/font-awesome.min.css'
import './assets/css/style.css'
import 'animate.css'
import './assets/css/mystyle.css'
import './assets/css/wf-graph.css'
import './assets/css/toastr.min.css'

import $ from './assets/js/jquery-vendor.js'
import 'bootstrap'
import 'metismenu'
import slimScroll from 'jquery-slimscroll'

import './assets/js/inspinia.js'
import './assets/js/pace.min.js'
import './assets/js/toastr.min.js'
import Vue from 'vue'
import global from './Global'
import App from './App'
import router from './router'
Vue.config.productionTip = false
Vue.prototype.global = global
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
