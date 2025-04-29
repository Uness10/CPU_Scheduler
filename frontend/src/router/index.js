import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/visualization',
    name: 'visualization',
    component: () => import(/* webpackChunkName: "visualization" */ '../views/VisualizationView.vue')
  },
  {
    path: '/comparison',
    name: 'comparison',
    component: () => import(/* webpackChunkName: "comparison" */ '../views/ComparisonView.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
