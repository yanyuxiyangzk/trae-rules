---
trigger: manual
---

# 规范索引 v1.0
# ============================================
# 规范套件的中心控制文件。
# 单一事实来源为 .txt；可选开启 .md 镜像以便 IDE 展示。
# 管理模块、全局开关、规则依赖、冲突与项目类型配置。
#
# 使用方法：
# 1. 将此文件放在项目根目录。
# 2. 在 AI 对话中与模块一起引用，例如：
#    "@spec-index.txt @requirements-spec.txt @workflow-spec.txt @naming-conventions.txt"
# 3. 设置 GLOBAL 开关与 PROFILE；AI 将应用模块状态与覆盖项。
#
# 最后更新：2025-11-09
# ============================================

# ============================================
# GLOBAL CONFIG
# ============================================
GLOBAL:
  DEFAULT_PROFILE: Web            # Options: Web | CLI | Library
  ENABLE_MODULES:
    requirements-spec.txt: ENABLED
    workflow-spec.txt: ENABLED
    naming-conventions.txt: ENABLED
  MIRROR_MD: DISABLED             # 若 ENABLED，则从 .txt 自动生成 .md 镜像
  LANGUAGE_PAIRS: ENABLED         # 需要时为人阅读使用 .zh-CN 配对文件

# ============================================
# MODULES
# ============================================
MODULE: requirements-spec.txt
  STATUS: ENABLED
  VERSION: v1.1
  SUMMARY:
    - 13 条通用编码规则（CRITICAL/HIGH/MEDIUM）
    - 关注点：完整性、复用、最小依赖、正确性、编译/运行、与现有标准一致性
  TOP_PRIORITY:
    - RULE 1: Generate complete, runnable code (CRITICAL)
    - RULE 6: Verify all APIs exist (CRITICAL)
    - RULE 10: Ensure code compiles successfully (CRITICAL)
    - RULE 13: Use only real, existing libraries (CRITICAL)

MODULE: workflow-spec.txt
  STATUS: ENABLED
  VERSION: v1.0
  SUMMARY:
    - 12 条工作流规则，支持 ENABLED/DISABLED 切换
    - 关注点：变更日志、版本管理、文档同步、破坏性变更、依赖更新、错误处理
  TOP_PRIORITY:
    - RULE 1: Change Log Management (ENABLED)
    - RULE 2: Version Number Management (ENABLED)
    - RULE 6: Documentation Sync (ENABLED)
    - RULE 9: Breaking Changes Protocol (ENABLED)
    - RULE 10: Dependency Update Policy (ENABLED)
    - RULE 12: Error Handling Standards (ENABLED)

MODULE: naming-conventions.txt
  STATUS: ENABLED
  VERSION: v1.0
  SUMMARY:
    - 12 条命名约定，支持 ENABLED/DISABLED 切换
    - 默认启用：变量、函数、类、常量、文件、环境变量命名

# ============================================
# RULE DEPENDENCIES (auto-enable dependents)
# ============================================
DEPENDENCIES:
  # requirements-spec
  requirements-spec.txt::RULE 1 -> requirements-spec.txt::RULE 10
    note: 完整性依赖于成功编译
  requirements-spec.txt::RULE 6 -> workflow-spec.txt::RULE 2
    note: API 准确性要求发布版本对齐

  # workflow-spec
  workflow-spec.txt::RULE 9 -> workflow-spec.txt::RULE 2
    note: 破坏性变更需正确提升 MAJOR 版本
  workflow-spec.txt::RULE 9 -> workflow-spec.txt::RULE 1
    note: 破坏性变更必须记录到变更日志

  # naming-conventions（按 PROFILE 生效）
  naming-conventions.txt::CONVENTION 6 -> PROFILE(Web)
    note: UI 组件命名适用于 Web 前端项目

# ============================================
# RULE CONFLICTS & RESOLUTION
# ============================================
CONFLICTS:
  CASE: workflow-spec.txt::RULE 6 (Documentation Sync) vs requirements-spec.txt::RULE 5 (Only Requested Changes)
  RISK: 同步文档可能扩大修改范围，与最小化修改策略冲突
  RESOLUTION:
    - 若代码改动影响公共 API 面或用户可见行为，则 Documentation Sync 为必需。
    - 其他情况优先最小化修改；文档更新安排到后续文档任务。
    - 优先级顺序：CRITICAL > HIGH > MEDIUM

  CASE: dependency updates (workflow-spec.txt::RULE 10) vs minimal deps (requirements-spec.txt::RULE 3)
  RESOLUTION:
    - 安全补丁与关键修复优先于最小依赖策略。
    - 非关键更新应尽量减少依赖影响。

MODULE_PRECEDENCE:
  - 代码正确性与可运行性（requirements-spec）在生成输出时优先。
  - 流程合规（workflow-spec）在发布治理中优先。
  - 命名（naming-conventions）在不影响代码正确性时适用。

# ============================================
# PROJECT PROFILES (recommended enables)
# ============================================
PROFILE: Web
  REQUIREMENTS:
    ENABLE: [RULE 1, 2, 3, 5, 6, 7, 10, 11, 12, 13]
    OPTIONAL: [RULE 8, 9]
  WORKFLOW:
    ENABLE: [RULE 1, 2, 6, 9, 10, 12]
    OPTIONAL: [RULE 3, 4, 5, 7, 8, 11]
  NAMING:
    ENABLE: [CONVENTION 1, 2, 3, 4, 5, 6, 9]
    OPTIONAL: [CONVENTION 7, 8, 10, 11, 12]

PROFILE: CLI
  REQUIREMENTS:
    ENABLE: [RULE 1, 2, 3, 5, 6, 7, 10, 12, 13]
    OPTIONAL: [RULE 8, 9, 11]
  WORKFLOW:
    ENABLE: [RULE 1, 2, 6, 10, 12]
    OPTIONAL: [RULE 3, 4, 5, 7, 8, 9, 11]
  NAMING:
    ENABLE: [CONVENTION 1, 2, 3, 4, 5, 9]
    OPTIONAL: [CONVENTION 6, 7, 8, 10, 11, 12]

PROFILE: Library
  REQUIREMENTS:
    ENABLE: [RULE 1, 2, 3, 6, 7, 10, 12, 13]
    OPTIONAL: [RULE 5, 8, 9, 11]
  WORKFLOW:
    ENABLE: [RULE 1, 2, 9, 10, 12]
    OPTIONAL: [RULE 3, 4, 5, 6, 7, 8, 11]
  NAMING:
    ENABLE: [CONVENTION 1, 2, 3, 4, 5, 10, 12]
    OPTIONAL: [CONVENTION 6, 7, 8, 9, 11]

# ============================================
# OVERRIDES (optional per-project switches)
# ============================================
# 用于在不编辑模块文件的情况下覆盖模块内状态。
# 示例语法：
OVERRIDES:
  requirements-spec.txt:
    DISABLE: [RULE 8]        # 速度优先时临时关闭注释一致性
    ENABLE:  [RULE 9]        # 明确启用“功能优先”
  workflow-spec.txt:
    ENABLE:  [RULE 3]        # 采用 Conventional Commits
    DISABLE: [RULE 8]        # 非生产环境跳过部署前检查清单
  naming-conventions.txt:
    ENABLE:  [CONVENTION 7]  # 后端服务开启数据库命名约定

# ============================================
# SUMMARY
# ============================================
ACTIVE:
  PROFILE: Web
  MODULES: requirements-spec.txt (ENABLED), workflow-spec.txt (ENABLED), naming-conventions.txt (ENABLED)
  MIRROR_MD: DISABLED

# ============================================
# Version History
# ============================================
# v1.0 (2025-11-09) - 首个中心索引：含全局开关、依赖、冲突与项目配置
# ============================================
