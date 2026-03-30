# provider-model-management Specification

## Purpose
TBD - created by archiving change provider-multi-model. Update Purpose after archive.
## Requirements
### Requirement: Provider 支持多模型管理
系统 SHALL 允许每个 Provider 关联多个模型记录（ProviderModel），每个模型包含唯一标识名（name）和默认标记（is_default）。

#### Scenario: 创建 Provider 时同时创建模型
- **WHEN** 用户创建 Provider 并提交包含至少一个模型名称的表单
- **THEN** 系统创建 Provider 及关联的 ProviderModel 记录，第一个模型自动设为默认

#### Scenario: Provider 可以没有模型
- **WHEN** 用户创建 Provider 但不指定任何模型名称
- **THEN** 系统创建 Provider，该 Provider 的模型列表为空

### Requirement: 列出 Provider 下所有模型
系统 SHALL 提供 `GET /providers/{provider_id}/models` 端点，返回该 Provider 下所有模型记录。

#### Scenario: 查询有模型的 Provider
- **WHEN** 用户请求 Provider 的模型列表
- **THEN** 返回该 Provider 下所有 ProviderModel 记录，按创建时间排序

#### Scenario: 查询无模型的 Provider
- **WHEN** 用户请求一个没有任何模型的 Provider 的模型列表
- **THEN** 返回空数组

#### Scenario: 查询不存在的 Provider
- **WHEN** 用户请求不存在的 Provider 的模型列表
- **THEN** 返回 404

### Requirement: 添加模型到 Provider
系统 SHALL 提供 `POST /providers/{provider_id}/models` 端点，允许用户向 Provider 添加新模型。

#### Scenario: 添加第一个模型
- **WHEN** 用户向没有模型的 Provider 添加模型 "gpt-4o"
- **THEN** 系统创建 ProviderModel 记录，自动设为默认

#### Scenario: 添加非首个模型
- **WHEN** 用户向已有默认模型的 Provider 添加模型 "gpt-4o-mini"
- **THEN** 系统创建 ProviderModel 记录，is_default=False

#### Scenario: 添加重复模型名
- **WHEN** 用户向 Provider 添加已存在的模型名 "gpt-4o"
- **THEN** 返回 409 Conflict

#### Scenario: 添加模型到不属于自己的 Provider
- **WHEN** 用户尝试向其他用户的 Provider 添加模型
- **THEN** 返回 404

### Requirement: 删除 Provider 下的模型
系统 SHALL 提供 `DELETE /providers/{provider_id}/models/{model_id}` 端点。

#### Scenario: 删除非默认模型
- **WHEN** 用户删除一个非默认模型
- **THEN** 系统删除该 ProviderModel 记录

#### Scenario: 删除默认模型
- **WHEN** 用户删除默认模型，且 Provider 下还有其他模型
- **THEN** 系统删除该模型，并将最近添加的模型设为新的默认

#### Scenario: 删除唯一的模型
- **WHEN** 用户删除 Provider 下唯一的模型
- **THEN** 系统删除该模型，Provider 变为无模型状态

### Requirement: 设置默认模型
系统 SHALL 提供 `PUT /providers/{provider_id}/models/{model_id}/default` 端点。

#### Scenario: 设置新的默认模型
- **WHEN** 用户将某个模型设为默认
- **THEN** 系统清除该 Provider 下其他模型的默认标记，将目标模型设为默认

### Requirement: 按模型测试连通性
系统 SHALL 提供 `POST /providers/{provider_id}/models/{model_id}/test` 端点，使用 Provider 的 api_key/base_url 结合模型的 name 发起连通性测试。

#### Scenario: 测试存在的模型
- **WHEN** 用户测试 Provider 下某个模型的连通性
- **THEN** 系统使用该 Provider 的 api_key、base_url 和模型的 name 构造 ChatOpenAI 请求，返回测试结果

#### Scenario: 测试不存在的模型
- **WHEN** 用户测试不存在的模型 ID
- **THEN** 返回 404

### Requirement: 表单级模型测试（test-config 调整）
`POST /providers/test-config` 端点的 body SHALL 包含独立的 `model` 字段（不再嵌套在 config 对象内）。

#### Scenario: 带 model 测试
- **WHEN** 用户提交 `{api_key, base_url, model}` 进行测试
- **THEN** 系统使用 api_key、base_url、model 构造请求并返回结果

#### Scenario: 不带 model 测试
- **WHEN** 用户提交 `{api_key, base_url}` 不带 model 进行测试
- **THEN** 系统使用 api_key、base_url（不指定 model）构造请求并返回结果

