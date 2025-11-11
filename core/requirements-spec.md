---
trigger: manual
---

# Development Requirements Specification v1.1
# ============================================
# AI-assisted development coding rules and requirements
# Follow these rules strictly when generating code
#
# Usage:
# 1. Place this file in project root directory
# 2. Reference with @requirements-spec.txt in AI conversations
# 3. AI will automatically follow these rules
#
# Scope: All programming languages and frameworks
# Last updated: 2025-11-09
# ============================================

## [RULE 1] Generate Complete, Runnable Code (Priority: CRITICAL)
# Generate complete, executable code without placeholders

- Code must be immediately executable, no placeholders allowed
- Include all necessary imports, dependencies, and configurations
- Provide full implementation, not partial code snippets
- No incomplete functions or missing logic
- No TODO comments or "implement later" notes

Consequences:
- Placeholder or partial code leads to runtime failures and rework
- Missing imports/configurations cause build breaks and deployment delays

Example:
❌ WRONG:
  function processData() {
    // TODO: implement this
  }

✅ CORRECT:
  function processData(data: string[]): ProcessedData {
    return data.map(item => ({
      id: generateId(),
      value: item.trim(),
      timestamp: Date.now()
    }));
  }

## [RULE 2] Reuse Existing Code and APIs (Priority: HIGH)
# MUST reuse existing interfaces and APIs before creating new ones

- Check existing codebase before creating new interfaces
- Do not reinvent existing functionality
- Reference and utilize current API endpoints
- Maintain compatibility with existing interfaces
- Search for similar implementations first

Example:
❌ WRONG:
  // Creating new validation function
  function validateUser(user) {
    // custom validation logic
  }

✅ CORRECT:
  // Use existing validation service
  import { validateUser } from '@/services/auth';
  validateUser(user);

## [RULE 3] Minimize New Dependencies (Priority: HIGH)
# Use existing project dependencies first

- Prioritize existing project dependencies
- Justify any new dependency additions
- Check package.json/requirements.txt before adding
- Prefer built-in libraries over external packages
- Avoid heavy dependencies when simple native solutions exist

Example:
❌ WRONG:
  import moment from 'moment';  // Heavy new dependency
  moment(date).format('YYYY-MM-DD');

✅ CORRECT:
  // Use native API
  new Date(date).toISOString().split('T')[0];

## [RULE 4] Learn from Previous Mistakes (Priority: HIGH)
# Do not repeat errors from conversation history

- Reference conversation history before implementing
- Avoid making the same mistake twice
- Apply corrections consistently across all code
- Remember user feedback and preferences

## [RULE 5] Make Only Requested Changes (Priority: HIGH)
# Only modify what was explicitly requested - no unauthorized refactoring

- Do not refactor working code without permission
- Keep original logic unless asked to improve
- Stick to the specific task requirements
- Minimize scope of changes
- Preserve existing code structure

Consequences:
- Unrequested refactors introduce regressions and slow reviews
- Scope creep increases cost and misses deadlines

Example (User only asked to change button color):
❌ WRONG:
  // Refactoring entire component architecture
  // Switching to Context API
  // Adding performance optimizations

✅ CORRECT:
  // Only change button color
  <button style={{ backgroundColor: 'blue' }}>Submit</button>

## [RULE 6] Verify All APIs Exist (Priority: CRITICAL)
# Do not invent non-existent APIs or methods

- Verify APIs exist before using them
- Check documentation for correct API signatures
- Only use confirmed, available APIs
- Do not make up fictional library methods
- Test API compatibility with project version

Consequences:
- Using non-existent or incompatible APIs causes crashes and support burden
- Incorrect signatures lead to silent data corruption

Example:
❌ WRONG:
  array.removeAt(index);  // Non-existent method

✅ CORRECT:
  array.splice(index, 1);  // Standard method

## [RULE 7] Fix Errors Completely on First Attempt (Priority: HIGH)
# Address root cause, not symptoms

- Test solutions before presenting
- Provide working fixes, not iterative attempts
- Solve root cause, not just symptoms
- Ensure code compiles and runs before delivery

## [RULE 8] Keep Comments Consistent with Code (Priority: MEDIUM)
# Ensure comments match actual implementation

- Update comments when code changes
- Provide accurate, truthful documentation
- No misleading or outdated comments
- Comments should reflect actual behavior

Example:
❌ WRONG:
  // Get user list
  function deleteUser(id) { ... }  // Comment doesn't match

✅ CORRECT:
  // Delete specified user
  function deleteUser(id) { ... }

## [RULE 9] Functionality Over Perfection (Priority: MEDIUM)
# Prioritize getting code working first

- Working code > perfect code
- Functionality before optimization
- Deliver MVP before enhancements
- Get it running, then make it better

## [RULE 10] Ensure Code Compiles Successfully (Priority: CRITICAL)
# All code must compile/run without errors

- Check syntax before delivery
- Resolve all compilation errors
- Test build process
- Verify imports and dependencies are correct

Consequences:
- Build failures block delivery pipelines
- Runtime errors degrade user experience and trust

## [RULE 11] Follow Provided Examples Exactly (Priority: MEDIUM)
# When examples are given, match them precisely

- Match code style from examples
- Use same patterns and structures
- Maintain consistency with provided samples
- Replicate structure and naming conventions

## [RULE 12] Respect Project Naming Conventions (Priority: MEDIUM)
# Preserve existing naming patterns

- Do not rename variables/functions without permission
- Follow project's naming style
- Maintain consistency with codebase
- Match existing patterns (camelCase, snake_case, etc.)

## [RULE 13] Use Only Real, Existing Libraries (Priority: CRITICAL)
# Only import actual, existing libraries

- Verify package exists before importing
- No fictional or made-up packages
- Check npm/pip/package registry
- Confirm library version compatibility

Consequences:
- Importing fictional or wrong-version libraries breaks builds
- Security exposure from unvetted packages

Example:
❌ WRONG:
  import { magicHelper } from 'super-magic-lib';  // Doesn't exist

✅ CORRECT:
  import { useState } from 'react';  // Real library

# ============================================
# SUMMARY - Critical Rules (Top Priority)
# ============================================

1. Generate COMPLETE, runnable code (no TODOs, no placeholders)
2. Reuse existing interfaces/APIs - don't create new ones unnecessarily
3. Minimize dependencies - use what already exists
4. Make ONLY requested changes - no unauthorized refactoring
5. Verify all APIs exist before using them
6. Code must compile and run immediately
7. Learn from previous errors in conversation
8. Use only real, existing libraries
9. Follow provided examples exactly
10. Keep comments consistent with implementation

# ============================================
# Usage
# ============================================
# Reference this file in AI conversations:
#   "@requirements-spec.txt implement user login"
#
# Or mention in project README:
#   "This project uses requirements-spec.txt for AI code generation standards"
#
# ============================================
# Project Profiles
# ============================================
# Recommended rule sets to enable per project type

Profile: Web Application
- ENABLE: [RULE 1, 2, 3, 5, 6, 7, 10, 11, 12, 13]
- OPTIONAL: [RULE 8, 9]
- Rationale: Web apps need completeness, API correctness, fast fixes, and compile/run guarantees. Comments and examples improve collaboration.

Profile: CLI Tool
- ENABLE: [RULE 1, 2, 3, 5, 6, 7, 10, 12, 13]
- OPTIONAL: [RULE 8, 9, 11]
- Rationale: CLI focuses on reliability, minimal deps, error handling, and running clean in varied environments.

Profile: Library/SDK
- ENABLE: [RULE 1, 2, 3, 6, 7, 10, 12, 13]
- OPTIONAL: [RULE 5, 8, 9, 11]
- Rationale: Libraries emphasize API correctness, versioning discipline, completeness, and high-quality error handling with minimal dependencies.

# ============================================
# Version History
# ============================================
# v1.1 (2025-11-09) - Refined to 13 essential rules, removed language-specific requirements
# v1.0 (2025-11-09) - Initial version based on user feedback data
# ============================================
