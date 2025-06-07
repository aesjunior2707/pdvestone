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
            {{ table.items.length }} iten{{ table.items.length !== 1 ? 's' : '' }} confirmado{{ table.items.length !== 1 ? 's' : '' }} • 
            R${{ table.total.toFixed(2) }}
            <span v-if="table.pendingItems.length > 0" class="text-amber-600 ml-2">
              (+ {{ table.pendingItems.length }} pendente{{ table.pendingItems.length !== 1 ? 's' : '' }})
            </span>
          </p>
        </div>
      </div>
      
      <div class="flex space-x-2">
        <button
          v-if="table.items.length > 0"
          @click="printPartialReceipt"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          Imprimir Conta
        </button>
        <button
          v-if="table.items.length > 0"
          @click="showCloseTableModal = true"
          class="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
        >
          Receber Mesa
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

    <!-- Pending Items Section -->
    <div v-if="table.pendingItems.length > 0" class="mb-6">
      <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-medium text-amber-800">
            Itens Pendentes ({{ table.pendingItems.length }})
          </h3>
          <div class="text-sm text-amber-700">
            Total: R${{ table.pendingTotal.toFixed(2) }}
          </div>
        </div>
        
        <div class="space-y-2 mb-4">
          <div
            v-for="item in table.pendingItems"
            :key="item.id"
            class="flex items-center justify-between bg-white p-3 rounded border border-amber-200"
          >
            <div class="flex-1">
              <h4 class="font-medium text-gray-900">{{ item.menuItem.name }}</h4>
              <p class="text-sm text-gray-600">
                Qtd: {{ item.quantity }} × R${{ item.menuItem.price.toFixed(2) }} = 
                R${{ (item.quantity * item.menuItem.price).toFixed(2) }}
              </p>
              <p v-if="item.observation" class="text-sm text-amber-600 italic">
                Obs: {{ item.observation }}
              </p>
            </div>
            <button
              @click="removePendingItem(item.id)"
              class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Pending Actions -->
        <div class="flex space-x-3">
          <button
            @click="clearPendingItems"
            class="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-lg transition-colors"
          >
            Cancelar Todos
          </button>
          <button
            @click="sendPendingItems"
            class="flex-1 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-lg transition-colors"
          >
            Enviar
          </button>
        </div>
      </div>
    </div>

    <!-- Confirmed Items List -->
    <div v-if="table.items.length > 0">
      <h3 class="font-medium text-gray-900 mb-3">Itens Confirmados</h3>
      <div class="space-y-3 mb-6">
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
              <p v-if="item.observation" class="text-sm text-emerald-600 mt-1 italic">
                Obs: {{ item.observation }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                Enviado {{ formatTime(item.addedAt) }}
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
    </div>

    <!-- Empty State -->
    <div v-if="table.items.length === 0 && table.pendingItems.length === 0" class="text-center py-12 text-gray-500">
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

const removePendingItem = (pendingItemId) => {
  if (table.value) {
    restaurantStore.removePendingItemFromTable(table.value.id, pendingItemId)
  }
}

const sendPendingItems = () => {
  if (table.value && table.value.pendingItems.length > 0) {
    restaurantStore.sendPendingItems(table.value.id)
  }
}

const clearPendingItems = () => {
  if (table.value && table.value.pendingItems.length > 0) {
    if (confirm('Cancelar todos os itens pendentes?')) {
      restaurantStore.clearPendingItems(table.value.id)
    }
  }
}

const handleAddItem = (menuItemId, quantity, observation) => {
  if (table.value) {
    restaurantStore.addItemToTable(table.value.id, menuItemId, quantity, observation)
  }
  showAddItemModal.value = false
}

const handleCloseTable = (paymentMethod, invoiceData = null) => {
  if (table.value && authStore.waiter) {
    // Check if there are pending items
    if (table.value.pendingItems.length > 0) {
      alert('Não é possível fechar a mesa com itens pendentes. Envie ou cancele os itens pendentes primeiro.')
      return
    }
    
    restaurantStore.closeTable(table.value.id, authStore.waiter.name, paymentMethod, invoiceData)
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