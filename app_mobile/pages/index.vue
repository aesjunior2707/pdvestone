<template>
  <div class="min-h-screen">
    <LoginPage v-if="!authStore.isAuthenticated" />
    <DashboardLayout v-else />
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
</script>