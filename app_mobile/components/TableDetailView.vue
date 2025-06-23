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
          <h2 class="text-xl font-bold text-gray-900">
            Mesa {{ table.description }}
          </h2>
          <p class="text-sm text-gray-600">
            {{ ItemsConfirmed.length }} iten{{
              ItemsConfirmed.length !== 1 ? "s" : ""
            }}
            confirmado{{ ItemsConfirmed.length !== 1 ? "s" : "" }} • R${{
              total_table.toFixed(2)
            }}
            <span
              v-if="table.pendingItems.length > 0"
              class="text-amber-600 ml-2"
            >
              (+ {{ table.pendingItems.length }} pendente{{
                table.pendingItems.length !== 1 ? "s" : ""
              }})
            </span>
          </p>
        </div>
      </div>

      <div class="flex space-x-2">
        <button
          v-if="ItemsConfirmed.length > 0"
          @click="printPartialReceipt"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          Imprimir Conta
        </button>
        <button
          v-if="ItemsConfirmed.length > 0"
          @click="showCloseTableModal = true"
          class="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
        >
          Dar Pagamento
        </button>
      </div>
    </div>

    <!-- Add Item Button -->
    <button
      @click="onShowModalCategory"
      class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2.5 px-6 rounded-lg transition-colors duration-200 active:scale-95 mb-6 flex items-center justify-center"
    >
      <PlusIcon class="w-5 h-5 mr-2" />
      Adicionar item
    </button>

    <!-- Pending Items Section -->
    <div v-if="pendingItems.length > 0" class="mb-6">
      <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-medium text-amber-800">
            Itens Pendentes ({{ pendingItems.length }})
          </h3>
          <div class="text-sm text-amber-700">
            Total: R${{ pendingTotal.toFixed(2) }}
          </div>
        </div>

        <div class="space-y-2 mb-4">
          <div
            v-for="item in pendingItems"
            :key="item.id"
            class="flex items-center justify-between bg-white p-3 rounded border border-amber-200"
          >
            <div class="flex-1">
              <h4 class="font-medium text-gray-900">
                {{ item.product_description }}
              </h4>
              <p class="text-sm text-gray-600">
                Qtd: {{ item.quantity }} × R${{ item.unit_price.toFixed(2) }} =
                R${{ (item.quantity * item.unit_price).toFixed(2) }}
              </p>
              <p v-if="item.note" class="text-sm text-amber-600 italic">
                Obs: {{ item.note }}
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
    <div v-if="ItemsConfirmed.length > 0">
      <h3 class="font-medium text-gray-900 mb-3">Itens Confirmados</h3>
      <div class="space-y-3 mb-6">
        <div v-for="item in ItemsConfirmed" :key="item.id" class="card">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="font-medium text-gray-900">
                {{ item.product_description }}
              </h3>
              <p class="text-sm text-gray-600 mt-1">
                Qtd: {{ item.quantity }} × R${{
                  item.unit_price.toFixed(2)
                }}
                = R${{ (item.quantity * item.unit_price).toFixed(2) }}
              </p>
              <p
                v-if="item.note"
                class="text-sm text-emerald-600 mt-1 italic"
              >
                Obs: {{ item.note }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                Enviado {{ formatTime(item.created_at) }}
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
    <div
      v-if="ItemsConfirmed.length === 0 && pendingItems.length === 0"
      class="text-center py-12 text-gray-500"
    >
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
      :itemsTable="ItemsConfirmed"
      @close="showCloseTableModal = false"
      @confirm="handleCloseTable"
    />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import {
  ArrowLeftIcon,
  PlusIcon,
  TrashIcon,
  UtensilsIcon,
} from "lucide-vue-next";
import { useRestaurantStore } from "~/stores/restaurant";
import { useAuthStore } from "~/stores/auth";

const restaurantStore = useRestaurantStore();
const authStore = useAuthStore();

const showAddItemModal = ref(false);


const showCloseTableModal = ref(false);

const table = computed(() => restaurantStore.selectedTable);

const total_table = computed(() => {
  return restaurantStore.getTotalTable(table.value);
});

const ItemsConfirmed = computed(() => {
  return restaurantStore.ItemsConfirmed
});

const pendingItems = computed(() => {
  return restaurantStore.pendingItems;
});

const pendingTotal = computed(() => {
  return restaurantStore.pendingTotal;
});

const goBack = () => {
  restaurantStore.selectedTable = null;
};

const removeItem = (order_id) => {
    restaurantStore.removeItemFromTable(order_id);
};

const removePendingItem = (pendingItemId) => {
  restaurantStore.removePendingItemFromTable(pendingItemId);
};

const sendPendingItems = () => {
  if (restaurantStore.pendingItems.length > 0) {
    restaurantStore.sendPendingItems().then(() => {
      showAddItemModal.value = false;
        restaurantStore.initializeTables().then(() => {
          goBack();
        });
    });
  }
};

const clearPendingItems = () => {
    if (confirm("Cancelar todos os itens pendentes?")) {
      restaurantStore.clearPendingItems();
    }
};

const handleAddItem = async (
  product_id,
  product_description,
  price,
  quantity,
  observation
) => {
  const json_send_order = {
    id: null,
    company_id: authStore.user.company_id,
    table_id: table.value.id,
    user_id: authStore.user.id,
    product_id: product_id,
    product_description: product_description,
    unit_price: price,
    quantity: quantity,
    total_price: Number(price * quantity),
    note: observation,
    user_name: authStore.user.name,
    status: "peding",
  };

  if (table.value) {
    restaurantStore.addItemToTable(json_send_order).then(() => {
      showAddItemModal.value = false;
    });
  }
};

const handleCloseTable = () => {
    if (pendingItems.value.length > 0) {
      alert(
        "Não é possível fechar a mesa com itens pendentes. Envie ou cancele os itens pendentes primeiro."
      );
      return;
    }
    
    showCloseTableModal.value = false;
    goBack();
};

const printPartialReceipt = () => {
  if (table.value) {
    const content = {
      'table_id': table.value.id,
      'company_id': useAuthStore().user.company_id,
    }

    restaurantStore.printPartialReceipt(content).catch((error) => {
      console.error('Erro ao imprimir recibo parcial:', error);
    });
  }
};

const getGroupedItems = (items) => {
  const groups = new Map();

  items.forEach((item) => {
    const key = item.menuItem.name;
    if (groups.has(key)) {
      const existing = groups.get(key);
      existing.totalQuantity += item.quantity;
      existing.totalPrice += item.quantity * item.menuItem.price;
    } else {
      groups.set(key, {
        name: item.menuItem.name,
        price: item.menuItem.price,
        totalQuantity: item.quantity,
        totalPrice: item.quantity * item.menuItem.price,
      });
    }
  });

  return Array.from(groups.values());
};

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
};

const onShowModalCategory = () => {
  restaurantStore.getCategorysCompany().then(() => {
    showAddItemModal.value = true;
  });
};
</script>