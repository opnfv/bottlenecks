import Vue from 'vue'
import Router from 'vue-router'
import testsuite from '@/components/testsuite'
import testcase from '@/components/testcase'
import testcase_content from '@/components/testcase_content'
import test_result from '@/components/test_result'
import environment from '@/components/environment'
Vue.use(Router)

const Report = {
  template: "<div></div>"
}
export default new Router({
  routes: [
    {
      path: '/',
      name: 'testsuite',
      component: testsuite
    },
    {
      path: '/testcase',
      name: 'testcase',
      component: testcase
    },
    {
      path: '/content',
      name: 'testcase_content',
      component: testcase_content
    },
    {
      path: '/result',
      name: 'result',
      component: test_result
    },
    {
      path: '/report',
      name: 'report',
      component: Report
    },
    {
      path: '/environment',
      name: 'environment',
      component: environment
    }
  ]
})
