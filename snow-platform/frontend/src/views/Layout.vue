<template>
  <div class="layout-container">
    <aside class="sidebar">
      <div class="logo">AI测试用例平台</div>
      <nav class="nav-menu">
        <router-link to="/" class="nav-item" active-class="active">
          <el-icon><Folder /></el-icon>
          <span>项目管理</span>
        </router-link>
        <router-link to="/settings" class="nav-item" active-class="active">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </router-link>
      </nav>
    </aside>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { Folder, Setting } from '@element-plus/icons-vue'
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  background-color: #f5f7fa;
}

.sidebar {
  width: 200px;
  background-color: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.logo {
  padding: 20px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #ecf0f1;
}

.nav-menu {
  padding: 10px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: #bdc3c7;
  text-decoration: none;
  transition: all 0.3s;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-item.active {
  background-color: rgba(52, 152, 219, 0.3);
  color: #3498db;
  border-right: 3px solid #3498db;
}

.nav-item .el-icon {
  font-size: 18px;
}

.main-content {
  flex: 1;
  overflow-y: auto;
}
</style>
