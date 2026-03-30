# Frontend CLAUDE.md

本目录是 Vue 3 + Vite 前端实现，负责控制台界面、路由编排、状态管理与后端 API 对接。

## 先看这些文件

- `src/main.js`: 应用入口（Vue + Pinia + Router）
- `src/App.vue`: 全局框架布局（侧栏、顶栏、`router-view`）
- `src/router/routes.js`: 路由定义与鉴权元信息
- `src/api/client.js`: Axios 实例、JWT 注入、401 统一处理
- `src/stores/`: Pinia 状态模块
- `src/style.css`: 全局视觉 token（Axiom Azure 主题）

## 技术栈（当前代码）

- Vue 3（Composition API / `<script setup>`）
- Vue Router 4
- Pinia
- Vite 6
- Tailwind CSS v4（`@tailwindcss/vite`）
- OpenTiny（`@opentiny/vue`）

## 运行与构建

```bash
cd frontend
make install
make dev
```

```bash
cd frontend
make build
make preview
```

## 测试约定

- 当前测试为 Node 原生测试（`node:test`），测试文件分布在 `src/**/*.test.js`。
- 新增公共工具函数、路由规则、关键文案约束时，优先补对应测试文件。

可直接运行：

```bash
cd frontend
node --test src/**/*.test.js
```

## 实现约束

- 页面结构优先复用 `PageBodyShell.vue`，保持面包屑与头部一致性。
- API 调用统一走 `src/api/` 封装；不要在视图里直接手写 `axios` 请求。
- 鉴权态（token/profile）统一走 `stores/user.js`，禁止在多个组件重复维护登录状态。
- 新增路由若需要登录保护，必须在 `routes.js` 增加 `meta.requiresAuth` 并补路由测试。

## UI 约束（避免风格漂移）

- 全局 token 以 `src/style.css` 为准，不新增“临时色值体系”。
- 组件优先使用既有卡片/间距/排版模式，避免页面风格割裂。
- 新增按钮、表格、弹窗优先复用 OpenTiny 组件，降低视觉和交互分叉。

## 与后端契约协作

- 接口字段与路径变更前，先核对 `../api/openapi.yaml`。
- 前端改了请求路径/字段，必须与后端变更同批提交，不允许契约漂移。

## 代码风格

- 遵守根目录规则：`../rules/vue/`
- 保持 KISS / YAGNI / DRY：小步改动、少层级、少重复
