// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: false },
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@vite-pwa/nuxt'
  ],
  css: ['~/assets/css/main.css'],
  ssr: false,
  runtimeConfig: {
    public: {
      appName: 'RestaurantPOS'
    }
  },
  pwa: {
    registerType: 'autoUpdate',
    workbox: {
      navigateFallback: '/',
      globPatterns: ['**/*.{js,css,html,png,svg,ico}'],
      runtimeCaching: [
        {
          urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'google-fonts-cache',
            expiration: {
              maxEntries: 10,
              maxAgeSeconds: 60 * 60 * 24 * 365 // <== 365 days
            },
            cacheKeyWillBeUsed: async ({ request }) => {
              return `${request.url}?${Date.now()}`
            }
          }
        },
        {
          urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'gstatic-fonts-cache',
            expiration: {
              maxEntries: 10,
              maxAgeSeconds: 60 * 60 * 24 * 365 // <== 365 days
            }
          }
        }
      ]
    },
    client: {
      installPrompt: true,
      periodicSyncForUpdates: 20
    },
    devOptions: {
      enabled: true,
      suppressWarnings: true,
      navigateFallbackAllowlist: [/^\/$/],
      type: 'module'
    },
    manifest: {
      name: 'ESTONE PDV - Sistema de Ponto de Venda',
      short_name: 'ESTONE PDV',
      description: 'Sistema completo de ponto de venda para restaurantes',
      theme_color: '#059669',
      background_color: '#f9fafb',
      display: 'standalone',
      orientation: 'portrait',
      scope: '/',
      start_url: '/',
      icons: [
        {
          src: '/pwa-192x192.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: '/pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png'
        },
        {
          src: '/pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any maskable'
        }
      ],
      categories: ['business', 'productivity', 'utilities'],
      shortcuts: [
        {
          name: 'Mesas',
          short_name: 'Mesas',
          description: 'Ver todas as mesas',
          url: '/',
          icons: [{ src: '/pwa-192x192.png', sizes: '192x192' }]
        },
        {
          name: 'Histórico',
          short_name: 'Histórico',
          description: 'Ver histórico de vendas',
          url: '/?history=true',
          icons: [{ src: '/pwa-192x192.png', sizes: '192x192' }]
        }
      ]
    }
  }
})