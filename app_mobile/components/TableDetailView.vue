<template>
  <div class="p-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <button
          @click="goBack"
          class="p-2 -ml-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeftIcon class="w-5 h-5" />
        </button>
        <div>
          <h2 class="text-xl font-bold text-gray-900">Mesa {{ table.number }}</h2>
          <p class="text-sm text-gray-600">
            {{ table.items.length }} iten{{ table.items.length !== 1 ? 's' : '' }} • 
            R${{ table.total.toFixed(2) }}
          </p>
        </div>
      </div>
      
      <div class="flex space-x-2">
        <button
          v-if="table.items.length > 0"
          @click="printPartialReceipt"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          Imprimir Parcial
        </button>
        <button
          v-if="table.items.length > 0"
          @click="showCloseTableModal = true"
          class="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
        >
          Fechar Mesa
        </button>
      </div>
    </div>

    <!-- Add Item Button -->
    <button
      @click="showAddItemModal = true"
      class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2.5 px-6 rounded-lg transition-colors duration-200 active:scale-95 mb-6 flex items-center justify-center"
    >
      <PlusIcon class="w-5 h-5 mr-2" />
      Adicionar item
    </button>

    <!-- Items List -->
    <div v-if="table.items.length > 0" class="space-y-3">
      <div
        v-for="item in table.items"
        :key="item.id"
        class="card"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="font-medium text-gray-900">{{ item.menuItem.name }}</h3>
            <p class="text-sm text-gray-600 mt-1">
              Qtd: {{ item.quantity }} × R${{ item.menuItem.price.toFixed(2) }} = 
              R${{ (item.quantity * item.menuItem.price).toFixed(2) }}
            </p>
            <p v-if="item.observation" class="text-sm text-amber-600 mt-1 italic">
              Obs: {{ item.observation }}
            </p>
            <p class="text-xs text-gray-500 mt-1">
              Adicionado {{ formatTime(item.addedAt) }}
            </p>
          </div>
          <button
            @click="removeItem(item.id)"
            class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <TrashIcon class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 text-gray-500">
      <UtensilsIcon class="w-12 h-12 mx-auto mb-4 text-gray-300" />
      <p>Nenhum item adicionado a esta mesa ainda</p>
      <p class="text-sm">Toque em "Adicionar item" para começar</p>
    </div>

    <!-- Add Item Modal -->
    <AddItemModal
      v-if="showAddItemModal"
      :table="table"
      @close="showAddItemModal = false"
      @add="handleAddItem"
    />

    <!-- Close Table Modal -->
    <CloseTableModal
      v-if="showCloseTableModal"
      :table="table"
      @close="showCloseTableModal = false"
      @confirm="handleCloseTable"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowLeftIcon, PlusIcon, TrashIcon, UtensilsIcon } from 'lucide-vue-next'
import { useRestaurantStore } from '~/stores/restaurant'
import { useAuthStore } from '~/stores/auth'

const restaurantStore = useRestaurantStore()
const authStore = useAuthStore()

const showAddItemModal = ref(false)
const showCloseTableModal = ref(false)

const table = computed(() => restaurantStore.selectedTable)

const goBack = () => {
  restaurantStore.selectedTable = null
}

const removeItem = (itemId) => {
  if (table.value) {
    restaurantStore.removeItemFromTable(table.value.id, itemId)
  }
}

const handleAddItem = (menuItemId, quantity, observation) => {
  if (table.value) {
    restaurantStore.addItemToTable(table.value.id, menuItemId, quantity, observation)
  }
  showAddItemModal.value = false
}

const handleCloseTable = (paymentMethod) => {
  if (table.value && authStore.waiter) {
    restaurantStore.closeTable(table.value.id, authStore.waiter.name, paymentMethod)
    showCloseTableModal.value = false
    goBack()
  }
}

const printPartialReceipt = () => {
  if (table.value) {
    const groupedItems = getGroupedItems(table.value.items)
    const serviceCharge = table.value.total * 0.10
    const finalTotal = table.value.total + serviceCharge
    
    console.log('Printing partial receipt for Table', table.value.number, {
      items: groupedItems,
      subtotal: table.value.total,
      serviceCharge: serviceCharge,
      finalTotal: finalTotal,
      date: new Date(),
      waiter: authStore.waiter?.name,
      type: 'PARTIAL'
    })
    
    // Show feedback to user
    alert(`Recibo parcial da Mesa ${table.value.number} enviado para impressora`)
  }
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

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>