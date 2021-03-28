import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/create',
    name: 'Create',
    component: () => import('../views/CreateWallet.vue')
  },
  {
    path: '/registration',
    name: 'Registration',
    component: () => import('../views/Registration.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/get-seed',
    name: 'GetSeed',
    component: () => import('../views/GettingSeed.vue')
  },
  {
    path: '/confirm-seed',
    name: 'ConfirmSeed',
    component: () => import('../views/ConfirmSeed.vue')
  },
  {
    path: '/uikit',
    name: 'UIKit',
    component: () => import('../views/Ui.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
