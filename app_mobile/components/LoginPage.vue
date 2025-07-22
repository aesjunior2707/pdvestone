<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="card max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">comandaGO PDV</h1>
        <p class="text-sm text-gray-600">Sistema de Ponto de Venda</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username-name" class="block text-sm font-medium text-gray-700 mb-2">
            Usuário
          </label>
          <input
            id="username-name"
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
            placeholder="Digite seu nome de usuário"
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Senha
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
            placeholder="Digite sua senha"
          />
        </div>
        
        <!-- Remember Me Option -->
        <div class="flex items-center">
          <input
            id="remember-me"
            v-model="rememberMe"
            type="checkbox"
            class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"
          />
          <label for="remember-me" class="ml-2 text-sm text-gray-700">
            Manter-me conectado
          </label>
        </div>
        
        <button
          type="submit"
          class="w-full btn-primary"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Entrando...' : 'Entrar' }}
        </button>
        
        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>
      </form>
      
      <!-- Demo Credentials -->
      <div class="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 class="text-sm font-medium text-gray-700 mb-2">Credenciais de demonstração:</h4>
        <div class="text-sm text-gray-600">
          <p><strong>Usuário:</strong> admin</p>
          <p><strong>Senha:</strong> 123</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const rememberMe = ref(true)
const isLoading = ref(false)
const error = ref('')

// Load saved credentials if available
onMounted(() => {
  if (process.client) {
    const savedCredentials = localStorage.getItem('restaurant_credentials')
    if (savedCredentials) {
      try {
        const credentials = JSON.parse(savedCredentials)
        username.value = credentials.username || ''
        rememberMe.value = credentials.rememberMe !== false
      } catch (error) {
        console.error('Error loading saved credentials:', error)
      }
    }
  }
})

const handleLogin = async () => {
  if (!username.value || !password.value) return
  
  isLoading.value = true
  error.value = ''
  
  const success = authStore.login(username.value, password.value)

  if (success) {
    // Save credentials if remember me is checked
    if (rememberMe.value && process.client) {
      const credentials = {
        username: username.value,
        rememberMe: rememberMe.value
      }


      localStorage.setItem('restaurant_credentials', JSON.stringify(credentials))
    } else if (process.client) {
      // Clear saved credentials if remember me is unchecked
      localStorage.removeItem('restaurant_credentials')
    }
  } else {
    error.value = 'Credenciais inválidas. Tente novamente.'
  }
  
  isLoading.value = false
}
</script>