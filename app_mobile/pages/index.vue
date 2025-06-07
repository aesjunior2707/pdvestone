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
</script>