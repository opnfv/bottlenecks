// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './assets/css/bootstrap.min.css'
import './assets/css/font-awesome.css'
import './assets/css/style.css'
import './assets/css/animate.css'
import './assets/css/TheStyle.css'
import './assets/css/wf-graph.css'
import './assets/css/toastr.min.css'
import './assets/js/jquery-3.3.1.js'
import './assets/js/bootstrap.min.js'
import './assets/js/jquery.metisMenu.js'
import './assets/js/jquery.slimscroll.min.js'
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
