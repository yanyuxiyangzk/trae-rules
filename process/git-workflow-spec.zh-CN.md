---
trigger: manual
---

# Git 工作流规范 v1.0
# ============================================
# AI 辅助开发的 Git 工作流标准和要求
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据团队需求启用/禁用规则
# 3. 在 AI 对话中使用 @git-workflow-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 依赖规范：workflow-spec.txt、naming-conventions.txt
# 最后更新：2025-11-10
# ============================================

## [规则 1] 分支命名规范 [ENABLED]
# 统一的分支命名约定

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 主分支：main 或 master
- 开发分支：develop
- 功能分支：feature/功能名称
- 修复分支：bugfix/问题描述 或 fix/问题描述
- 热修复分支：hotfix/紧急修复
- 发布分支：release/版本号
- 使用 kebab-case 命名

示例：
✅ 正确：
  main
  develop
  feature/user-authentication
  feature/add-payment-gateway
  bugfix/fix-login-error
  hotfix/critical-security-patch
  release/v1.2.0

❌ 错误：
  Feature_UserAuth
  bug_fix_login
  HOTFIX_SECURITY
  release_1.2

WHY: 统一命名便于识别分支类型和自动化处理


## [规则 2] 提交消息规范 [ENABLED]
# Conventional Commits 标准

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 格式：<type>(<scope>): <subject>
- type: feat, fix, docs, style, refactor, test, chore
- scope: 可选，影响的模块
- subject: 简短描述（小于50字符）
- body: 可选，详细描述
- footer: 可选，Breaking Changes 或关闭 Issue

后果：
- 不规范的提交消息难以生成变更日志
- 无法自动判断版本号变更类型

示例：
✅ 正确：
  feat(auth): add JWT authentication
  
  Implement JWT token-based authentication for API endpoints.
  - Add login endpoint
  - Add token validation middleware
  - Update user model
  
  Closes #123

  fix(payment): resolve payment gateway timeout issue
  
  refactor(api): simplify error handling logic
  
  docs(readme): update installation instructions
  
  chore(deps): upgrade dependencies to latest versions

❌ 错误：
  Updated code
  fix bugs
  WIP
  minor changes


## [规则 3] 提交频率 [ENABLED]
# 小而频繁的提交

STATUS: ENABLED
说明：
- 每个提交应该是独立的逻辑单元
- 避免大量不相关的修改在一个提交中
- 提交前确保代码可编译和运行
- 一天至少提交一次工作进度
- 每个提交只解决一个问题

示例：
✅ 正确（拆分提交）：
  Commit 1: feat(user): add user model
  Commit 2: feat(user): add user controller
  Commit 3: test(user): add user service tests

❌ 错误（混杂提交）：
  Commit: Add user feature, fix payment bug, update docs


## [规则 4] Pull Request 规范 [ENABLED]
# PR 创建和审查标准

STATUS: ENABLED
说明：
- PR 标题使用与提交消息相同的格式
- 提供清晰的描述和上下文
- 包含相关 Issue 链接
- 添加适当的标签（feature, bugfix, etc.）
- 通过所有 CI 检查后再请求审查
- 至少一个审查者批准才能合并

PR 模板示例：
```markdown
## 描述
简要描述此 PR 的目的和修改内容

## 类型
- [ ] 新功能 (feature)
- [ ] Bug 修复 (bugfix)
- [ ] 重构 (refactor)
- [ ] 文档 (docs)
- [ ] 其他

## 相关 Issue
Closes #123

## 修改内容
- 添加了用户认证功能
- 更新了 API 文档
- 添加了单元测试

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试完成

## 截图（如适用）
[添加截图]

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已添加必要的测试
- [ ] 文档已更新
- [ ] 无 console.log 或调试代码
- [ ] 通过所有 CI 检查
```


## [规则 5] 分支策略 [ENABLED]
# Git Flow 或 GitHub Flow

STATUS: ENABLED
说明：
选择适合团队的分支策略：

**Git Flow（适合发布周期固定的项目）**：
- main - 生产环境代码
- develop - 开发环境代码
- feature/* - 新功能开发
- release/* - 发布准备
- hotfix/* - 紧急修复

**GitHub Flow（适合持续部署的项目）**：
- main - 始终可部署
- feature/* - 功能分支
- 通过 PR 合并到 main
- 合并后立即部署

工作流程示例（Git Flow）：
```bash
# 开始新功能
git checkout develop
git checkout -b feature/user-profile

# 开发和提交
git add .
git commit -m "feat(profile): add user profile page"

# 完成功能
git checkout develop
git merge --no-ff feature/user-profile
git branch -d feature/user-profile

# 准备发布
git checkout -b release/v1.1.0 develop
# 测试、修复 bug
git checkout main
git merge --no-ff release/v1.1.0
git tag -a v1.1.0 -m "Release version 1.1.0"
git checkout develop
git merge --no-ff release/v1.1.0
git branch -d release/v1.1.0
```


## [规则 6] 代码审查要求 [ENABLED]
# 强制代码审查流程

STATUS: ENABLED
说明：
- 所有代码必须经过审查才能合并
- 审查者应该检查：
  - 代码质量和可读性
  - 是否遵循规范和最佳实践
  - 测试覆盖率
  - 安全漏洞
  - 性能问题
- 提供建设性的反馈
- 及时响应审查请求（24小时内）

审查清单：
```markdown
## 代码审查清单
- [ ] 代码逻辑正确且完整
- [ ] 遵循命名约定和代码规范
- [ ] 无明显的性能问题
- [ ] 无安全漏洞（SQL注入、XSS等）
- [ ] 错误处理适当
- [ ] 测试充分且通过
- [ ] 文档和注释清晰
- [ ] 无调试代码或注释掉的代码
- [ ] 变更范围合理，不引入无关修改
```


## [规则 7] 合并策略 [ENABLED]
# 选择合适的合并方式

STATUS: ENABLED
说明：
- **Merge Commit** - 保留完整历史，适合功能分支
- **Squash and Merge** - 压缩提交，适合小型功能
- **Rebase and Merge** - 线性历史，适合保持主分支清晰

选择建议：
- feature → develop: Merge Commit (--no-ff)
- develop → main: Merge Commit (--no-ff)
- hotfix → main: Merge Commit
- 小型 PR: Squash and Merge

示例：
```bash
# Merge Commit（保留分支历史）
git checkout develop
git merge --no-ff feature/user-auth
git push origin develop

# Squash（压缩为单个提交）
git checkout main
git merge --squash feature/small-fix
git commit -m "fix: resolve minor UI issues"
git push origin main

# Rebase（线性历史）
git checkout feature/api-update
git rebase develop
git checkout develop
git merge feature/api-update
```


## [规则 8] 禁止的操作 [ENABLED]
# 避免危险的 Git 操作

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 禁止直接推送到 main/master 分支
- 禁止强制推送到共享分支（git push -f）
- 禁止修改已推送的公共历史
- 禁止提交敏感信息（密钥、密码）
- 禁止提交大文件（>100MB）

后果：
- 强制推送覆盖他人工作导致代码丢失
- 敏感信息泄露导致安全风险

保护措施：
```bash
# 设置分支保护规则（GitHub）
# Settings → Branches → Add rule
- Require pull request reviews before merging
- Require status checks to pass
- Include administrators
- Restrict who can push to matching branches

# Git hooks 示例（pre-commit）
#!/bin/bash
# 检查敏感信息
if grep -r "API_KEY\s*=\s*['\"][^'\"]*['\"]" .; then
  echo "Error: API key detected in code"
  exit 1
fi

# 检查文件大小
find . -type f -size +100M | while read file; do
  echo "Error: Large file detected: $file"
  exit 1
done
```


## [规则 9] 标签管理 [ENABLED]
# 版本标签规范

STATUS: ENABLED
说明：
- 使用语义化版本号：v主版本.次版本.修订版本
- 主要发布创建带注释的标签
- 标签消息包含发布说明
- 标签应该指向稳定的提交

示例：
```bash
# 创建带注释的标签
git tag -a v1.2.0 -m "Release version 1.2.0

New Features:
- User authentication
- Payment gateway integration

Bug Fixes:
- Fixed login timeout issue
- Resolved payment validation error
"

# 推送标签
git push origin v1.2.0

# 推送所有标签
git push origin --tags

# 列出标签
git tag -l

# 查看标签详情
git show v1.2.0
```


## [规则 10] 冲突解决 [ENABLED]
# 合并冲突处理流程

STATUS: ENABLED
说明：
- 定期从主分支同步到功能分支
- 冲突解决后充分测试
- 保留有意义的修改，删除冗余代码
- 冲突解决后请原作者审查

流程：
```bash
# 更新功能分支
git checkout feature/my-feature
git fetch origin
git merge origin/develop

# 解决冲突
# 编辑冲突文件
git add .
git commit -m "merge: resolve conflicts with develop"

# 运行测试
npm test

# 推送更新
git push origin feature/my-feature
```


## [规则 11] .gitignore 管理 [ENABLED]
# 忽略不应提交的文件

STATUS: ENABLED
说明：
- 忽略依赖目录（node_modules, venv）
- 忽略构建输出（dist, build）
- 忽略 IDE 配置（.vscode, .idea）
- 忽略环境变量文件（.env）
- 忽略日志文件（*.log）
- 忽略临时文件

示例（.gitignore）：
```
# 依赖
node_modules/
venv/
__pycache__/

# 构建输出
dist/
build/
*.js.map

# 环境变量
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# 日志
*.log
logs/

# 操作系统
.DS_Store
Thumbs.db

# 测试覆盖率
coverage/
.nyc_output/

# 临时文件
*.tmp
*.bak
```


## [规则 12] Commit Hooks [DISABLED]
# Git Hooks 自动化检查

STATUS: DISABLED
说明：
- pre-commit: 代码格式化、lint 检查
- commit-msg: 提交消息格式验证
- pre-push: 运行测试

示例（使用 husky）：
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS",
      "pre-push": "npm test"
    }
  },
  "lint-staged": {
    "*.{js,ts}": ["eslint --fix", "prettier --write"],
    "*.py": ["black", "flake8"]
  }
}

// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore'
    ]],
    'subject-max-length': [2, 'always', 50]
  }
};
```


# ============================================
# 项目类型配置
# ============================================

团队协作项目：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
- 可选： [规则 12]
- 关键：分支规范、PR流程、代码审查、禁止危险操作

个人项目：
- 启用： [规则 1, 2, 3, 8, 9, 11]
- 可选： [规则 4, 5, 6, 7, 10, 12]
- 关键：分支命名、提交规范、标签管理

开源项目：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
- 可选： [规则 10, 12]
- 关键：PR规范、代码审查、贡献指南


# ============================================
# 与其他规范的集成
# ============================================

DEPENDENCIES:
  git-workflow-spec.txt::RULE 2 -> workflow-spec.txt::RULE 1
    note: 提交消息对齐变更日志管理规范
  git-workflow-spec.txt::RULE 9 -> workflow-spec.txt::RULE 2
    note: 标签管理对齐版本号管理规范


# ============================================
# 摘要 - 启用的规则
# ============================================

✅ [规则 1]  分支命名规范 - kebab-case命名约定
✅ [规则 2]  提交消息规范 - Conventional Commits
✅ [规则 3]  提交频率 - 小而频繁的提交
✅ [规则 4]  PR 规范 - 清晰描述和审查流程
✅ [规则 5]  分支策略 - Git Flow/GitHub Flow
✅ [规则 6]  代码审查 - 强制审查流程
✅ [规则 7]  合并策略 - 选择合适的合并方式
✅ [规则 8]  禁止操作 - 避免危险的Git操作
✅ [规则 9]  标签管理 - 语义化版本标签
✅ [规则 10] 冲突解决 - 合并冲突处理流程
✅ [规则 11] .gitignore - 忽略文件管理


# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-10) - 初始 Git 工作流规范，包含 12 条规则
# ============================================
