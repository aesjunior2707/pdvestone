<template>
  <div class="min-h-screen">
    <LoginPage v-if="!authStore.isAuthenticated" />
    <DashboardLayout v-else />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

// Initialize authentication state on app load
onMounted(() => {
  authStore.initializeAuth()
})

// Set page meta for PWA
useHead({
  title: 'ESTONE PDV - Sistema de Ponto de Venda',
  meta: [
    { name: 'description', content: 'Sistema completo de ponto de venda para restaurantes' },
    { name: 'theme-color', content: '#059669' },
    { name: 'apple-mobile-web-app-capable', content: 'yes' },
    { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
    { name: 'apple-mobile-web-app-title', content: 'ESTONE PDV' },
    { name: 'mobile-web-app-capable', content: 'yes' },
    { name: 'msapplication-TileColor', content: '#059669' },
    { name: 'msapplication-tap-highlight', content: 'no' }
  ],
  link: [
    { rel: 'apple-touch-icon', href: '/pwa-192x192.png' },
    { rel: 'mask-icon', href: '/pwa-192x192.png', color: '#059669' }
  ]
})
</script>