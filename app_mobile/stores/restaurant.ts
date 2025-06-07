import { defineStore } from 'pinia'

export interface MenuItem {
  id: string
  name: string
  price: number
  category: string
}

export interface OrderItem {
  id: string
  menuItem: MenuItem
  quantity: number
  observation: string
  addedAt: Date
}

export interface Table {
  id: string
  number: number
  status: 'available' | 'occupied'
  items: OrderItem[]
  total: number
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
}

export const useRestaurantStore = defineStore('restaurant', {
  state: () => ({
    tables: [] as Table[],
    menuItems: [] as MenuItem[],
    closedTables: [] as ClosedTable[],
    selectedTable: null as Table | null,
  }),

  actions: {
    initializeTables() {
      if (this.tables.length === 0) {
        this.tables = Array.from({ length: 12 }, (_, i) => ({
          id: `Mesa-${i + 1}`,
          number: i + 1,
          status: 'available' as const,
          items: [],
          total: 0
        }))
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

    selectTable(tableId: string) {
      this.selectedTable = this.tables.find(t => t.id === tableId) || null
    },

    addItemToTable(tableId: string, menuItemId: string, quantity: number, observation: string) {
      const table = this.tables.find(t => t.id === tableId)
      const menuItem = this.menuItems.find(m => m.id === menuItemId)

      if (table && menuItem) {
        const orderItem: OrderItem = {
          id: `Ped-${Date.now()}-${Math.random()}`,
          menuItem,
          quantity,
          observation,
          addedAt: new Date()
        }

        table.items.push(orderItem)
        table.status = 'occupied'
        this.updateTableTotal(tableId)
      }
    },

    removeItemFromTable(tableId: string, orderItemId: string) {
      const table = this.tables.find(t => t.id === tableId)
      if (table) {
        table.items = table.items.filter(item => item.id !== orderItemId)
        if (table.items.length === 0) {
          table.status = 'available'
        }
        this.updateTableTotal(tableId)
      }
    },

    updateTableTotal(tableId: string) {
      const table = this.tables.find(t => t.id === tableId)
      if (table) {
        table.total = table.items.reduce((sum, item) =>
          sum + (item.menuItem.price * item.quantity), 0
        )
      }
    },

    closeTable(tableId: string, waiterName: string) {
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
          waiter: waiterName
        }

        this.closedTables.unshift(closedTable)

        // Reset table
        table.items = []
        table.total = 0
        table.status = 'available'

        if (this.selectedTable?.id === tableId) {
          this.selectedTable = table
        }
      }
    },

    getMenuItemsByCategory() {
      const categories: Record<string, MenuItem[]> = {}
      this.menuItems.forEach(item => {
        if (!categories[item.category]) {
          categories[item.category] = []
        }
        categories[item.category].push(item)
      })
      return categories
    }
  }
})