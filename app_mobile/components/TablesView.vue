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
        :class="table.status === 'available' ? 'table-available hover:bg-emerald-200' : 'table-occupied hover:bg-red-200'"
      >
        <div class="text-xl font-bold mb-1">{{ table.number }}</div>
        <div v-if="table.status === 'available'" class="text-xs font-medium capitalize opacity-80">disponível</div>
        <div v-else class="text-xs font-medium capitalize opacity-80">ocupado</div>
        <div v-if="table.items.length > 0" class="text-xs mt-1 opacity-70">
          {{ table.items.length }} item{{ table.items.length !== 1 ? 's' : '' }}
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
</script>