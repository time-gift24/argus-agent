## ADDED Requirements

### Requirement: Provider 列表页统一 body 头部
`/providers` 页面 SHALL 在内容区左上角显示面包屑、页面标题、页面说明和主操作区。

#### Scenario: 访问 Provider 列表
- **WHEN** 用户导航到 `/providers`
- **THEN** 页面头部显示当前页面包屑 "LLM 提供商"
- **THEN** "新增提供商" 作为页面级主操作显示在头部区域，而不是通过弹窗触发新增表单
