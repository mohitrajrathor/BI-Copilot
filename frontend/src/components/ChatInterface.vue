<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <div class="content">{{ msg.content }}</div>
      </div>
      <div v-if="loading" class="message assistant">
        <div class="content">Thinking...</div>
      </div>
    </div>
    <div class="input-area">
      <input 
        v-model="query" 
        @keyup.enter="sendMessage" 
        placeholder="Ask a question about your data..." 
        :disabled="loading"
      />
      <button @click="sendMessage" :disabled="loading || !query">Send</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['result']);

const query = ref('');
const messages = ref<{ role: 'user' | 'assistant', content: string }[]>([]);
const loading = ref(false);

const sendMessage = async () => {
  if (!query.value) return;

  const userQuery = query.value;
  messages.value.push({ role: 'user', content: userQuery });
  query.value = '';
  loading.value = true;

  try {
    const response = await axios.post('http://localhost:8000/api/chat', { query: userQuery });
    const result = response.data;
    
    messages.value.push({ role: 'assistant', content: result.answer });
    emit('result', result);
  } catch (error) {
    messages.value.push({ role: 'assistant', content: 'Error processing your request.' });
    console.error(error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid #ddd;
  padding: 1rem;
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.message {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.message.user {
  background-color: #e3f2fd;
  align-self: flex-end;
  text-align: right;
}

.message.assistant {
  background-color: #f5f5f5;
  align-self: flex-start;
}

.input-area {
  display: flex;
  gap: 0.5rem;
}

input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
}
</style>
