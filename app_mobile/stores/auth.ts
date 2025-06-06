import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    waiter: null as { id: string; name: string } | null,
  }),

  actions: {
    login(waiterName: string, password: string) {
      // Simple authentication - in production, this would be a proper API call
      const validWaiters = [
        { id: '4', name: 'admin', password: '123' }
      ]

      const waiter = validWaiters.find(w => 
        w.name.toLowerCase() === waiterName.toLowerCase() && w.password === password
      )

      if (waiter) {
        this.isAuthenticated = true
        this.waiter = { id: waiter.id, name: waiter.name }
        return true
      }
      return false
    },

    logout() {
      this.isAuthenticated = false
      this.waiter = null
    }
  }
})