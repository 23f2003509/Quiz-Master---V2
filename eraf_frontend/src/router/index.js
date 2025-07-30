
import { createRouter, createWebHistory } from 'vue-router'

import ErafLanding from '@/components/ErafLanding.vue'
import ErafLogin from '@/components/ErafLogin.vue'
import ErafAdminDashboard from '@/components/ErafAdminDashboard.vue'
import ErafSignup from '@/components/Eraf_Signup.vue'
import Eraf_ManageSubjects from '@/components/Eraf_ManageSubjects.vue'


import Eraf_ManageQuiz from '@/components/Eraf_ManageQuiz.vue'
import Eraf_QuizQuestions from '@/components/Eraf_QuizQuestions.vue'

import Eraf_UserDashboard from '@/components/Eraf_UserDashboard.vue'
import Eraf_StartQuiz from '@/components/Eraf_StartQuiz.vue'
import Eraf_UserSummary from '@/components/Eraf_UserSummary.vue'

import Eraf_ManageUser from '@/components/Eraf_ManageUser.vue'

import Eraf_AdminSummary from '@/components/Eraf_AdminSummary.vue'

function requireAdminAuth(to, from, next) {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    next('/login');
  } else {
    next();
  }
}



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
      beforeEnter: requireAdminAuth
    },
    {
      path: '/manage_subjects',
      name: 'manage_subjects',
      component: Eraf_ManageSubjects,
      beforeEnter: requireAdminAuth
    },
    {
      path: '/manage_quizs',
      name: 'manage_quizs',
      component: Eraf_ManageQuiz,
      beforeEnter: requireAdminAuth
    },
    {
      path: '/manage_users',
      name: 'manage_users',
      component: Eraf_ManageUser,
      beforeEnter: requireAdminAuth
    },
    {
      path: '/quiz_questions/:quizId',
      name: 'quiz_questions',
      component: Eraf_QuizQuestions,
      beforeEnter: requireAdminAuth
    },


    {
      path: '/user',
      name: 'user',
      component: Eraf_UserDashboard,
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('user_token');
        if (!token) {
          next('/login');
        } else {
          next();
        }
      }

    },
    {
      path: '/start_quiz/:quizId',
      name: 'start_quiz',
      component: Eraf_StartQuiz,
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('user_token');
        if (!token) {
          next('/login');
        } else {
          next();
        }
      }
    },
    {
      path: '/user_summary',
      name: 'user_summary',
      component: Eraf_UserSummary,
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('user_token');
        if (!token) {
          next('/login');
        } else {
          next();
        }
      }
    },
    {
      path: '/admin_summary',
      name: 'admin_summary',
      component: Eraf_AdminSummary,
      beforeEnter: requireAdminAuth
    },
   
   
  ],
})

export default router
