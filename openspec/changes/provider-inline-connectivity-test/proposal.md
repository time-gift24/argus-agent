## Why

当前测试连接功能需要弹出对话框，操作路径长；新增/编辑页面完全没有测试入口，用户必须先创建 Provider 才能测试。需要将测试能力内联到列表卡片和新增表单中，做到「所见即测」。

## What Changes

- 列表页：移除测试弹窗，测试结果直接内联显示在 Provider 卡片上（状态点 + 延迟/错误信息），按钮变为 loading 态
- 新增/编辑页：表单底部添加「测试连接」按钮，使用表单中已填写的 api_key / base_url / model 进行测试（需新增后端端点或复用现有逻辑）

## Capabilities

### New Capabilities
- `inline-provider-test`: 列表卡片内联测试 + 新增表单内测试，无需弹窗

### Modified Capabilities

## Impact

- **前端**: `ProvidersView.vue`（移除弹窗，内联状态）、`ProviderEditView.vue`（新增测试按钮）
- **后端**: 需新增 `POST /api/v1/providers/test-config` 端点，接受未保存的 config 直接测试（新增表单场景下 Provider 尚未创建）
