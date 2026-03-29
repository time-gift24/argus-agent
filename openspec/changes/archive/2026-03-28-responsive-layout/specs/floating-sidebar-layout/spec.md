## ADDED Requirements

### Requirement: 侧边栏 fixed overlay
侧边栏 SHALL 使用 CSS fixed 定位悬浮于页面左侧，不占据文档流空间。主内容区 SHALL 使用 padding-left 适配侧边栏宽度。

#### Scenario: 展开状态
- **WHEN** 侧边栏展开（w-64）
- **THEN** 侧边栏固定在左侧，宽度 256px
- **THEN** 主内容区 padding-left 为 256px

#### Scenario: 收缩状态
- **WHEN** 侧边栏收缩（w-20）
- **THEN** 侧边栏固定在左侧，宽度 80px，仅显示图标
- **THEN** 主内容区 padding-left 为 80px

### Requirement: 侧边栏 hover 展开
当侧边栏处于收缩状态时，鼠标 hover 到侧边栏区域 SHALL 临时展开为完整宽度，显示图标+文字。鼠标离开后 SHALL 收回为收缩态。

#### Scenario: hover 展开
- **WHEN** 侧边栏收缩（w-20）且鼠标进入侧边栏区域
- **THEN** 侧边栏平滑展开至 w-64，显示完整导航项文字

#### Scenario: hover 收回
- **WHEN** 侧边栏因 hover 展开且鼠标离开侧边栏区域
- **THEN** 侧边栏平滑收缩回 w-20

### Requirement: 主内容区上下布局
主内容区 SHALL 为上下结构：顶部固定导航栏（TopNav h-16）+ 下方 `<router-view>` 内容区。内容区宽度 100% 减去侧边栏宽度。

#### Scenario: 页面结构
- **WHEN** 页面加载完成
- **THEN** TopNav 固定在顶部（h-16）
- **THEN** 内容区位于 TopNav 下方，宽度自适应

### Requirement: 移动端隐藏侧边栏
在移动端（< md 断点）SHALL 默认隐藏侧边栏，通过 hamburger 按钮触发 overlay 显示。

#### Scenario: 移动端默认隐藏
- **WHEN** 屏幕宽度 < 768px
- **THEN** 侧边栏默认隐藏
- **THEN** 主内容区 padding-left 为 0

#### Scenario: 移动端 overlay 显示
- **WHEN** 用户点击 hamburger 按钮
- **THEN** 侧边栏以 overlay 形式显示（z-50）
- **THEN** 背景显示半透明遮罩
