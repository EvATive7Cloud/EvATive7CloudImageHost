<script setup lang="ts">
import { onMounted, ref } from "vue";

const worldText = ref("");
const loading = ref(true);
const error = ref("");

const apiBase = "";

onMounted(async () => {
  try {
    const response = await fetch(`${apiBase}/api/world`);
    if (!response.ok) throw new Error("Failed to fetch");
    worldText.value = await response.json();
  } catch {
    error.value = "Failed to connect to server";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="container">
    <div class="greeting">
      <span class="hello">Hello</span>
      <span class="separator">,</span>
      <span v-if="!loading && !error" class="world">{{ worldText }}</span>
      <span v-else-if="loading" class="loading">...</span>
      <span v-else class="error">{{ error }}</span>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.greeting {
  font-size: 4rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.hello {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.separator {
  color: #333;
}

.world {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fadeIn 0.5s ease-in-out;
}

.loading {
  color: #999;
  animation: pulse 1s ease-in-out infinite;
}

.error {
  color: #f5576c;
  font-size: 1rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.5;
  }
}

@media (prefers-color-scheme: dark) {
  .separator,
  .exclamation {
    color: #fff;
  }
}
</style>
