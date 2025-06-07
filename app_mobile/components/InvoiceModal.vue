<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-[70]">
    <div class="bg-white w-full sm:max-w-lg sm:mx-4 rounded-t-2xl sm:rounded-2xl max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-gray-200 p-4 rounded-t-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Emitir Nota Fiscal</h3>
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
        <!-- Document Type Selection -->
        <div class="mb-6">
          <h4 class="font-medium text-gray-900 mb-3">Tipo de documento</h4>
          <div class="grid grid-cols-2 gap-3">
            <button
              @click="documentType = 'cpf'"
              class="p-3 border-2 rounded-lg text-center font-medium transition-all duration-200"
              :class="documentType === 'cpf' 
                ? 'border-emerald-500 bg-emerald-50 text-emerald-700' 
                : 'border-gray-200 text-gray-700 hover:border-gray-300'"
            >
              <div class="text-lg mb-1">👤</div>
              <div class="text-sm">CPF</div>
              <div class="text-xs text-gray-500">Pessoa Física</div>
            </button>
            <button
              @click="documentType = 'cnpj'"
              class="p-3 border-2 rounded-lg text-center font-medium transition-all duration-200"
              :class="documentType === 'cnpj' 
                ? 'border-emerald-500 bg-emerald-50 text-emerald-700' 
                : 'border-gray-200 text-gray-700 hover:border-gray-300'"
            >
              <div class="text-lg mb-1">🏢</div>
              <div class="text-sm">CNPJ</div>
              <div class="text-xs text-gray-500">Pessoa Jurídica</div>
            </button>
          </div>
        </div>

        <!-- Document Input -->
        <div class="mb-6">
          <label :for="documentType" class="block text-sm font-medium text-gray-700 mb-2">
            {{ documentType === 'cpf' ? 'CPF' : 'CNPJ' }}
          </label>
          <input
            :id="documentType"
            v-model="documentNumber"
            type="text"
            :placeholder="documentType === 'cpf' ? '000.000.000-00' : '00.000.000/0000-00'"
            :maxlength="documentType === 'cpf' ? 14 : 18"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
            @input="formatDocument"
          />
          <p class="text-xs text-gray-500 mt-1">
            {{ documentType === 'cpf' ? 'Digite apenas números ou com formatação' : 'Digite apenas números ou com formatação' }}
          </p>
        </div>

        <!-- Customer Name (Optional) -->
        <div class="mb-6">
          <label for="customer-name" class="block text-sm font-medium text-gray-700 mb-2">
            Nome do cliente (opcional)
          </label>
          <input
            id="customer-name"
            v-model="customerName"
            type="text"
            placeholder="Nome completo ou razão social"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
          />
        </div>

        <!-- Email (Optional) -->
        <div class="mb-6">
          <label for="customer-email" class="block text-sm font-medium text-gray-700 mb-2">
            E-mail (opcional)
          </label>
          <input
            id="customer-email"
            v-model="customerEmail"
            type="email"
            placeholder="email@exemplo.com"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
          />
          <p class="text-xs text-gray-500 mt-1">
            A nota fiscal será enviada para este e-mail
          </p>
        </div>

        <!-- Invoice Summary -->
        <div class="mb-6 p-4 bg-gray-50 rounded-lg">
          <h4 class="font-medium text-gray-900 mb-3">Resumo da nota fiscal</h4>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600">Mesa</span>
              <span class="text-gray-900">{{ table.number }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal</span>
              <span class="text-gray-900">R${{ table.total.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Taxa de serviço (10%)</span>
              <span class="text-gray-900">R${{ serviceCharge.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between font-medium pt-2 border-t border-gray-200">
              <span class="text-gray-900">Total</span>
              <span class="text-emerald-600">R${{ finalTotal.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <!-- Validation Error -->
        <div v-if="validationError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-800">{{ validationError }}</p>
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
            @click="handleIssueInvoice"
            :disabled="!isFormValid"
            class="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Emitir Nota Fiscal
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

const documentType = ref('cpf')
const documentNumber = ref('')
const customerName = ref('')
const customerEmail = ref('')
const validationError = ref('')

const serviceCharge = computed(() => {
  return props.table.total * 0.10
})

const finalTotal = computed(() => {
  return props.table.total + serviceCharge.value
})

const isFormValid = computed(() => {
  return documentNumber.value.length > 0 && !validationError.value
})

const formatDocument = (event) => {
  let value = event.target.value.replace(/\D/g, '')
  
  if (documentType.value === 'cpf') {
    // CPF formatting: 000.000.000-00
    if (value.length <= 11) {
      value = value.replace(/(\d{3})(\d)/, '$1.$2')
      value = value.replace(/(\d{3})(\d)/, '$1.$2')
      value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2')
    }
  } else {
    // CNPJ formatting: 00.000.000/0000-00
    if (value.length <= 14) {
      value = value.replace(/(\d{2})(\d)/, '$1.$2')
      value = value.replace(/(\d{3})(\d)/, '$1.$2')
      value = value.replace(/(\d{3})(\d)/, '$1/$2')
      value = value.replace(/(\d{4})(\d{1,2})$/, '$1-$2')
    }
  }
  
  documentNumber.value = value
  validateDocument()
}

const validateDocument = () => {
  validationError.value = ''
  
  if (!documentNumber.value) {
    return
  }
  
  const numbers = documentNumber.value.replace(/\D/g, '')
  
  if (documentType.value === 'cpf') {
    if (numbers.length !== 11) {
      validationError.value = 'CPF deve conter 11 dígitos'
      return
    }
    
    // Basic CPF validation
    if (!/^\d{11}$/.test(numbers) || /^(\d)\1{10}$/.test(numbers)) {
      validationError.value = 'CPF inválido'
      return
    }
    
    // CPF check digit validation
    let sum = 0
    for (let i = 0; i < 9; i++) {
      sum += parseInt(numbers.charAt(i)) * (10 - i)
    }
    let remainder = (sum * 10) % 11
    if (remainder === 10 || remainder === 11) remainder = 0
    if (remainder !== parseInt(numbers.charAt(9))) {
      validationError.value = 'CPF inválido'
      return
    }
    
    sum = 0
    for (let i = 0; i < 10; i++) {
      sum += parseInt(numbers.charAt(i)) * (11 - i)
    }
    remainder = (sum * 10) % 11
    if (remainder === 10 || remainder === 11) remainder = 0
    if (remainder !== parseInt(numbers.charAt(10))) {
      validationError.value = 'CPF inválido'
      return
    }
  } else {
    if (numbers.length !== 14) {
      validationError.value = 'CNPJ deve conter 14 dígitos'
      return
    }
    
    // Basic CNPJ validation
    if (!/^\d{14}$/.test(numbers) || /^(\d)\1{13}$/.test(numbers)) {
      validationError.value = 'CNPJ inválido'
      return
    }
    
    // CNPJ check digit validation
    const weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    const weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    let sum = 0
    for (let i = 0; i < 12; i++) {
      sum += parseInt(numbers.charAt(i)) * weights1[i]
    }
    let remainder = sum % 11
    const digit1 = remainder < 2 ? 0 : 11 - remainder
    
    if (digit1 !== parseInt(numbers.charAt(12))) {
      validationError.value = 'CNPJ inválido'
      return
    }
    
    sum = 0
    for (let i = 0; i < 13; i++) {
      sum += parseInt(numbers.charAt(i)) * weights2[i]
    }
    remainder = sum % 11
    const digit2 = remainder < 2 ? 0 : 11 - remainder
    
    if (digit2 !== parseInt(numbers.charAt(13))) {
      validationError.value = 'CNPJ inválido'
      return
    }
  }
}

const handleIssueInvoice = () => {
  if (!isFormValid.value) return
  
  const invoiceData = {
    documentType: documentType.value,
    documentNumber: documentNumber.value,
    customerName: customerName.value,
    customerEmail: customerEmail.value,
    table: props.table,
    subtotal: props.table.total,
    serviceCharge: serviceCharge.value,
    finalTotal: finalTotal.value,
    issuedAt: new Date()
  }
  
  // Log invoice data for demonstration
  console.log('Issuing invoice:', invoiceData)
  
  // Show success message
  alert(`Nota fiscal emitida com sucesso!\n${documentType.value.toUpperCase()}: ${documentNumber.value}${customerName.value ? '\nCliente: ' + customerName.value : ''}${customerEmail.value ? '\nE-mail: ' + customerEmail.value : ''}`)
  
  emit('confirm', invoiceData)
}
</script>