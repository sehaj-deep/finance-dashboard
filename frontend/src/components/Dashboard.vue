<template>
  <div class="dashboard">
    <div class="stats-grid">
      <div class="stat-card card">
        <div class="stat-icon">💵</div>
        <div class="stat-content">
          <h3>Total Spent</h3>
          <p class="stat-value">${{ totalSpent.toFixed(2) }}</p>
        </div>
      </div>
      
      <div class="stat-card card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>Transactions</h3>
          <p class="stat-value">{{ transactions.length }}</p>
        </div>
      </div>
      
      <div class="stat-card card">
        <div class="stat-icon">🏷️</div>
        <div class="stat-content">
          <h3>Categories</h3>
          <p class="stat-value">{{ uniqueCategories }}</p>
        </div>
      </div>
    </div>

    <div class="charts-section">
      <div class="card">
        <h2>Top 5 Spending Categories</h2>
        <div class="category-bars">
          <div 
            v-for="(cat, index) in topCategories" 
            :key="cat.name"
            class="category-bar"
          >
            <div class="bar-label">
              <span class="category-name">{{ cat.name }}</span>
              <span class="category-amount">${{ cat.amount.toFixed(2) }}</span>
            </div>
            <div class="bar-container">
              <div 
                class="bar-fill" 
                :style="{ width: (cat.amount / maxCategoryAmount * 100) + '%', backgroundColor: getColor(index) }"
              ></div>
            </div>
          </div>
        </div>
        
        <button 
          v-if="categoryStats.length > 5" 
          @click="showAllCategories = !showAllCategories"
          class="btn btn-secondary mt-2"
        >
          {{ showAllCategories ? 'Show Less' : `Show ${categoryStats.length - 5} More Categories` }}
        </button>
        
        <div v-if="showAllCategories" class="category-bars mt-2">
          <div 
            v-for="(cat, index) in remainingCategories" 
            :key="cat.name"
            class="category-bar"
          >
            <div class="bar-label">
              <span class="category-name">{{ cat.name }}</span>
              <span class="category-amount">${{ cat.amount.toFixed(2) }}</span>
            </div>
            <div class="bar-container">
              <div 
                class="bar-fill" 
                :style="{ width: (cat.amount / maxCategoryAmount * 100) + '%', backgroundColor: getColor(index + 5) }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'

export default {
  name: 'Dashboard',
  props: {
    transactions: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const showAllCategories = ref(false)
    
    const totalSpent = computed(() => {
      return props.transactions
        .filter(t => t.amount > 0)
        .reduce((sum, t) => sum + t.amount, 0)
    })
    
    const uniqueCategories = computed(() => {
      return new Set(props.transactions.map(t => t.category)).size
    })
    
    const categoryStats = computed(() => {
      const stats = {}
      props.transactions.forEach(t => {
        if (t.amount > 0) {
          stats[t.category] = (stats[t.category] || 0) + t.amount
        }
      })
      
      return Object.entries(stats)
        .map(([name, amount]) => ({ name, amount }))
        .sort((a, b) => b.amount - a.amount)
    })
    
    const topCategories = computed(() => categoryStats.value.slice(0, 5))
    const remainingCategories = computed(() => categoryStats.value.slice(5))
    
    const maxCategoryAmount = computed(() => {
      return categoryStats.value.length > 0 ? categoryStats.value[0].amount : 1
    })
    
    const colors = [
      '#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
      '#3b82f6', '#14b8a6', '#f97316', '#06b6d4', '#a855f7'
    ]
    
    const getColor = (index) => colors[index % colors.length]
    
    return {
      totalSpent,
      uniqueCategories,
      categoryStats,
      topCategories,
      remainingCategories,
      maxCategoryAmount,
      showAllCategories,
      getColor
    }
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-icon {
  font-size: 3rem;
  opacity: 0.8;
}

.stat-content h3 {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.charts-section {
  margin-top: 1rem;
}

.category-bars {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}

.category-bar {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bar-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.95rem;
}

.category-name {
  font-weight: 600;
  color: var(--text-primary);
}

.category-amount {
  color: var(--text-secondary);
  font-weight: 500;
}

.bar-container {
  height: 12px;
  background: var(--bg-secondary);
  border-radius: 6px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}
</style>
