<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50">
    <div class="bg-white w-full sm:max-w-lg sm:mx-4 rounded-t-2xl sm:rounded-2xl max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-gray-200 p-4 rounded-t-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Fechar Mesa {{ itemsTable.table_id }}</h3>
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
          
          <!-- Subtotal -->
          <div class="flex justify-between items-center pt-3 mt-3 border-t border-gray-200">
            <span class="text-base font-medium text-gray-700">Subtotal</span>
            <span class="text-base font-medium text-gray-700">R${{ total_price.toFixed(2) }}</span>
          </div>
          
          <!-- Service Charge -->
          <div class="flex justify-between items-center pt-2">
            <span class="text-base font-medium text-gray-700">Taxa de serviço (10%)</span>
            <span class="text-base font-medium text-gray-700">R${{ serviceCharge.toFixed(2) }}</span>
          </div>
          
          <!-- Final Total -->
          <div class="flex justify-between items-center pt-3 mt-3 border-t-2 border-gray-300">
            <span class="text-lg font-bold text-gray-900">Total Final</span>
            <span class="text-lg font-bold text-emerald-600">R${{ finalTotal.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Payment Method Selection -->
        <div class="mb-6">
          <h4 class="font-medium text-gray-900 mb-3">Forma de pagamento</h4>
          <div class="grid grid-cols-2 gap-3">
            <button
              v-for="method in paymentMethods"
              :key="method.value"
              @click="selectedPaymentMethod = method.value"
              class="p-3 border-2 rounded-lg text-center font-medium transition-all duration-200"
              :class="selectedPaymentMethod === method.value 
                ? 'border-emerald-500 bg-emerald-50 text-emerald-700' 
                : 'border-gray-200 text-gray-700 hover:border-gray-300'"
            >
              <div class="text-lg mb-1">{{ method.icon }}</div>
              <div class="text-sm">{{ method.label }}</div>
            </button>
          </div>
        </div>

        <!-- Print and Invoice Options -->
        <div class="mb-6 space-y-3">
          <label class="flex items-center space-x-3">
            <input
              v-model="printReceipt"
              type="checkbox"
              class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"
            />
            <span class="text-sm text-gray-700">Imprimir recibo do cliente</span>
          </label>
          
          <label class="flex items-center space-x-3">
            <input
              v-model="issueInvoice"
              type="checkbox"
              class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"
            />
            <span class="text-sm text-gray-700">Emitir nota fiscal</span>
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
            :disabled="!selectedPaymentMethod"
            class="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
           Fechar Mesa
          </button>
        </div>
      </div>
    </div>

    <!-- Invoice Modal -->
    <InvoiceModal
      v-if="showInvoiceModal"
      :table="table"
      @close="showInvoiceModal = false"
      @confirm="handleInvoiceConfirm"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { XIcon } from 'lucide-vue-next'

import { useAuthStore } from '../stores/auth'
import { useRestaurantStore } from '../stores/restaurant'

const props = defineProps(['itemsTable'])
const emit = defineEmits(['close', 'confirm'])

const printReceipt = ref(true)
const issueInvoice = ref(false)
const selectedPaymentMethod = ref('')
const showInvoiceModal = ref(false)

const paymentMethods = [
  { value: 'pix', label: 'PIX', icon: '📱' },
  { value: 'debit', label: 'Débito', icon: '💳' },
  { value: 'credit', label: 'Crédito', icon: '💳' },
  { value: 'cash', label: 'Dinheiro', icon: '💵' }
]

const total_price = computed(() => {
  return props.itemsTable.reduce((total, item) => {
    return total + (item.quantity * item.unit_price)
  }, 0)
})

const groupedItems = computed(() => {
  const groups = new Map()
  
  props.itemsTable.forEach(item => {
    const key = item.product_description
    if (groups.has(key)) {
      const existing = groups.get(key)
      existing.totalQuantity += item.quantity
      existing.totalPrice += item.quantity * item.unit_price
    } else {
      groups.set(key, {
        name: item.product_description,
        price: item.unit_price,
        totalQuantity: item.quantity,
        totalPrice: item.quantity * item.unit_price
      })
    }
  })
  
  return Array.from(groups.values())
})

const serviceCharge = computed(() => {
  return total_price.value * 0.10
})

const finalTotal = computed(() => {
  return total_price.value + serviceCharge.value
})

const handleClose = () => {
  if (!selectedPaymentMethod.value) return
  
  // If invoice is requested, show invoice modal first
  if (issueInvoice.value) {
    showInvoiceModal.value = true
    return
  }
  
  // Otherwise proceed with normal closure
  proceedWithClosure()
}

const handleInvoiceConfirm = (invoiceData) => {
  showInvoiceModal.value = false

  proceedWithClosure()
}

const proceedWithClosure = () => {
  
  const json_sales_record = {
      id : 'SLR-' + Math.random().toString(36).substr(2, 9),
      company_id : useAuthStore().user.company_id,
      table_id : useRestaurantStore().selectedTable.id,
      payment_type: selectedPaymentMethod.value,
      total_amount: finalTotal.value,
  }

  useRestaurantStore().create_sales_record(json_sales_record)
    .then(() => {
      emit('close')
      emit('confirm',json_sales_record)
    })
    .catch(error => {
      console.error('Error closing table:', error)
      alert('Erro ao fechar mesa. Tente novamente.')
    })
 
}
</script>