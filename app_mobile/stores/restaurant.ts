import { defineStore } from 'pinia'

import HttpRequest from '~/services/request'

import { useAuthStore } from '~/stores/auth'

const http = new HttpRequest()
export interface MenuItem {
  id: string
  name: string
  price: number
  category: string
}

export interface Products {
  id: string
  category_id: string
  company_id: number
  created_at: string
  description: string
  price: number
  updated_at: string
  subcategory_id?: string | null
}


export interface Category {
  id: string
  description: string
}


export interface Order {
  company_id: string
  created_at: string
  id: string
  note: string
  product_description: string
  product_id: string
  quantity: number
  status: string,
  table_id: string
  total_price: number
  unit_price: number
  updated_at: string
  user_id: string
  user_name: string
}

export interface OrderItem {
  id: string
  menuItem: MenuItem
  quantity: number
  observation: string
  addedAt: Date
}




export interface PendingItem {
  id: string
  menuItem: MenuItem
  quantity: number
  observation: string
  addedAt: Date
}

export interface Table {
  id: string
  number: number
  description: string
  status: 'available' | 'occupied'
  items: OrderItem[]
  pendingItems: PendingItem[]
  total: number
  pendingTotal: number
}

export interface InvoiceData {
  documentType: string
  documentNumber: string
  customerName: string
  customerEmail: string
  issuedAt: Date
}

export interface ClosedTable {
  id: string
  tableNumber: number
  items: OrderItem[]
  total: number
  serviceCharge: number
  finalTotal: number
  closedAt: Date
  waiter: string
  paymentMethod: string
  invoice?: InvoiceData
}

export const useRestaurantStore = defineStore('restaurant', {
  state: () => ({
    tables: [] as Table[],
    categories: [] as Category[],
    products: [] as Products[],
    pendingItems: [] as Order[],
    ItemsConfirmed: [] as Order[],
    pendingTotal: 0,
    menuItems: [] as MenuItem[],
    closedTables: [] as ClosedTable[],
    selectedTable: null as Table | null,
  }),

  actions: {

    async initializeTables() {
      try {
        const res = await http.request('GET', `company-tables/${useAuthStore().user?.company_id}`)

        const tablesData = (res.data as { data: Table[] }).data;

        console.log('Tables data:', tablesData)

        this.tables = tablesData.map((table: Table) => ({
          id: table.id,
          number: table.number,
          description: table.description || '',
          status: table.status || 'available',
          items: table.items || [],
          pendingItems: table.pendingItems || [],
          total: table.total || 0,
          pendingTotal: table.pendingTotal || 0
        }))


        return true

      }
      catch (error) {
        console.error('Error initializing tables:', error)
        return false
      }
    },


    initializeMenuItems() {
      if (this.menuItems.length === 0) {
        this.menuItems = [
          // BEBIDAS
          { id: '1', name: 'Coca Cola', price: 3.99, category: 'BEBIDAS' },
          { id: '2', name: 'Suco Natural de Laranja', price: 4.99, category: 'BEBIDAS' },
          { id: '3', name: 'Água com Gás', price: 2.50, category: 'BEBIDAS' },
          { id: '4', name: 'Refrigerante Guaraná', price: 3.99, category: 'BEBIDAS' },

          // CERVEJAS
          { id: '5', name: 'Heineken Long Neck', price: 9.99, category: 'CERVEJAS' },
          { id: '6', name: 'Brahma Chopp', price: 7.50, category: 'CERVEJAS' },
          { id: '7', name: 'Skol Pilsen', price: 6.99, category: 'CERVEJAS' },
          { id: '8', name: 'Stella Artois', price: 10.99, category: 'CERVEJAS' },
          { id: '9', name: 'Budweiser', price: 9.50, category: 'CERVEJAS' },

          // BATIDAS
          { id: '10', name: 'Batida de Coco', price: 12.00, category: 'BATIDAS' },
          { id: '11', name: 'Batida de Maracujá', price: 13.00, category: 'BATIDAS' },
          { id: '12', name: 'Batida de Morango', price: 12.50, category: 'BATIDAS' },
          { id: '13', name: 'Batida de Amendoim', price: 13.50, category: 'BATIDAS' },

          // SALADAS
          { id: '14', name: 'Salada Caesar', price: 12.99, category: 'SALADAS' },
          { id: '15', name: 'Salada Caprese', price: 11.99, category: 'SALADAS' },
          { id: '16', name: 'Salada Tropical', price: 10.99, category: 'SALADAS' },


          // Entradas
          { id: '17', name: 'Bruschetta', price: 12.00, category: 'Entradas' },
          { id: '18', name: 'Ceviche', price: 18.50, category: 'Entradas' },
          { id: '19', name: 'Carpaccio', price: 22.00, category: 'Entradas' },

          // Peixe / Camarão
          { id: '20', name: 'Salmão Grelhado', price: 45.90, category: 'Peixe / Camarão' },
          { id: '21', name: 'Camarão ao Alho e Óleo', price: 52.00, category: 'Peixe / Camarão' },
          { id: '22', name: 'Moqueca de Peixe', price: 48.50, category: 'Peixe / Camarão' },

          // Carne / Massa
          { id: '23', name: 'Filé Mignon com Fettuccine', price: 55.00, category: 'Carne / Massa' },
          { id: '24', name: 'Lasanha à Bolonhesa', price: 38.00, category: 'Carne / Massa' },
          { id: '25', name: 'Bife Ancho com Batatas', price: 58.00, category: 'Carne / Massa' },

          // Infantil
          { id: '26', name: 'Mini Hambúrguer com Fritas', price: 22.00, category: 'Infantil' },
          { id: '27', name: 'Espaguete ao Sugo', price: 18.00, category: 'Infantil' },
          { id: '28', name: 'Nuggets com Purê', price: 20.00, category: 'Infantil' },

          // Sobremesa
          { id: '29', name: 'Petit Gâteau', price: 9.90, category: 'Sobremesa' },
          { id: '30', name: 'Pudim de Leite', price: 7.50, category: 'Sobremesa' },
          { id: '31', name: 'Mousse de Maracujá', price: 6.50, category: 'Sobremesa' },

          // Vinhos
          { id: '32', name: 'Vinho Tinto Cabernet', price: 89.90, category: 'Vinhos' },
          { id: '33', name: 'Vinho Branco Chardonnay', price: 79.00, category: 'Vinhos' },
          { id: '34', name: 'Vinho Rosé', price: 69.50, category: 'Vinhos' },

          // Drinks
          { id: '35', name: 'Caipirinha', price: 18.00, category: 'Drinks' },
          { id: '36', name: 'Mojito', price: 20.00, category: 'Drinks' },
          { id: '37', name: 'Gin Tônica', price: 22.00, category: 'Drinks' },

          // Doses
          { id: '38', name: 'Whisky 12 anos', price: 25.00, category: 'Doses' },
          { id: '39', name: 'Tequila Silver', price: 18.00, category: 'Doses' },
          { id: '40', name: 'Vodka Importada', price: 20.00, category: 'Doses' },
        ]
      }
    },

    async selectTable(tableId: string) {
      this.selectedTable = this.tables.find(t => t.id === tableId) || null
      try {
        const res = await http.request('GET', `company-orders/${useAuthStore().user?.company_id}?table=${tableId}`)

        const responseData = res.data as { data: Order[] };
        this.ItemsConfirmed = responseData.data.map(order => ({
          id: order.id,
          company_id: order.company_id,
          created_at: order.created_at,
          note: order.note,
          product_description: order.product_description,
          product_id: order.product_id,
          quantity: order.quantity,
          status: order.status,
          table_id: order.table_id,
          total_price: order.total_price,
          unit_price: order.unit_price,
          updated_at: order.updated_at,
          user_id: order.user_id,
          user_name: order.user_name
        }))
      }
      catch (error) {
        console.error('Error fetching orders for table:', error)
      }
    },

    async addPendingItemToTable(order: Order) {
      if (order) {
        order.id = `ORD-${Date.now()}-${Math.random()}`

        console.log('Adding pending item to table:', order)
        this.pendingItems.push(order)
        this.updateTablePendingTotal()
      }
    },

    removePendingItemFromTable(pendingItemId: string) {
      this.pendingItems = this.pendingItems.filter(item => item.id !== pendingItemId)
      this.updateTablePendingTotal()
    },

    async sendPendingItems() {
      try {
        const res = await http.request('POST', `company-orders/`, this.pendingItems)
        this.pendingItems = []
        this.pendingTotal = 0

        return true
      }
      catch (error) {
        console.error('Error sending pending items:', error)
        throw error
      }

    },

    clearPendingItems() {
      this.pendingItems = []
      this.pendingTotal = 0
    },

    async addItemToTable(order: Order) {
      this.addPendingItemToTable(order)
    },

    async removeItemFromTable(orderItemId: string) {
      try {
          http.request('DELETE', `company-orders/${useAuthStore().user?.company_id}/${orderItemId}`).then(() => {
            this.selectTable(this.selectedTable?.id || '')
          })
      }
      catch (error) {
        console.error('Error removing item from table:', error)
      }


      //this.updateTableTotal(tableId)

    },

    updateTableTotal(tableId: string) {
      const table = this.tables.find(t => t.id === tableId)
      if (table) {
        table.total = table.items.reduce((sum, item) =>
          sum + (item.menuItem.price * item.quantity), 0
        )
      }
    },

    updateTablePendingTotal() {
      this.pendingTotal = this.pendingItems.reduce((sum, item) =>
        sum + (item.unit_price * item.quantity), 0
      );
    },

    closeTable(tableId: string, waiterName: string, paymentMethod: string, invoiceData: InvoiceData | null = null) {
      const table = this.tables.find(t => t.id === tableId)
      if (table && table.items.length > 0) {
        const serviceCharge = table.total * 0.10
        const finalTotal = table.total + serviceCharge

        const closedTable: ClosedTable = {
          id: `closed-${Date.now()}`,
          tableNumber: table.number,
          items: [...table.items],
          total: table.total,
          serviceCharge: serviceCharge,
          finalTotal: finalTotal,
          closedAt: new Date(),
          waiter: waiterName,
          paymentMethod: paymentMethod,
          invoice: invoiceData || undefined
        }

        this.closedTables.unshift(closedTable)

        // Reset table
        table.items = []
        this.pendingItems = []
        table.total = 0
        this.pendingTotal = 0
        table.status = 'available'

        if (this.selectedTable?.id === tableId) {
          this.selectedTable = table
        }
      }
    },
    async getCategorysCompany() {
      try {
        const res = await http.request('GET', `company-category/${useAuthStore().user?.company_id}`)

        const categoriesData = (res.data as { data: { id: string, description: string }[] }).data;

        this.categories = categoriesData.map(category => ({
          id: category.id,
          description: category.description
        }));
      }
      catch (error) {
        console.error('Error getting categories:', error)
        return []
      }
    },

    async getProductsCategory(categoryId: string) {
      try {
        const res = await http.request('GET', `company-products/${useAuthStore().user?.company_id}/${categoryId}`)

        const productsData = (res.data as { data: Products[] }).data;

        this.products = productsData.map(product => ({
          id: product.id,
          category_id: product.category_id,
          company_id: product.company_id,
          created_at: product.created_at,
          description: product.description,
          price: product.price,
          updated_at: product.updated_at,
          subcategory_id: product.subcategory_id || null
        }));

        console.log('Products by category:', this.products)
        return this.products
      }
      catch (error) {
        console.error('Error getting products by category:', error)
      }
    },

    getTotalTable(): number {
      if (this.ItemsConfirmed.length === 0) {
        return 0;
      }

      return this.ItemsConfirmed.reduce((total, item) => {
        return total + (item.unit_price * item.quantity);
      }, 0);
    }
  }

})