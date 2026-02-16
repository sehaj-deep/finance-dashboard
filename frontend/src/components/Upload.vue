<template>
  <div class="upload-container">
    <div class="card upload-card">
      <h2>📤 Upload Bank Statement</h2>
      <p class="text-muted mb-3">Upload your PDF or CSV bank statement to categorize transactions</p>
      
      <div 
        class="dropzone"
        :class="{ 'dragover': isDragging, 'uploading': isUploading }"
        @drop.prevent="handleDrop"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
      >
        <div v-if="!isUploading" class="dropzone-content">
          <div class="upload-icon">📁</div>
          <p class="upload-text">Drag & drop your statement here</p>
          <p class="text-muted">or</p>
          <label for="file-input" class="btn btn-primary">
            Choose File
          </label>
          <input 
            id="file-input"
            type="file" 
            accept=".pdf,.csv"
            @change="handleFileSelect"
            style="display: none;"
          >
          <p class="text-muted mt-2" style="font-size: 0.85rem;">Supports PDF and CSV files</p>
        </div>
        
        <div v-else class="uploading-content">
          <div class="spinner"></div>
          <p class="upload-text">Processing {{ selectedFile?.name }}...</p>
          <p class="text-muted">Extracting and categorizing transactions</p>
        </div>
      </div>
      
      <div v-if="uploadResult" class="result-card mt-3" :class="uploadResult.success ? 'success' : 'error'">
        <div class="result-icon">{{ uploadResult.success ? '✅' : '❌' }}</div>
        <div class="result-content">
          <h3>{{ uploadResult.success ? 'Upload Successful!' : 'Upload Failed' }}</h3>
          <p v-if="uploadResult.success">
            Processed {{ uploadResult.transactions_processed }} transactions, 
            saved {{ uploadResult.new_saved }} new entries
          </p>
          <p v-else>{{ uploadResult.message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Upload',
  emits: ['uploaded'],
  setup(props, { emit }) {
    const isDragging = ref(false)
    const isUploading = ref(false)
    const selectedFile = ref(null)
    const uploadResult = ref(null)
    
    const uploadFile = async (file) => {
      if (!file) return
      
      selectedFile.value = file
      isUploading.value = true
      uploadResult.value = null
      
      const formData = new FormData()
      formData.append('file', file)
      
      try {
        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        })
        
        const data = await response.json()
        
        if (response.ok) {
          uploadResult.value = {
            success: true,
            ...data
          }
          emit('uploaded')
        } else {
          uploadResult.value = {
            success: false,
            message: data.detail || 'Upload failed'
          }
        }
      } catch (error) {
        uploadResult.value = {
          success: false,
          message: error.message
        }
      } finally {
        isUploading.value = false
        selectedFile.value = null
      }
    }
    
    const handleDrop = (e) => {
      isDragging.value = false
      const file = e.dataTransfer.files[0]
      if (file && (file.type === 'application/pdf' || file.name.endsWith('.csv'))) {
        uploadFile(file)
      }
    }
    
    const handleFileSelect = (e) => {
      const file = e.target.files[0]
      if (file) {
        uploadFile(file)
      }
    }
    
    return {
      isDragging,
      isUploading,
      selectedFile,
      uploadResult,
      handleDrop,
      handleFileSelect
    }
  }
}
</script>

<style scoped>
.upload-container {
  max-width: 700px;
  margin: 0 auto;
}

.upload-card {
  text-align: center;
}

.dropzone {
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-md);
  padding: 3rem 2rem;
  background: var(--bg-secondary);
  transition: var(--transition);
  cursor: pointer;
}

.dropzone.dragover {
  border-color: var(--accent-primary);
  background: rgba(99, 102, 241, 0.1);
  transform: scale(1.02);
}

.dropzone.uploading {
  border-color: var(--accent-secondary);
  background: rgba(139, 92, 246, 0.1);
}

.dropzone-content, .uploading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  font-size: 4rem;
  opacity: 0.6;
}

.upload-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--bg-card);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  border-radius: var(--radius-md);
  text-align: left;
}

.result-card.success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid var(--accent-success);
}

.result-card.error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--accent-danger);
}

.result-icon {
  font-size: 2.5rem;
}

.result-content h3 {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.result-content p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}
</style>
