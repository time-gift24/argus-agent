<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <header class="welcome-header">
        <h1 class="title">Welcome to Argus</h1>
        <p class="subtitle">智能体协作平台 · AI Agent Collaboration Platform</p>
      </header>

      <div class="features">
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>智能体编排</h3>
          <p>多智能体协同工作，自动化复杂业务流程</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔗</div>
          <h3>灵活集成</h3>
          <p>支持多种大语言模型，无缝对接现有系统</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>可视化监控</h3>
          <p>实时追踪任务执行状态，数据驱动决策</p>
        </div>
      </div>

      <footer class="welcome-footer">
        <tiny-button type="primary" size="large" @click="handleStart">
          开始使用
        </tiny-button>
        <tiny-button size="large" @click="handleDocs">
          查看文档
        </tiny-button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { TinyButton } from '@opentiny/vue'

const handleStart = () => {
  console.log('Starting...')
}

const handleDocs = () => {
  console.log('Opening docs...')
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.welcome-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.welcome-content {
  max-width: 900px;
  width: 100%;
  text-align: center;
}

.welcome-header {
  margin-bottom: 3rem;
}

.title {
  font-size: 3.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  color: #333;
  margin-bottom: 0.75rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.welcome-footer {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.welcome-footer :deep(.tiny-button) {
  min-width: 140px;
}
</style>
