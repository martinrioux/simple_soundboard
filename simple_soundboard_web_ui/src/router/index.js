import Vue from 'vue'
import VueRouter from 'vue-router'
import Soundboard from '../components/Soundboard.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Soundboard',
    component: Soundboard
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
