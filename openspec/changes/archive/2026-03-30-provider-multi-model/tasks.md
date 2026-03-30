## 1. 数据库迁移

- [x] 1.1 在 `backend/app/models/user.py` 新增 `ProviderModel` ORM 模型（id, provider_id FK CASCADE, name String(128), is_default Boolean, created_at, updated_at, UniqueConstraint(provider_id, name)），并在 Provider 上添加 `models` relationship
- [x] 1.2 创建 Alembic 迁移：建 `provider_models` 表 + 数据迁移（遍历所有 Provider → 解密 config → 提取 model → 插入 ProviderModel → 移除 config 中 model → 重加密写回）

## 2. 后端 Schema

- [x] 2.1 在 `backend/app/schemas/user.py` 移除 `ProviderConfigInput.model` 字段，新增 `ProviderModelCreate`、`ProviderModelRead`、`TestConfigInput` schema

## 3. 后端端点

- [x] 3.1 新增模型 CRUD 端点：`GET/POST/DELETE /providers/{id}/models`、`PUT .../default`
- [x] 3.2 新增 `POST /providers/{id}/models/{model_id}/test` 端点
- [x] 3.3 调整 `POST /providers/test-config`：使用 `TestConfigInput`（model 顶层字段）
- [x] 3.4 调整 `POST /providers/{id}/test`：测试默认模型，无模型时返回提示
- [x] 3.5 `provider_test.py` 重构：`test_provider_connectivity` 接受 `model_name` 参数，`test_config_connectivity` 从顶层取 model

## 4. 后端测试

- [x] 4.1 新增 14 个 ProviderModel CRUD 测试（全部通过）
- [x] 4.2 新增 provider-test-with-no-models 测试；conftest.py 增加 provider_models 表清理

## 5. 前端 API

- [x] 5.1 新增模型 API 函数：listModels, addModel, deleteModel, setDefaultModel, testModel
- [x] 5.2 ProviderConfigForm 不再包含 model 输入；test-config 传顶层 model

## 6. 前端组件

- [x] 6.1 创建 `ProviderModelList.vue` — 模型列表组件（添加/删除/设默认/逐个测试/内联结果）
- [x] 6.2 改造 `ProviderConfigForm.vue` — 移除 model 输入，只保留 name/api_key/base_url
- [x] 6.3 改造 `ProviderEditView.vue` — 集成 ProviderModelList，新增后跳转编辑页管理模型

## 7. 验证

- [x] 7.1 后端测试 57/58 通过（1 个预存问题：test_auth_deps）
- [x] 7.2 前端构建通过
