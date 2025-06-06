<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50">
    <div class="bg-white w-full sm:max-w-lg sm:mx-4 rounded-t-2xl sm:rounded-2xl max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-gray-200 p-4 rounded-t-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Fechar tabela {{ table.number }}</h3>
          <button
            @click="$emit('close')"
            class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XIcon class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="p-4">
        <!-- Items Summary -->
        <div class="mb-6">
          <h4 class="font-medium text-gray-900 mb-3">Resumo do pedido</h4>
          <div class="space-y-2">
            <div
              v-for="group in groupedItems"
              :key="group.name"
              class="flex justify-between items-center py-2 border-b border-gray-100"
            >
              <div>
                <span class="font-medium">{{ group.name }}</span>
                <span class="text-gray-600 ml-2">×{{ group.totalQuantity }}</span>
              </div>
              <span class="font-medium">R${{ group.totalPrice.toFixed(2) }}</span>
            </div>
          </div>
          
          <div class="flex justify-between items-center pt-3 mt-3 border-t border-gray-200">
            <span class="text-lg font-semibold text-gray-900">Total</span>
            <span class="text-lg font-semibold text-gray-900">R${{ table.total.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Print Options -->
        <div class="mb-6">
          <label class="flex items-center space-x-3">
            <input
              v-model="printReceipt"
              type="checkbox"
              class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"
            />
            <span class="text-sm text-gray-700">Imprimir recibo do cliente</span>
          </label>
        </div>

        <!-- Actions -->
        <div class="flex space-x-3">
          <button
            @click="$emit('close')"
            class="flex-1 btn-secondary"
          >
            Cancelar
          </button>
          <button
            @click="handleClose"
            class="flex-1 btn-primary"
          >
           Fechar Mesa
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { XIcon } from 'lucide-vue-next'

const props = defineProps(['table'])
const emit = defineEmits(['close', 'confirm'])

const printReceipt = ref(true)

const groupedItems = computed(() => {
  const groups = new Map()
  
  props.table.items.forEach(item => {
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
})

const handleClose = () => {
  if (printReceipt.value) {
    // Simulate printing receipt
    console.log('Printing receipt for Table', props.table.number, {
      items: groupedItems.value,
      total: props.table.total
    })
  }
  
  emit('confirm')
}
</script>