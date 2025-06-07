<template>
  <div class="p-4">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">Mesas</h2>
      <p class="text-gray-600">Toque em uma mesa para gerenciar pedidos</p>
    </div>
    
    <div class="grid grid-cols-4 sm:grid-cols-5 md:grid-cols-6 gap-3">
      <button
        v-for="table in restaurantStore.tables"
        :key="table.id"
        @click="selectTable(table)"
        class="aspect-square rounded-xl border-2 transition-all duration-200 active:scale-95 flex flex-col items-center justify-center p-3 shadow-sm hover:shadow-md"
        :class="getTableStatusClass(table)"
      >
        <div class="text-xl font-bold mb-1">{{ table.number }}</div>
        <div class="text-xs font-medium capitalize opacity-80">
          {{ getTableStatusText(table) }}
<<<<<<< HEAD
=======
        </div>
        <div v-if="table.items.length > 0 || table.pendingItems.length > 0" class="text-xs mt-1 opacity-70">
          <div v-if="table.items.length > 0">
            {{ table.items.length }} confirmado{{ table.items.length !== 1 ? 's' : '' }}
          </div>
          <div v-if="table.pendingItems.length > 0" class="text-amber-600">
            {{ table.pendingItems.length }} pendente{{ table.pendingItems.length !== 1 ? 's' : '' }}
          </div>
>>>>>>> bacda74164eea3fa3530391690c05a3edb0836ab
        </div>
    
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRestaurantStore } from '~/stores/restaurant'

const restaurantStore = useRestaurantStore()

const selectTable = (table) => {
  restaurantStore.selectTable(table.id)
}

const getTableStatusClass = (table) => {
  if (table.pendingItems.length > 0) {
    return 'bg-amber-50 border-amber-300 text-amber-800 hover:bg-amber-100'
  } else if (table.status === 'occupied') {
    return 'table-occupied hover:bg-red-200'
  } else {
    return 'table-available hover:bg-emerald-200'
  }
}

const getTableStatusText = (table) => {
  if (table.pendingItems.length > 0) {
    return 'pendente'
  } else if (table.status === 'occupied') {
    return 'ocupado'
  } else {
    return 'disponível'
  }
}
</script>