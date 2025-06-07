<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-[60]">
    <div class="bg-white w-full sm:max-w-lg sm:mx-4 rounded-t-2xl sm:rounded-2xl max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-gray-200 p-4 rounded-t-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Adicionar item</h3>
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
        <!-- Product Info -->
        <div class="mb-6">
          <h4 class="text-xl font-semibold text-gray-900 mb-2">{{ product.name }}</h4>
          <p class="text-lg text-emerald-600 font-medium">R${{ product.price.toFixed(2) }}</p>
        </div>

        <!-- Quantity -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-3">
              Quantidade
          </label>
          <div class="flex items-center justify-center space-x-4">
            <button
              type="button"
              @click="quantity = Math.max(1, quantity - 1)"
              class="w-12 h-12 flex items-center justify-center border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <MinusIcon class="w-5 h-5" />
            </button>
            <span class="text-2xl font-semibold w-16 text-center">{{ quantity }}</span>
            <button
              type="button"
              @click="quantity++"
              class="w-12 h-12 flex items-center justify-center border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <PlusIcon class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Notes -->
        <div class="mb-6">
          <label for="notes" class="block text-sm font-medium text-gray-700 mb-2">
              Observação
          </label>
          <textarea
            id="notes"
            v-model="notes"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
            placeholder="Alguma observação especial"
          ></textarea>
          <p class="text-xs text-gray-500 mt-1">Obs : Isso não aparecerá no recibo</p>
        </div>

        <!-- Total -->
        <div class="mb-6 p-4 bg-gray-50 rounded-lg">
          <div class="flex justify-between items-center">
            <span class="text-lg font-medium text-gray-900">Total</span>
            <span class="text-xl font-bold text-emerald-600">
              R${{ (product.price * quantity).toFixed(2) }}
            </span>
          </div>
        </div>

        <!-- Pending Notice -->
        <div class="mb-6 p-3 bg-amber-50 border border-amber-200 rounded-lg">
          <div class="flex items-start space-x-2">
            <div class="w-5 h-5 text-amber-600 mt-0.5">⏳</div>
            <div class="text-sm text-amber-800">
              <p class="font-medium">Item será adicionado como pendente</p>
              <p class="text-xs mt-1">Você precisará clicar em "Enviar" para confirmar o pedido</p>
            </div>
          </div>
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
            @click="handleSubmit"
            class="flex-1 btn-primary"
          >
          Adicionar à Mesa {{ table.number }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { XIcon, MinusIcon, PlusIcon } from 'lucide-vue-next'

const props = defineProps(['product', 'table'])
const emit = defineEmits(['close', 'add'])

const quantity = ref(1)
const notes = ref('')

const handleSubmit = () => {
  emit('add', props.product.id, quantity.value, notes.value)
}
</script>