## 1. 依赖与 Schema

- [x] 1.1 在 `backend/pyproject.toml` 添加 `langchain-openai` 依赖
- [x] 1.2 在 `backend/app/schemas/user.py` 添加 `ProviderTestResult` schema

## 2. 服务层

- [x] 2.1 创建 `backend/app/services/provider_test.py` — 解密 config → 实例化 ChatOpenAI → 发送测试消息 → 返回 ProviderTestResult

## 3. 端点

- [x] 3.1 在 `backend/app/api/endpoints/providers.py` 添加 `POST /providers/{provider_id}/test` 端点

## 4. 验证

- [x] 4.1 安装依赖并确认后端启动无报错

## 5. 前端

- [x] 5.1 修复 `ProvidersView.vue` 的 `handleTest` 函数，正确处理后端返回的 `{ success, latency_ms, message }` 响应
- [x] 5.2 更新测试结果弹窗 UI：成功显示绿色状态点 + 延迟，失败显示红色状态点 + 错误信息
