<template>
  <div class="app-container">
    <div class="sidebar">
      <ChatInterface @result="handleResult" />
    </div>
    <div class="main">
      <Dashboard :data="currentResult" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ChatInterface from './components/ChatInterface.vue';
import Dashboard from './components/Dashboard.vue';

const currentResult = ref(null);

const handleResult = (result: any) => {
  currentResult.value = result;
};
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Inter', sans-serif;
}

#app {
  height: 100%;
}

.app-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 350px;
  background-color: #fff;
}

.main {
  flex: 1;
  background-color: #f9f9f9;
  overflow: hidden;
}
</style>
