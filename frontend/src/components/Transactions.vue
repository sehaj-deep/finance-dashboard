<template>
  <div class="transactions-container">
    <div class="card">
      <div class="header-row">
        <h2>📝 Transaction History</h2>
        <div class="filters">
          <select v-model="filterCategory" class="filter-select">
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
      </div>
      
      <div v-if="filteredTransactions.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p>No transactions found</p>
        <p class="text-muted">Upload a bank statement to get started</p>
      </div>
      
      <div v-else class="transactions-list">
        <div 
          v-for="txn in paginatedTransactions" 
          :key="txn.id"
          class="transaction-item"
        >
          <div class="txn-main">
            <div class="txn-icon">{{ getCategoryIcon(txn.category) }}</div>
            <div class="txn-details">
              <p class="txn-description">{{ txn.description }}</p>
              <p class="txn-date text-muted">{{ txn.date }}</p>
            </div>
          </div>
          <div class="txn-right">
            <p class="txn-amount" :class="{ 'income': txn.amount < 0 }">
              {{ txn.amount < 0 ? '+' : '-' }}${{ Math.abs(txn.amount).toFixed(2) }}
            </p>
            <select 
              v-model="txn.category" 
              @change="updateCategory(txn)"
              class="category-select"
            >
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
        </div>
        
        <div v-if="totalPages > 1" class="pagination">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="btn btn-secondary"
          >
            ← Previous
          </button>
          <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="btn btn-secondary"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Transactions',
  props: {
    transactions: {
      type: Array,
      required: true
    }
  },
  emits: ['refresh'],
  setup(props, { emit }) {
    const filterCategory = ref('')
    const currentPage = ref(1)
    const itemsPerPage = 20
    const categories = ref([])
    
    // Fetch categories from API
    const fetchCategories = async () => {
      try {
        const response = await fetch('/api/categories')
        if (response.ok) {
          categories.value = await response.json()
        }
      } catch (e) {
        console.error("Failed to fetch categories", e)
      }
    }
    
    // Initial fetch
    fetchCategories()
    
    const filteredTransactions = computed(() => {
      if (!filterCategory.value) return props.transactions
      return props.transactions.filter(t => t.category === filterCategory.value)
    })
    
    const totalPages = computed(() => {
      return Math.ceil(filteredTransactions.value.length / itemsPerPage)
    })
    
    const paginatedTransactions = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return filteredTransactions.value.slice(start, end)
    })
    
    const categoryIcons = {
      'Food': '🍔',
      'Transport': '🚗',
      'Utilities': '💡',
      'Rent': '🏠',
      'Entertainment': '🎬',
      'Shopping': '🛍️',
      'Income': '💰',
      'Investment': '📈',
      'Health': '⚕️',
      'Other': '📦'
    }
    
    const getCategoryIcon = (category) => {
      return categoryIcons[category] || '📦'
    }
    
    const updateCategory = async (txn) => {
      try {
        const response = await fetch(`/api/transactions/${txn.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ category: txn.category }),
        })
        
        if (response.ok) {
          console.log(`Updated transaction ${txn.id} to ${txn.category}`)
          // Optional: Show a toast/notification
        } else {
          console.error('Failed to update category')
          // Revert change in UI if failed? 
          // For now, just logging error.
        }
      } catch (e) {
        console.error('Error updating category:', e)
      }
    }
    
    return {
      filterCategory,
      currentPage,
      categories,
      filteredTransactions,
      paginatedTransactions,
      totalPages,
      getCategoryIcon,
      updateCategory
    }
  }
}
</script>

<style scoped>
.transactions-container {
  max-width: 900px;
  margin: 0 auto;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
}

.filter-select, .category-select {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.transactions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.transaction-item:hover {
  background: var(--bg-card);
  transform: translateX(4px);
}

.txn-main {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.txn-icon {
  font-size: 2rem;
}

.txn-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.txn-description {
  font-weight: 600;
  color: var(--text-primary);
}

.txn-date {
  font-size: 0.85rem;
}

.txn-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.txn-amount {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent-danger);
  min-width: 100px;
  text-align: right;
}

.txn-amount.income {
  color: var(--accent-success);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.page-info {
  color: var(--text-secondary);
  font-weight: 600;
}
</style>
