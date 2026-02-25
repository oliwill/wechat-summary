# Git 使用指南

## 📦 初始化仓库

```bash
git init
git branch -m main
git add .
git commit -m "Initial commit"
```

## 📝 常用命令

### 查看状态

```bash
git status
```

### 查看提交历史

```bash
git log --oneline --graph --all
```

### 查看当前分支

```bash
git branch
```

### 切换分支

```bash
git checkout <branch-name>
```

### 添加文件

```bash
git add <file>
git add .  # 添加所有文件
```

### 提交更改

```bash
git commit -m "提交信息"
```

### 推送到远程仓库

```bash
git push origin main
```

## 🔧 开发工作流

### 1. 创建新功能

```bash
# 创建新分支
git checkout -b feature/new-feature

# 进行开发
# ...

# 提交
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin feature/new-feature
```

### 2. 修复 Bug

```bash
# 创建修复分支
git checkout -b fix/bug-fix

# 进行修复
# ...

# 提交
git commit -m "fix: 修复 bug"

# 推送到远程
git push origin fix/bug-fix
```

### 3. 更新主分支

```bash
# 切换到主分支
git checkout main

# 拉取最新代码
git pull origin main

# 合并功能分支
git merge feature/new-feature

# 推送到远程
git push origin main
```

### 4. 撤销更改

```bash
# 撤销工作区更改
git checkout -- <file>

# 撤销暂存区更改
git reset HEAD <file>

# 撤销提交（保留更改）
git reset --soft HEAD~1

# 撤销提交并丢弃更改
git reset --hard HEAD~1
```

## 📤 推送到 GitHub

### 1. 创建 GitHub 仓库

在 GitHub 上创建新仓库（不要初始化 README、.gitignore 等）

### 2. 关联远程仓库

```bash
git remote add origin https://github.com/你的用户名/wechat-summary.git
```

### 3. 推送代码

```bash
git push -u origin main
```

### 4. 首次推送

如果仓库是空的，添加 `-u` 参数：

```bash
git push -u origin main --force
```

## 🔒 .gitignore 说明

已配置的忽略规则：

- **环境变量文件**：`.env*` - 敏感信息
- **密钥文件**：`*.key` - API 密钥
- **日志文件**：`*.log` - 日志文件
- **Python**：`__pycache__/`, `*.py[cod]`, `venv/`
- **Node.js**：`node_modules/`

## 🤝 代码审查流程

### 1. Pull Request

在 GitHub 上创建 PR，描述更改内容

### 2. 自动检查

GitHub Actions 会自动运行：
- 代码格式检查
- 单元测试
- 覆盖率报告

### 3. 代码审查

等待其他开发者审查 PR

### 4. 合并

审查通过后合并到主分支

## 📊 查看贡献统计

### 查看提交统计

```bash
git log --author="你的名字" --oneline
```

### 查看文件统计

```bash
git log --stat --author="你的名字" HEAD~10
```

### 查看代码行数

```bash
git log --pretty=tformat: --numstat | awk '{add += $1; subs += $2} END {printf "added lines: %s, removed lines: %s\n", add, subs}'
```

## 🔄 分支管理策略

### 功能分支开发

```
main (生产环境)
  ├── feature/new-feature (新功能)
  ├── fix/bug-fix (Bug 修复)
  └── refactor/code-refactor (代码重构)
```

### Git Flow

1. `main` - 稳定版本
2. `develop` - 开发版本
3. `feature/*` - 功能分支
4. `release/*` - 发布分支
5. `hotfix/*` - 紧急修复

## 🔐 保护主分支

在 GitHub 上配置：
- 需要代码审查才能合并
- 需要通过所有 CI 检查
- 需要最多 1 个 approve

## 📚 推荐工具

- **GitHub Desktop** - 图形化 Git 客户端
- **VS Code GitLens** - Git 可视化扩展
- **GitKraken** - Git 可视化工具

## 🆘 常见问题

### 1. 忘记密码

使用 SSH 替代 HTTPS：

```bash
# 生成 SSH 密钥
ssh-keygen -t rsa -b 4096

# 添加公钥到 GitHub
# 复制 ~/.ssh/id_rsa.pub 内容

# 使用 SSH 推送
git remote set-url origin git@github.com:你的用户名/wechat-summary.git
```

### 2. 拉取失败

```bash
# 强制更新本地仓库
git fetch --all
git reset --hard origin/main
```

### 3. 合并冲突

```bash
# 查看冲突文件
git status

# 编辑冲突文件，解决冲突
# ...

# 标记为已解决
git add <resolved-file>

# 提交
git commit
```

## 📖 学习资源

- [Git 官方文档](https://git-scm.com/doc)
- [Pro Git 书籍](https://git-scm.com/book/zh/v2)
- [GitHub 学习实验室](https://skills.github.com/)

---

**最后更新**：2025-08-21
