## Context

后端已有 `POST /providers/{id}/test` 端点，但该端点需要 Provider 已存在于数据库中。新增表单场景下 Provider 尚未创建，需要一个接受原始 config 的测试端点。

## Goals / Non-Goals

**Goals:**
- 列表卡片内联展示测试结果，去掉弹窗
- 新增/编辑表单提供「测试连接」按钮，直接用表单中填写的内容测试
- 后端新增 `POST /providers/test-config` 端点，接受 `{ api_key, base_url, model }` 直接测试

**Non-Goals:**
- 不做批量测试
- 不做自动定时探测
- 不修改现有 `/providers/{id}/test` 端点

## Decisions

### 1. 新增 `POST /providers/test-config` 端点

接受 `ProviderConfigInput` body，直接用传入的 api_key/base_url/model 进行连通性探测，无需 Provider 存在于 DB。

- **理由**: 新增表单场景下无法调用 `/providers/{id}/test`，因为 Provider 尚未创建
- **复用**: 直接调用已有的 `provider_test.py` 中的核心逻辑，将 `test_provider_connectivity` 拆为可接受原始 config 的版本

### 2. 列表页内联状态

每张卡片维护独立的 `testResult` 状态（以 provider.id 为 key），测试按钮点击后变为 loading 图标，完成后直接在卡片 actions 行上方展示状态条（绿点+延迟 / 红点+错误信息）。

- **移除**: `TinyDialogBox` 测试弹窗

### 3. 表单页测试按钮

在提交按钮旁添加「测试连接」按钮，复用 `POST /providers/test-config`。测试结果展示在按钮下方（成功/失败 + 信息）。

## Risks / Trade-offs

- **[test-config 端点可被滥用探测外部服务]** → 需认证（已有 auth deps），且限流可后续添加
- **[列表卡片多卡同时测试]** → 每卡独立状态，互不影响
