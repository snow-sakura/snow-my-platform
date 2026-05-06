import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/Layout.vue'),
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/ProjectList.vue')
        },
        {
          path: '/project/:id',
          name: 'ProjectDetail',
          component: () => import('@/views/ProjectDetail.vue'),
          children: [
            {
              path: 'documents',
              name: 'Documents',
              component: () => import('@/views/Documents.vue')
            },
            {
              path: 'test-points',
              name: 'TestPoints',
              component: () => import('@/views/TestPoints.vue')
            },
            {
              path: 'knowledge-bases',
              name: 'KnowledgeBases',
              component: () => import('@/views/KnowledgeBases.vue')
            },
            {
              path: 'test-cases',
              name: 'TestCases',
              component: () => import('@/views/TestCases.vue')
            }
          ]
        },
        {
          path: '/settings',
          name: 'Settings',
          component: () => import('@/views/Settings.vue')
        }
      ]
    }
  ]
})

export default router
