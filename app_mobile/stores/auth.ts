import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    waiter: null as { id: string; name: string } | null,
  }),

  actions: {
    // Initialize auth state from localStorage on app start
    initializeAuth() {
      if (process.client) {
        const savedAuth = localStorage.getItem('restaurant_auth')
        if (savedAuth) {
          try {
            const authData = JSON.parse(savedAuth)
            if (authData.isAuthenticated && authData.waiter) {
              this.isAuthenticated = authData.isAuthenticated
              this.waiter = authData.waiter
            }
          } catch (error) {
            console.error('Error parsing saved auth data:', error)
            localStorage.removeItem('restaurant_auth')
          }
        }
      }
    },

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
        
        // Save to localStorage
        if (process.client) {
          const authData = {
            isAuthenticated: this.isAuthenticated,
            waiter: this.waiter,
            loginTime: new Date().toISOString()
          }
          localStorage.setItem('restaurant_auth', JSON.stringify(authData))
        }
        
        return true
      }
      return false
    },

    logout() {
      this.isAuthenticated = false
      this.waiter = null
      
      // Clear localStorage
      if (process.client) {
        localStorage.removeItem('restaurant_auth')
      }
    },

    // Check if session is still valid (optional - for future use)
    validateSession() {
      if (process.client) {
        const savedAuth = localStorage.getItem('restaurant_auth')
        if (savedAuth) {
          try {
            const authData = JSON.parse(savedAuth)
            const loginTime = new Date(authData.loginTime)
            const now = new Date()
            const hoursSinceLogin = (now.getTime() - loginTime.getTime()) / (1000 * 60 * 60)
            
            // Optional: Auto-logout after 24 hours
            if (hoursSinceLogin > 24) {
              this.logout()
              return false
            }
            
            return true
          } catch (error) {
            console.error('Error validating session:', error)
            this.logout()
            return false
          }
        }
      }
      return false
    }
  }
})