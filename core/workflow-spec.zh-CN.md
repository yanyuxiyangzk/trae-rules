---
trigger: manual
---

# 工作流程规范 v1.0
# ============================================
# AI 辅助编码的开发工作流程和流程规则
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据项目需求启用/禁用规则
# 3. 在 AI 对话中使用 @workflow-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 最后更新：2025-11-09
# ============================================

## [规则 1] 变更日志管理 [ENABLED]
# 在变更日志文件中维护更新记录

STATUS: ENABLED
说明：
- 在 CHANGELOG.md 或类似文件中记录所有重要变更
- 包含版本号、日期和变更描述
- 在提交代码变更前更新变更日志
- 遵循 "Keep a Changelog" 格式（Added/Changed/Deprecated/Removed/Fixed/Security）

示例格式：
```
## [1.2.0] - 2025-11-09
### Added
- User authentication with JWT tokens
- Password reset functionality

### Fixed
- Login form validation error
```

原因：提供清晰的项目演进历史，帮助团队追踪何时发生了什么变更

后果：
- 缺失变更日志使发布不可审计、难以追踪
- 团队失去可见性；支持无法定位变更
- 合规与复盘变得容易出错



## [规则 2] 版本号管理 [ENABLED]
# 在项目中一致地更新版本号

STATUS: ENABLED
说明：
- 遵循语义化版本控制（MAJOR.MINOR.PATCH）
- 发布时更新 package.json/version 文件中的版本
- MAJOR：破坏性变更
- MINOR：新功能（向后兼容）
- PATCH：错误修复（向后兼容）
- 更新所有相关文件中的版本（package.json、setup.py、build.gradle 等）

示例：
- 1.0.0 → 1.0.1（错误修复）
- 1.0.1 → 1.1.0（新功能）
- 1.1.0 → 2.0.0（破坏性变更）

原因：确保一致的版本追踪和依赖管理

后果：
- 错误的版本管理会混淆使用方并破坏集成
- 未记录的破坏性变更会导致下游大面积故障



## [规则 3] Git 提交信息格式 [DISABLED]
# 标准化提交信息结构

STATUS: DISABLED
说明：
- 遵循 Conventional Commits 规范
- 格式：<type>(<scope>): <subject>
- 类型：feat、fix、docs、style、refactor、test、chore
- 示例："feat(auth): add JWT token validation"
- 主题行保持在 72 字符以下
- 使用祈使语气（"add" 而不是 "added"）

示例：
✅ 正确：
  feat(login): add password reset functionality
  fix(api): resolve timeout issue in user endpoint

❌ 错误：
  updated login
  fixed bugs

原因：使提交历史可搜索，并支持自动生成变更日志


## [规则 4] 分支命名约定 [DISABLED]
# 一致的分支命名策略

STATUS: DISABLED
说明：
- 使用基于前缀的命名：<type>/<description>
- 类型：feature/、bugfix/、hotfix/、release/、docs/
- 描述使用 kebab-case
- 如果适用，包含工单/问题编号

示例：
✅ 正确：
  feature/user-authentication
  bugfix/login-validation-error
  hotfix/critical-security-patch
  feature/USER-123-payment-integration

❌ 错误：
  new-feature
  fix
  john-changes

原因：明确分支目的，使仓库更易于导航


## [规则 5] 代码审查要求 [DISABLED]
# Pull Request 和审查指南

STATUS: DISABLED
说明：
- 所有代码变更在合并前需要 PR（Pull Request）审查
- 至少需要 1 位审查者批准
- 创建 PR 前的自我审查清单：
  * 代码能编译/运行且无错误
  * 添加/更新了测试
  * 更新了文档
  * 没有调试代码或 console.logs
- 合并前处理所有审查意见

原因：保持代码质量并在团队间分享知识


## [规则 6] 文档同步 [ENABLED]
# 保持文档与代码变更同步

STATUS: ENABLED
说明：
- 修改代码时更新相关文档
- 更改端点/接口时更新 API 文档
- 添加新功能或更改设置时更新 README
- 更改函数行为时更新内联注释
- 突出记录破坏性变更

需要检查的文件：
- README.md（设置、功能、使用）
- API 文档
- 内联代码注释
- 架构图（如适用）

原因：防止文档漂移，帮助新人入职

后果：
- 过时文档导致误用、缺陷与入职延误
- API 使用方实现错误契约



## [规则 7] 测试覆盖率要求 [DISABLED]
# 新代码的测试标准

STATUS: DISABLED
说明：
- 新功能必须包含单元测试
- 错误修复必须包含回归测试
- 保持至少 80% 的代码覆盖率
- 测试边界情况和错误场景
- 在测试中模拟外部依赖

测试类型：
- 单元测试（单个函数/方法）
- 集成测试（组件交互）
- E2E 测试（关键用户流程）

原因：确保代码可靠性并防止回归


## [规则 8] 部署前检查清单 [DISABLED]
# 部署前的验证步骤

STATUS: DISABLED
说明：
部署到生产环境前：
- [ ] 所有测试通过
- [ ] 代码已审查并批准
- [ ] 文档已更新
- [ ] 变更日志已更新
- [ ] 版本号已提升
- [ ] 数据库迁移已测试
- [ ] 环境变量已配置
- [ ] 回滚计划已准备

原因：减少部署失败和停机时间


## [规则 9] 破坏性变更协议 [ENABLED]
# 如何处理破坏性变更

STATUS: ENABLED
说明：
- 清楚地记录所有破坏性变更
- 为用户提供迁移指南
- 提升 MAJOR 版本号
- 如果可能，提前宣布破坏性变更
- 在可行时保持向后兼容性
- 在移除前标记已弃用的功能

文档必须包含：
- 什么变了
- 为什么变
- 如何迁移（代码示例）
- 弃用时间表

原因：最小化对用户和维护者的干扰

后果：
- 突然的破坏性变更引发故障与信任受损
- 缺少迁移指南会阻碍采用、问题激增



## [规则 10] 依赖更新策略 [ENABLED]
# 管理第三方依赖

STATUS: ENABLED
说明：
- 定期审查依赖更新
- 在更新主要版本前彻底测试
- 在变更日志中记录依赖变更
- 在添加新依赖前检查安全漏洞
- 避免已弃用或无人维护的包
- 在生产环境中固定确切版本（不使用 ^ 或 ~）

安全：
- 运行安全审计（npm audit、pip-audit 等）
- 立即更新安全关键依赖
- 订阅关键依赖的安全公告

原因：在保持最新的同时维护安全性和稳定性

后果：
- 漏洞或弃用依赖使系统暴露于攻击面
- 未固定版本导致非确定性构建与生产漂移



## [规则 11] 文件组织标准 [DISABLED]
# 项目结构和文件放置

STATUS: DISABLED
说明：
- 遵循已建立的项目结构
- 将相关文件分组到适当的目录
- 保持文件专注于单一职责
- 使用 index 文件进行清晰导出
- 分离关注点（逻辑、UI、数据、配置）

常见结构：
```
src/
├── components/    # UI components
├── services/      # Business logic
├── utils/         # Helper functions
├── types/         # Type definitions
├── config/        # Configuration files
└── tests/         # Test files
```

原因：使代码库更易于导航和维护


## [规则 12] 错误处理标准 [ENABLED]
# 一致的错误处理方法

STATUS: ENABLED
说明：
- 始终处理错误，绝不静默失败
- 对异步操作使用 try-catch
- 使用足够的上下文记录错误
- 向用户返回有意义的错误消息
- 不要在错误消息中暴露敏感信息
- 对不同的错误类型使用自定义错误类

示例：
✅ 正确：
  try {
    await saveUser(data);
  } catch (error) {
    logger.error('Failed to save user', { userId: data.id, error });
    throw new DatabaseError('Unable to save user data');
  }

❌ 错误：
  try {
    await saveUser(data);
  } catch (error) {
    // Silent failure
  }

原因：改善调试和用户体验

后果：
- 静默失败隐藏缺陷并增加平均修复时间（MTTR）
- 错误信息泄露敏感数据引发安全事件



# ============================================
# 摘要 - 仅启用的规则
# ============================================
# 这些规则当前对您的项目是激活的：

✅ [规则 1]  变更日志管理 - 记录所有变更
✅ [规则 2]  版本号管理 - 遵循语义化版本控制
✅ [规则 6]  文档同步 - 保持文档与代码同步
✅ [规则 9]  破坏性变更协议 - 清楚地记录破坏性变更
✅ [规则 10] 依赖更新策略 - 安全地管理依赖
✅ [规则 12] 错误处理标准 - 一致的错误处理

# ============================================
# 如何启用/禁用规则
# ============================================
# 1. 将 STATUS 从 [ENABLED] 改为 [DISABLED]，或反之
# 2. 更新 SUMMARY 部分以反映当前状态
# 3. 将变更提交到版本控制
# 4. AI 将自动只遵循 ENABLED 的规则
#
# ============================================
# 项目类型配置
# ============================================
# 不同项目类型推荐启用的工作流规则

Web 应用：
- 启用： [规则 1, 2, 6, 9, 10, 12]
- 可选： [规则 3, 4, 5, 7, 8, 11]
- 说明：Web 部署需要严格的文档同步、依赖卫生与清晰的错误处理。

CLI 工具：
- 启用： [规则 1, 2, 6, 10, 12]
- 可选： [规则 3, 4, 5, 7, 8, 9, 11]
- 说明：CLI 强调可靠性与最小依赖；破坏性变更较少但出现时需记录。

库/SDK：
- 启用： [规则 1, 2, 9, 10, 12]
- 可选： [规则 3, 4, 5, 6, 7, 8, 11]
- 说明：库需要严格的版本管理、变更日志、依赖策略与健壮的错误语义。

# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-09) - 初始工作流程规范，包含 12 条规则
# ============================================
