## 1. Backend — test-config 端点

- [x] 1.1 在 `backend/app/services/provider_test.py` 新增 `test_config_connectivity(config: dict)` 函数，接受原始 config dict（无需 Provider ORM 对象）
- [x] 1.2 在 `backend/app/api/endpoints/providers.py` 新增 `POST /providers/test-config` 端点，接受 `ProviderConfigInput` body，调用 `test_config_connectivity`

## 2. Frontend — 列表页内联测试

- [x] 2.1 重构 `ProvidersView.vue`：移除 `showTestDialog` 和 `TinyDialogBox` 测试弹窗
- [x] 2.2 改用 `testResults` reactive Map（以 provider.id 为 key）存储每卡独立测试结果
- [x] 2.3 卡片内测试按钮点击后变为 loading 态，完成后在卡片 actions 上方内联展示状态（绿点+延迟 / 红点+错误）

## 3. Frontend — 新增/编辑页测试

- [x] 3.1 在 `ProviderEditView.vue` 表单 actions 区域添加「测试连接」按钮
- [x] 3.2 点击时校验 api_key 非空，调用 `POST /providers/test-config`，结果展示在按钮下方
