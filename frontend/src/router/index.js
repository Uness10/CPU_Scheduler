import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProcessesView from '../views/ProcessesView.vue'
import VisualizationView from '../views/VisualizationView.vue'
import ComparisonView from '../views/ComparisonView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'CPU Scheduler Simulator' }
  },
  {
    path: '/processes',
    name: 'processes',
    component: ProcessesView,
    meta: { title: 'Create/Generate Processes' }
  },
  {
    path: '/visualization',
    name: 'visualization',
    component: VisualizationView,
    meta: { title: 'Scheduler Visualization' }
  },
  {
    path: '/comparison',
    name: 'comparison',
    component: ComparisonView,
    meta: { title: 'Algorithm Comparison' }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: { title: 'About CPU Scheduling Algorithms' }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'CPU Scheduler Simulator';
  next();
})

export default router
