<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="card max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">ESTONE PDV</h1>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="waiter-name" class="block text-sm font-medium text-gray-700 mb-2">
            Username
          </label>
          <input
            id="waiter-name"
            v-model="waiterName"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
            placeholder="Enter your name"
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
            placeholder="Enter your password"
          />
        </div>
        
        <button
          type="submit"
          class="w-full btn-primary"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
        
        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>
      </form>
      
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

const waiterName = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!waiterName.value || !password.value) return
  
  isLoading.value = true
  error.value = ''
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500))
  
  const success = authStore.login(waiterName.value, password.value)
  
  if (!success) {
    error.value = 'Invalid credentials. Please try again.'
  }
  
  isLoading.value = false
}
</script>