# 基础开发指南

## 设计与检视原则(非常重要)
- YAGNI（You Ain't Gonna Need It，你不会需要它）
- KISS (Keep It Simple and Stupid，尽可能保持简单)
- DRY (Don't Repeat Yourself，禁止重复你自身)

# 后端开发指南

- 遵守 python 的[规则](./rules/python)


# 前端开发指南

## 技术选型

| 类别 | 技术 | 说明 |
|------|------|------|
| 框架 | Vue 3 | 渐进式 JavaScript 框架，Composition API |
| 构建 | Vite | 快速的开发服务器和构建工具 |
| UI 组件库 | TinyVue | OpenTiny 企业级 UI 组件库，支持 Vue 2/3、PC/移动端 |
| 语言 | TypeScript | 可选，详见下方说明 |

### 选型理由

- **TinyVue**: 基于 OpenTiny Design 设计体系，提供 130+ 组件，功能强大且稳定（服务内外部 1500+ 业务 9 年）
- **Vite**: 相比 Webpack 更快的冷启动和 HMR，基于 ESM 开发体验更好
- **Vue 3**: 更好的 TypeScript 支持、更灵活的 Composition API、更小的包体积

### 开发规范

- 使用 `<script setup>` 语法糖
- 组件样式使用 `scoped` 避免污染
- 遵循项目 KISS/YAGNI/DRY 原则
