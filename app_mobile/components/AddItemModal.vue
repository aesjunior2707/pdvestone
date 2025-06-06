<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50">
    <div class="bg-white w-full sm:max-w-lg sm:mx-4 rounded-t-2xl sm:rounded-2xl max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-gray-200 p-4 rounded-t-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">
            {{ selectedCategory ? selectedCategory : 'Adicionar novo item' }}
          </h3>
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
        <!-- Category Selection -->
        <div v-if="!selectedCategory">
          <h4 class="text-base font-medium text-gray-700 mb-4">Categoria</h4>
          <div class="grid grid-cols-2 gap-3">
            <button
              v-for="(items, category) in menuCategories"
              :key="category"
              @click="selectedCategory = category"
              class="p-4 bg-gray-100 hover:bg-gray-200 rounded-lg text-center font-medium text-gray-700 transition-colors duration-200 active:scale-95"
            >
              {{ category }}
            </button>
          </div>
        </div>

        <!-- Product Selection -->
        <div v-else>
          <!-- Back to Categories -->
          <div class="flex items-center mb-4">
            <button
              @click="selectedCategory = null"
              class="p-2 -ml-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <span class="text-sm text-gray-600 ml-2">Voltar para categorias</span>
          </div>

          <!-- Product List -->
          <div class="space-y-3">
            <button
              v-for="item in menuCategories[selectedCategory]"
              :key="item.id"
              @click="selectProduct(item)"
              class="w-full flex items-center p-3 border rounded-lg hover:bg-gray-50 transition-colors text-left"
            >
              <div class="flex-1">
                <div class="font-medium text-gray-900">{{ item.name }}</div>
                <div class="text-sm text-gray-600">R${{ item.price.toFixed(2) }}</div>
              </div>
              <ArrowRightIcon class="w-5 h-5 text-gray-400" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Details Modal -->
    <ProductDetailsModal
      v-if="selectedProduct"
      :product="selectedProduct"
      :table="table"
      @close="selectedProduct = null"
      @add="handleAddProduct"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { XIcon, ArrowLeftIcon, ArrowRightIcon } from 'lucide-vue-next'
import { useRestaurantStore } from '~/stores/restaurant'

const props = defineProps(['table'])
const emit = defineEmits(['close', 'add'])

const restaurantStore = useRestaurantStore()

const selectedCategory = ref(null)
const selectedProduct = ref(null)

const menuCategories = computed(() => restaurantStore.getMenuItemsByCategory())

// Reset when category changes
watch(selectedCategory, () => {
  selectedProduct.value = null
})

const selectProduct = (product) => {
  selectedProduct.value = product
}

const handleAddProduct = (productId, quantity, observation) => {
  emit('add', productId, quantity, observation)
  selectedProduct.value = null
}
</script>