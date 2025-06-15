<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50"
  >
    <div
      class="bg-white w-full sm:max-w-lg sm:mx-4 rounded-t-2xl sm:rounded-2xl max-h-[90vh] overflow-y-auto"
    >
      <!-- Header -->
      <div
        class="sticky top-0 bg-white border-b border-gray-200 p-4 rounded-t-2xl"
      >
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">
            {{
              category.selected ? category.description : "Adicionar novo item"
            }}
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
        <div v-if="!category.selected">
          <h4 class="text-base font-medium text-gray-700 mb-4">Categoria</h4>
          <div class="grid grid-cols-2 gap-3">
            <button
              v-for="category in categories"
              :key="category.id"
              @click="onClickSelectCategory(category)"
              class="p-4 bg-gray-100 hover:bg-gray-200 rounded-lg text-center font-medium text-gray-700 transition-colors duration-200 active:scale-95"
            >
              {{ category.description }}
            </button>
          </div>
        </div>

        <!-- Product Selection -->
        <div v-else>
          <!-- Back to Categories -->
          <div class="flex items-center mb-4">
            <button
              @click="onClickBackToCategories"
              class="p-2 -ml-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <span class="text-sm text-gray-600 ml-2"
              >Voltar para categorias</span
            >
          </div>

          <!-- Product List -->
          <div class="space-y-3">
            <div
              v-for="product in products"
              :key="product.id"
              @click="selectProduct(product)"
            >
              <button
                v-if="!product.subcategory_id || show_product_subs_cateogory"
                class="w-full flex items-center p-3 border rounded-lg hover:bg-gray-50 transition-colors text-left"
              >
                <div class="flex-1">
                  <div class="font-medium text-gray-900">
                    {{ product.description }}
                  </div>
                  <div
                    class="text-sm text-gray-600"
                    v-if="!product.subcategory_id_menu"
                  >
                    R${{ product.price.toFixed(2) }}
                  </div>
                </div>
                <ArrowRightIcon class="w-5 h-5 text-gray-400" />
              </button>
            </div>
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
import { ref, computed, watch } from "vue";
import { XIcon, ArrowLeftIcon, ArrowRightIcon } from "lucide-vue-next";
import { useRestaurantStore } from "~/stores/restaurant";

const props = defineProps(["table"]);

const emit = defineEmits(["close", "add"]);

const restaurantStore = useRestaurantStore();

const category = ref({
  selected: false,
  description: "",
  id: null,
});

const selectedProduct = ref(null);

const categories = computed(() => restaurantStore.categories);

const products = computed(() => restaurantStore.products);

const onClickSelectCategory = async (pcategory) => {
  await restaurantStore.getProductsCategory(pcategory.id).then(() => {
    category.value.selected = true;
    category.value.description = pcategory.description;
    category.value.id = pcategory.id;
  });
};

const onClickBackToCategories = () => {
  show_product_subs_cateogory.value = false;
  category.value.selected = false;
  category.value.description = "";
  category.value.id = null;
};

const show_product_subs_cateogory = ref(false);

const selectProduct = async (product) => {
  if (!product.subcategory_id_menu) {
    selectedProduct.value = product;
  } else {
    await restaurantStore
      .getProductsCategory(product.category_id, product.subcategory_id_menu)
      .then(() => {
        show_product_subs_cateogory.value = true;
      });
  }
};

const handleAddProduct = (
  productId,
  product_description,
  quantity,
  observation
) => {
  emit("add", productId, product_description, quantity, observation);
  selectedProduct.value = null;
};
</script>