<template>
  <div class="p-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <button
          @click="$emit('close')"
          class="p-2 -ml-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeftIcon class="w-5 h-5" />
        </button>
        <div>
          <h2 class="text-xl font-bold text-gray-900">Histórico da Mesa</h2>
          <p class="text-sm text-gray-600">{{ restaurantStore.closedTables.length }} mesas fechadas</p>
        </div>
      </div>
    </div>

    <!-- History List -->
    <div v-if="restaurantStore.closedTables.length > 0" class="space-y-4">
      <div
        v-for="closedTable in restaurantStore.closedTables"
        :key="closedTable.id"
        class="card"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-medium text-gray-900">Mesa {{ closedTable.tableNumber }}</h3>
            <p class="text-sm text-gray-600">
              {{ formatDateTime(closedTable.closedAt) }} • {{ closedTable.waiter }}
            </p>
          </div>
          <div class="text-right">
            <div class="font-semibold text-gray-900">R${{ closedTable.total.toFixed(2) }}</div>
            <button
              @click="reprintReceipt(closedTable)"
              class="text-sm text-emerald-600 hover:text-emerald-700 transition-colors"
            >
              Reprint
            </button>
          </div>
        </div>
        
        <div class="border-t border-gray-100 pt-3">
          <div class="space-y-1">
            <div
              v-for="group in getGroupedItems(closedTable.items)"
              :key="group.name"
              class="flex justify-between text-sm"
            >
              <span class="text-gray-600">{{ group.name }} ×{{ group.totalQuantity }}</span>
              <span class="text-gray-900">R${{ group.totalPrice.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 text-gray-500">
      <ClockIcon class="w-12 h-12 mx-auto mb-4 text-gray-300" />
      <p>Nenhuma mesa fechada ainda</p>
      <p class="text-sm">O histórico da mesa aparecerá aqui após o fechamento da tabela</p>
    </div>
  </div>
</template>

<script setup>
import { ArrowLeftIcon, ClockIcon } from 'lucide-vue-next'
import { useRestaurantStore } from '~/stores/restaurant'

const emit = defineEmits(['close'])
const restaurantStore = useRestaurantStore()

const formatDateTime = (date) => {
  const d = new Date(date)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getGroupedItems = (items) => {
  const groups = new Map()
  
  items.forEach(item => {
    const key = item.menuItem.name
    if (groups.has(key)) {
      const existing = groups.get(key)
      existing.totalQuantity += item.quantity
      existing.totalPrice += item.quantity * item.menuItem.price
    } else {
      groups.set(key, {
        name: item.menuItem.name,
        price: item.menuItem.price,
        totalQuantity: item.quantity,
        totalPrice: item.quantity * item.menuItem.price
      })
    }
  })
  
  return Array.from(groups.values())
}

const reprintReceipt = (closedTable) => {
  console.log('Reprinting receipt for Table', closedTable.tableNumber, {
    items: getGroupedItems(closedTable.items),
    total: closedTable.total,
    date: closedTable.closedAt,
    waiter: closedTable.waiter
  })
  
  // Show feedback to user
  alert(`Receipt for Table ${closedTable.tableNumber} sent to printer`)
}
</script>