## 1. 布局结构重构

- [x] 1.1 重构 App.vue template：侧边栏使用 fixed 定位，主内容区改为 flex column 布局
- [x] 1.2 主内容区使用 padding-left 替代 margin-left，随侧边栏状态变化
- [x] 1.3 TopNav 高度 h-16 固定，内容区 pt-16 留出顶部空间

## 2. 侧边栏 hover 展开

- [x] 2.1 收缩状态下鼠标 hover 侧边栏时临时展开为 w-64
- [x] 2.2 鼠标离开后平滑收回 w-20

## 3. 移动端适配

- [x] 3.1 移动端（< md）默认隐藏侧边栏，主内容区 padding-left 为 0
- [x] 3.2 hamburger 按钮触发 overlay 显示侧边栏 + 半透明遮罩

## 4. 验证

- [x] 4.1 确认构建通过
