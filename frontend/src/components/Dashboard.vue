<template>
  <div class="dashboard">
    <div v-if="!data" class="placeholder">
      <p>Ask a question to see analytics.</p>
    </div>
    <div v-else class="content">
      <h2>Analysis Result</h2>
      <div class="chart-container" v-if="data.chart">
        <img :src="'data:image/png;base64,' + data.chart" alt="Chart" />
      </div>
      <div class="table-container" v-if="data.table" v-html="data.table"></div>
      <div class="sql-container" v-if="data.sql">
        <h3>Generated SQL</h3>
        <pre>{{ data.sql }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  data: any
}>();
</script>

<style scoped>
.dashboard {
  padding: 1rem;
  height: 100%;
  overflow-y: auto;
}

.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #888;
}

.chart-container img {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.table-container {
  margin-bottom: 1rem;
  overflow-x: auto;
}

.sql-container {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
