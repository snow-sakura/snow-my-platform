<script setup>
import ChatWindow from './components/ChatWindow.vue'
</script>

<template>
  <div class="app-container">
    <ChatWindow />
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
}
</style>
