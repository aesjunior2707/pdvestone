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
          <p class="text-sm text-gray-600">{{ filteredTables.length }} mesas encontradas</p>
        </div>
      </div>
    </div>

    <!-- Date Filter -->
    <div class="mb-6">
      <div class="flex items-center">
        <div class="w-48">
          <label for="date-filter" class="block text-sm font-medium text-gray-700 mb-2">
            Filtrar por data
          </label>
          <input
            id="date-filter"
            v-model="selectedDate"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
          />
        </div>
        <button
          @click="clearFilter"
          class="mt-6 ml-1 px-4 py-2 text-sm text-white rounded-lg transition-colors"
          style="background-color: #EF5350;"
          onmouseover="this.style.backgroundColor='#E53935'"
          onmouseout="this.style.backgroundColor='#EF5350'"
        >
          Limpar
        </button>
      </div>
      
      <!-- Quick Date Buttons -->
      <div class="flex space-x-2 mt-3">
        <button
          @click="setToday"
          class="px-3 py-1 text-xs bg-emerald-100 text-emerald-700 rounded-full hover:bg-emerald-200 transition-colors"
          :class="{ 'ring-2 ring-emerald-300': isToday }"
        >
          Hoje
        </button>
        <button
          @click="setYesterday"
          class="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
          :class="{ 'ring-2 ring-gray-300': isYesterday }"
        >
          Ontem
        </button>
        <button
          @click="setThisWeek"
          class="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
          :class="{ 'ring-2 ring-blue-300': isThisWeek }"
        >
          Esta semana
        </button>
      </div>
      
      <!-- Results Summary -->
      <div v-if="selectedDate" class="mt-3 text-sm text-gray-600">
        Mostrando resultados para: <span class="font-medium">{{ formatSelectedDate }}</span>
      </div>
    </div>

    <!-- History List -->
    <div v-if="filteredTables.length > 0" class="space-y-4">
      <div
        v-for="closedTable in filteredTables"
        :key="closedTable.id"
        class="card"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-medium text-gray-900">Mesa {{ closedTable.tableNumber }}</h3>
            <p class="text-sm text-gray-600">
              {{ formatDateTime(closedTable.closedAt) }} • {{ closedTable.waiter }}
            </p>
            <p class="text-sm text-blue-600 font-medium">
              Pagamento: {{ getPaymentMethodLabel(closedTable.paymentMethod) }}
            </p>
          </div>
          <div class="text-right">
            <div class="font-semibold text-gray-900">R${{ closedTable.finalTotal.toFixed(2) }}</div>
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
            
            <!-- Service charge in history -->
            <div class="flex justify-between text-sm pt-2 border-t border-gray-100">
              <span class="text-gray-600">Subtotal</span>
              <span class="text-gray-900">R${{ closedTable.total.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Taxa de serviço (10%)</span>
              <span class="text-gray-900">R${{ closedTable.serviceCharge.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-sm font-medium pt-1 border-t border-gray-200">
              <span class="text-gray-900">Total Final</span>
              <span class="text-emerald-600">R${{ closedTable.finalTotal.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 text-gray-500">
      <ClockIcon class="w-12 h-12 mx-auto mb-4 text-gray-300" />
      <p v-if="selectedDate">Nenhuma mesa fechada encontrada para {{ formatSelectedDate }}</p>
      <p v-else>Nenhuma mesa fechada ainda</p>
      <p class="text-sm">{{ selectedDate ? 'Tente selecionar uma data diferente' : 'O histórico da mesa aparecerá aqui após o fechamento da tabela' }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ArrowLeftIcon, ClockIcon } from 'lucide-vue-next'
import { useRestaurantStore } from '~/stores/restaurant'

const emit = defineEmits(['close'])
const restaurantStore = useRestaurantStore()

const selectedDate = ref('')

// Set current date as default on mount
onMounted(() => {
  setToday()
})

const formatDateTime = (date) => {
  const d = new Date(date)
  return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatSelectedDate = computed(() => {
  if (!selectedDate.value) return ''
  return new Date(selectedDate.value + 'T00:00:00').toLocaleDateString('pt-BR')
})

const filteredTables = computed(() => {
  if (!selectedDate.value) {
    return restaurantStore.closedTables
  }
  
  const filterDate = new Date(selectedDate.value + 'T00:00:00')
  const nextDay = new Date(filterDate)
  nextDay.setDate(nextDay.getDate() + 1)
  
  return restaurantStore.closedTables.filter(table => {
    const tableDate = new Date(table.closedAt)
    return tableDate >= filterDate && tableDate < nextDay
  })
})

// Quick filter helpers
const isToday = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return selectedDate.value === today
})

const isYesterday = computed(() => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  return selectedDate.value === yesterday.toISOString().split('T')[0]
})

const isThisWeek = computed(() => {
  return !selectedDate.value
})

const setToday = () => {
  const today = new Date()
  selectedDate.value = today.toISOString().split('T')[0]
}

const setYesterday = () => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  selectedDate.value = yesterday.toISOString().split('T')[0]
}

const setThisWeek = () => {
  // Clear filter to show all tables from this week
  selectedDate.value = ''
}

const clearFilter = () => {
  selectedDate.value = ''
}

const getPaymentMethodLabel = (method) => {
  const methods = {
    'pix': 'PIX',
    'debit': 'Débito',
    'credit': 'Crédito',
    'cash': 'Dinheiro'
  }
  return methods[method] || method
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
    subtotal: closedTable.total,
    serviceCharge: closedTable.serviceCharge,
    finalTotal: closedTable.finalTotal,
    date: closedTable.closedAt,
    waiter: closedTable.waiter,
    paymentMethod: closedTable.paymentMethod,
    type: 'REPRINT'
  })
  
  // Show feedback to user
  alert(`Receipt for Table ${closedTable.tableNumber} sent to printer`)
}
</script>