import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

function beforeEnter (to: any, from: any, next: any) {
  if (!store.getters.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
}


const routerOptions = [
  { 
    path: '/login',
    name: 'login', 
    component: 'Login' 
  }, { 
    path: '/student/home',
    name: 'studentHome', 
    component: 'StudentHome',
    beforeEnter: beforeEnter
  }, { 
    path: '/tutor/home',
    name: 'tutorHome', 
    component: 'TutorHome',
    beforeEnter: beforeEnter,
  }, {
    path: '/register',
    name: 'register',
    component: 'Register'
  }, {
    path: '/student/:subject',
    name: 'progress',
    props: true,
    component: 'Progress',
    beforeEnter: beforeEnter
  }, {
    path: '/tutor/:subject_name/:group_id',
    name: 'GroupSubjectInfo',
    props: true,
    component: 'GroupSubjectInfo',
    beforeEnter: beforeEnter
  }, {
    path: '/logout',
    name: 'logout',
    component: 'Logout',
    beforeEnter: beforeEnter
  }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
