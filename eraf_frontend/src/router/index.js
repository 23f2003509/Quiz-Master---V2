
import { createRouter, createWebHistory } from 'vue-router'

import ErafLanding from '@/components/ErafLanding.vue'
import ErafLogin from '@/components/ErafLogin.vue'
import ErafAdminDashboard from '@/components/ErafAdminDashboard.vue'
import ErafSignup from '@/components/Eraf_Signup.vue'
import Eraf_ManageSubjects from '@/components/Eraf_ManageSubjects.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ErafLanding,
    },
    {
      path: '/login',
      name: 'login',
      component: ErafLogin,
    },
    {
      path: '/signup',
      name: 'signup',
      component: ErafSignup,

    },
    {
      path: '/admin',
      name: 'admin',
      component: ErafAdminDashboard,
    },
    {
      path: '/manage_subjects',
      name: 'manage_subjects',
      component: Eraf_ManageSubjects,
    }
   
   
  ],
})

export default router
