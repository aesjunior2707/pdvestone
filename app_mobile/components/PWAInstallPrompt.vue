<template>
  <div
    v-if="showInstallPrompt"
    class="fixed bottom-4 left-4 right-4 bg-white border border-gray-200 rounded-lg shadow-lg p-4 z-50"
  >
    <div class="flex items-start space-x-3">
      <div class="flex-shrink-0">
        <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
          <DownloadIcon class="w-5 h-5 text-emerald-600" />
        </div>
      </div>
      <div class="flex-1 min-w-0">
        <h3 class="text-sm font-medium text-gray-900">Instalar COMAN PDV</h3>
        <p class="text-sm text-gray-600 mt-1">
          Adicione o app à sua tela inicial para acesso rápido e melhor experiência.
        </p>
      </div>
    </div>
    
    <div class="flex space-x-3 mt-4">
      <button
        @click="dismissPrompt"
        class="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
      >
        Agora não
      </button>
      <button
        @click="installApp"
        class="flex-1 px-4 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg transition-colors"
      >
        Instalar
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { DownloadIcon } from 'lucide-vue-next'

const showInstallPrompt = ref(false)
const deferredPrompt = ref(null)

const handleBeforeInstallPrompt = (e) => {
  // Prevent the mini-infobar from appearing on mobile
  e.preventDefault()
  // Stash the event so it can be triggered later
  deferredPrompt.value = e
  
  // Check if user has previously dismissed the prompt
  const dismissed = localStorage.getItem('pwa-install-dismissed')
  const dismissedTime = localStorage.getItem('pwa-install-dismissed-time')
  
  // Show prompt if not dismissed or if dismissed more than 7 days ago
  if (!dismissed || (dismissedTime && Date.now() - parseInt(dismissedTime) > 7 * 24 * 60 * 60 * 1000)) {
    showInstallPrompt.value = true
  }
}

const handleAppInstalled = () => {
  // Hide the install prompt
  showInstallPrompt.value = false
  deferredPrompt.value = null
  
  // Clear any dismissed state since app is now installed
  localStorage.removeItem('pwa-install-dismissed')
  localStorage.removeItem('pwa-install-dismissed-time')
}

const installApp = async () => {
  if (!deferredPrompt.value) return
  
  // Show the install prompt
  deferredPrompt.value.prompt()
  
  // Wait for the user to respond to the prompt
  const { outcome } = await deferredPrompt.value.userChoice
  
  if (outcome === 'accepted') {
    console.log('User accepted the install prompt')
  } else {
    console.log('User dismissed the install prompt')
  }
  
  // Clear the deferredPrompt
  deferredPrompt.value = null
  showInstallPrompt.value = false
}

const dismissPrompt = () => {
  showInstallPrompt.value = false
  
  // Remember that user dismissed the prompt
  localStorage.setItem('pwa-install-dismissed', 'true')
  localStorage.setItem('pwa-install-dismissed-time', Date.now().toString())
}

onMounted(() => {
  // Only add listeners on client side
  if (process.client) {
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    window.addEventListener('appinstalled', handleAppInstalled)
  }
})

onUnmounted(() => {
  if (process.client) {
    window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    window.removeEventListener('appinstalled', handleAppInstalled)
  }
})
</script>