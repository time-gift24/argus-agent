# header-layout-cleanup Specification

## Purpose
统一全局 header 与侧栏 footer 的信息层级，移除干扰元素并保留更清晰的主操作区域。
## Requirements
### Requirement: Header 搜索框左对齐
GlobalHeader SHALL 将搜索框放置在 Header 左侧区域（系统健康度 pill 之前），而非右侧。

#### Scenario: 搜索框位置
- **WHEN** 页面加载完成
- **THEN** 搜索框出现在 GlobalHeader 的左侧
- **THEN** 系统健康度 pill 紧随搜索框之后

### Requirement: 删除通知铃铛
GlobalHeader SHALL 不显示通知铃铛按钮。

#### Scenario: 通知铃铛不存在
- **WHEN** 页面加载完成
- **THEN** GlobalHeader 中不存在通知铃铛相关的 SVG 图标和按钮元素
- **THEN** 不存在通知红点指示器

### Requirement: 删除帮助中心
侧边栏 footer SHALL 不包含"帮助中心"条目。

#### Scenario: 帮助中心不存在
- **WHEN** 侧边栏展开
- **THEN** footer 区域为空（无任何条目）

### Requirement: Login 按钮右侧突出显示
GlobalHeader 右侧 SHALL 仅包含 Login 按钮（未登录态）或用户头像+Logout（已登录态），无其他干扰元素。

#### Scenario: 未登录态
- **WHEN** 用户未登录
- **THEN** GlobalHeader 右侧仅显示 Login 按钮，无分隔线或其他按钮

#### Scenario: 已登录态
- **WHEN** 用户已登录
- **THEN** GlobalHeader 右侧显示用户名、头像和 Logout 下拉，无其他干扰元素
