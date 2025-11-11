---
trigger: manual
---

# Spec Index v1.0
# ============================================
# Central control file for specification suite.
# Single source of truth in .txt; optional .md mirrors can be auto-synced.
# Manages modules, global switches, rule dependencies, conflicts, and project profiles.
#
# Usage:
# 1. Place this file in the project root.
# 2. Reference it in AI conversations along with modules, e.g.:
#    "@spec-index.txt @requirements-spec.txt @workflow-spec.txt @naming-conventions.txt"
# 3. Set GLOBAL switches and PROFILE; AI applies module statuses and overrides.
#
# Last updated: 2025-11-09
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
  MIRROR_MD: DISABLED             # If ENABLED, auto-generate .md mirrors from .txt
  LANGUAGE_PAIRS: ENABLED         # Use .zh-CN files for human reading when needed

# ============================================
# MODULES
# ============================================
MODULE: requirements-spec.txt
  STATUS: ENABLED
  VERSION: v1.1
  SUMMARY:
    - 13 universal coding rules (CRITICAL/HIGH/MEDIUM)
    - Focus: completeness, reuse, minimal deps, correctness, compile/run, consistency
  TOP_PRIORITY:
    - RULE 1: Generate complete, runnable code (CRITICAL)
    - RULE 6: Verify all APIs exist (CRITICAL)
    - RULE 10: Ensure code compiles successfully (CRITICAL)
    - RULE 13: Use only real, existing libraries (CRITICAL)

MODULE: workflow-spec.txt
  STATUS: ENABLED
  VERSION: v1.0
  SUMMARY:
    - 12 workflow rules with ENABLED/DISABLED toggles
    - Focus: changelog, versioning, docs sync, breaking changes, dependency updates, error handling
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
    - 12 naming conventions with ENABLED/DISABLED toggles
    - Default enabled: variables, functions, classes, constants, files, env vars

# ============================================
# RULE DEPENDENCIES (auto-enable dependents)
# ============================================
DEPENDENCIES:
  # requirements-spec
  requirements-spec.txt::RULE 1 -> requirements-spec.txt::RULE 10
    note: completeness depends on successful compilation
  requirements-spec.txt::RULE 6 -> workflow-spec.txt::RULE 2
    note: API accuracy requires aligned versioning across releases

  # workflow-spec
  workflow-spec.txt::RULE 9 -> workflow-spec.txt::RULE 2
    note: breaking changes require proper version bumping (MAJOR)
  workflow-spec.txt::RULE 9 -> workflow-spec.txt::RULE 1
    note: breaking changes must be documented in changelog

  # naming-conventions (profile-gated)
  naming-conventions.txt::CONVENTION 6 -> PROFILE(Web)
    note: UI component naming applies to Web frontend projects

# ============================================
# RULE CONFLICTS & RESOLUTION
# ============================================
CONFLICTS:
  CASE: workflow-spec.txt::RULE 6 (Documentation Sync) vs requirements-spec.txt::RULE 5 (Only Requested Changes)
  RISK: expanding scope to update docs may conflict with minimal change policy
  RESOLUTION:
    - If code change affects public API surface or user-facing behavior, Documentation Sync is MANDATORY.
    - Otherwise, prefer minimal change; defer docs update to next scheduled docs task.
    - Priority order: CRITICAL > HIGH > MEDIUM

  CASE: dependency updates (workflow-spec.txt::RULE 10) vs minimal deps (requirements-spec.txt::RULE 3)
  RESOLUTION:
    - Security patches and critical fixes override minimal-deps preference.
    - Non-critical updates should favor minimal dependency impact.

MODULE_PRECEDENCE:
  - Code correctness and runability (requirements-spec) take precedence for generation outputs.
  - Process compliance (workflow-spec) takes precedence for release governance.
  - Naming (naming-conventions) applies unless overridden by code correctness.

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
# Use to override statuses inside module files without editing them.
# Example syntax:
OVERRIDES:
  requirements-spec.txt:
    DISABLE: [RULE 8]        # disable comment consistency when speed is critical
    ENABLE:  [RULE 9]        # enforce functionality-first explicitly
  workflow-spec.txt:
    ENABLE:  [RULE 3]        # adopt Conventional Commits
    DISABLE: [RULE 8]        # skip pre-deployment checklist for non-prod envs
  naming-conventions.txt:
    ENABLE:  [CONVENTION 7]  # turn on DB naming for backend services

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
# v1.0 (2025-11-09) - Initial central index with global switches, dependencies, conflicts, and profiles
# ============================================
