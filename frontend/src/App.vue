<template>
  <div id="app">
    <header class="header">
      <h1>💰 Finance Dashboard</h1>
      <p class="text-muted">Track your spending with privacy-first AI categorization</p>
    </header>

    <nav class="nav-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="currentTab = tab.id"
        :class="['tab-btn', { active: currentTab === tab.id }]"
      >
        {{ tab.icon }} {{ tab.name }}
      </button>
    </nav>

    <main class="main-content fade-in">
      <Dashboard v-if="currentTab === 'dashboard'" :transactions="transactions" />
      <Upload v-if="currentTab === 'upload'" @uploaded="fetchTransactions" />
      <Transactions v-if="currentTab === 'transactions'" :transactions="transactions" @refresh="fetchTransactions" />
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Dashboard from './components/Dashboard.vue'
import Upload from './components/Upload.vue'
import Transactions from './components/Transactions.vue'

export default {
  name: 'App',
  components: {
    Dashboard,
    Upload,
    Transactions
  },
  setup() {
    const currentTab = ref('dashboard')
    const transactions = ref([])
    
    const tabs = [
      { id: 'dashboard', name: 'Dashboard', icon: '📊' },
      { id: 'upload', name: 'Upload', icon: '📤' },
      { id: 'transactions', name: 'Transactions', icon: '📝' }
    ]

    const fetchTransactions = async () => {
      try {
        const response = await fetch('/api/transactions')
        transactions.value = await response.json()
      } catch (error) {
        console.error('Failed to fetch transactions:', error)
      }
    }

    onMounted(() => {
      fetchTransactions()
    })

    return {
      currentTab,
      tabs,
      transactions,
      fetchTransactions
    }
  }
}
</script>

<style scoped>
.header {
  text-align: center;
  margin-bottom: 3rem;
  padding-top: 1rem;
}

.nav-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  background: var(--bg-secondary);
  padding: 0.5rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.tab-btn {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 1rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
}

.tab-btn:hover {
  background: var(--bg-card);
  color: var(--text-primary);
}

.tab-btn.active {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  box-shadow: var(--shadow-sm);
}

.main-content {
  min-height: 400px;
}
</style>
