---
name: using-git-worktrees
description: 在开始任何需要写代码的实施工作时使用。在项目 .worktrees/ 目录下创建隔离的 git worktree，确保 agent 从不在 main 分支工作。如果发现自己在 main 分支，尝试从 git 历史分析应该在的 worktree；如果确认不了则询问用户。与 openspec 工作流强绑定：文档阶段允许在 main 分支完成，实施阶段必须进入 worktree。
---

# Using Git Worktrees

## 核心原则

**Agent 永远不在 main 分支写代码。** 工作目录必须是 `.worktrees/` 下的一个 worktree。

**两种合法状态：**
- **文档阶段**（OpenSpec propose/explore/archive）：可以在 main 分支操作文件和文档，但**不提交代码**
- **实施阶段**（实现 feature/bugfix/重构）：必须位于 `.worktrees/` 下的 worktree

## 第零步：保持远程同步
git rebase origin/main 或者 git rebase origin/master

## 第一步：检测当前分支

```bash
current_branch=$(git branch --show-current 2>/dev/null)
```

### 如果在 main 分支

**允许的场景：** 仅进行文档操作（创建/编辑 openspec 文档、proposal、review 等），且不涉及代码文件提交。

**不允许的场景：** 任何代码修改、测试运行、安装依赖等实施工作。

#### 尝试从历史分析应该在的 worktree

```bash
# 1. 检查已有的 worktree
git worktree list

# 2. 搜索最近 commit message 中提及的分支名
git log --oneline -20 | grep -i "feature\|fix\|refactor\|impl" | head -5

# 3. 查看 .worktrees/ 下已有的目录
ls -d .worktrees/*/ 2>/dev/null
```

#### 如果能确认

```bash
cd .worktrees/<对应的分支名>
```

#### 如果无法确认

询问用户：

```
我在 main 分支，但看起来需要进行实施工作。

已有的 worktree：
<列出 .worktrees/ 下的目录>

请告诉我：
1. 要继续已有分支的工作？（请指定分支名）
2. 要基于哪个 openspec/change 新建 worktree？（我会从相关文档中推断分支名）
3. 其他指令
```

### 如果在 worktree 中

确认工作目录在 `.worktrees/` 下即可继续工作。

## 第二步：确保 .worktrees/ 存在且被忽略

```bash
if [ ! -d ".worktrees" ]; then
  mkdir .worktrees
fi

if ! git check-ignore -q .worktrees 2>/dev/null; then
  echo ".worktrees 未被忽略，正在修复..."
  echo ".worktrees/" >> .gitignore
  git add .gitignore
  git commit -m "chore: add .worktrees to gitignore"
fi
```

## 第三步：创建新 Worktree

### 从 OpenSpec 变更创建

从变更目录名推断分支名：

```bash
change_slug="<从变更目录推断>"
branch_name="impl/${change_slug}"

git worktree add ".worktrees/${change_slug}" -b "${branch_name}"
cd ".worktrees/${change_slug}"
```

### 从用户指令创建

```bash
branch_name="impl/<feature-slug>"
git worktree add ".worktrees/<feature-slug>" -b "${branch_name}"
cd ".worktrees/<feature-slug>"
```

## 第四步：OpenSpec 文档迁移（实施阶段）

进入实施阶段时，将相关文档移动到 worktree：

```bash
if [ -d "openspec" ]; then
  mkdir -p ".worktrees/<branch-slug>/openspec"
  git mv <原路径> ".worktrees/<branch-slug>/openspec/"
fi
```

**注意：** 使用 `git mv` 而非 `mv`，保持 git 历史关联。

## 第五步：运行项目初始化

```bash
# Python (uv)
if [ -f "backend/pyproject.toml" ]; then
  (cd backend && uv sync)
fi

# Node.js
if [ -f "package.json" ]; then
  npm install
fi
```

## 第六步：验证基线

```bash
# 运行测试
(cd backend && uv run pytest)
```

**如果测试失败：** 报告失败并询问是否继续调查。

## 报告格式

```
Worktree ready: .worktrees/<分支名>/
当前分支: <分支名>
测试状态: <N> tests, <failures> failures
就绪开始实施
```

## Quick Reference

| 场景 | 行动 |
|------|------|
| 在 main，文档工作 | ✅ 允许，不提交代码 |
| 在 main，实施工作 | ❌ 禁止，切换或创建 worktree |
| 在 worktree 中 | ✅ 正常工作 |
| .worktrees 未被忽略 | 修复并提交 .gitignore |
| OpenSpec 文档迁移 | 使用 git mv 移动到 worktree |

## 常见错误

### 在 main 分支实施

- **问题：** 代码与 main 分支耦合，无法独立提交
- **修复：** 立即切换或创建 worktree

### 使用 mv 而非 git mv 移动文档

- **问题：** 丢失 git 历史
- **修复：** 对文档始终使用 `git mv`

### 跳过 .gitignore 验证

- **问题：** worktree 内容被意外提交
- **修复：** 始终先验证 `.worktrees/` 被忽略

## 与 OpenSpec 技能的配合

- **openspec-propose / openspec-explore / openspec-archive**: 文档工作在 main 分支
- **进入实施阶段**: 创建 worktree，将相关 openspec 文档移动到 worktree
- **实施完成后**: 在 worktree 中完成归档
