---
trigger: manual
---

# Workflow Specification v1.0
# ============================================
# Development workflow and process rules for AI-assisted coding
# Enable/disable rules by changing [ENABLED] to [DISABLED]
#
# Usage:
# 1. Place this file in project root directory
# 2. Enable/disable rules based on your project needs
# 3. Reference with @workflow-spec.txt in AI conversations
# 4. AI will follow only ENABLED rules
#
# Last updated: 2025-11-09
# ============================================

## [RULE 1] Change Log Management [ENABLED]
# Maintain update records in a changelog file

STATUS: ENABLED
DESCRIPTION:
- Document all significant changes in CHANGELOG.md or similar file
- Include version number, date, and description of changes
- Update changelog before committing code changes
- Follow "Keep a Changelog" format (Added/Changed/Deprecated/Removed/Fixed/Security)

Example Format:
```
## [1.2.0] - 2025-11-09
### Added
- User authentication with JWT tokens
- Password reset functionality

### Fixed
- Login form validation error
```

WHY: Provides clear history of project evolution and helps team track what changed and when

CONSEQUENCES:
- Missing changelog makes releases unreliable and hard to audit
- Team loses visibility; support cannot track changes
- Compliance and postmortems become error-prone



## [RULE 2] Version Number Management [ENABLED]
# Update version numbers consistently across project

STATUS: ENABLED
DESCRIPTION:
- Follow Semantic Versioning (MAJOR.MINOR.PATCH)
- Update version in package.json/version files when making releases
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)
- Update version in all relevant files (package.json, setup.py, build.gradle, etc.)

Example:
- 1.0.0 → 1.0.1 (bug fix)
- 1.0.1 → 1.1.0 (new feature)
- 1.1.0 → 2.0.0 (breaking change)

WHY: Ensures consistent version tracking and dependency management

CONSEQUENCES:
- Incorrect versioning confuses consumers and breaks integrations
- Untracked breaking changes cause widespread downstream failures



## [RULE 3] Git Commit Message Format [DISABLED]
# Standardize commit message structure

STATUS: DISABLED
DESCRIPTION:
- Follow Conventional Commits specification
- Format: <type>(<scope>): <subject>
- Types: feat, fix, docs, style, refactor, test, chore
- Example: "feat(auth): add JWT token validation"
- Keep subject line under 72 characters
- Use imperative mood ("add" not "added")

Example:
✅ CORRECT:
  feat(login): add password reset functionality
  fix(api): resolve timeout issue in user endpoint

❌ WRONG:
  updated login
  fixed bugs

WHY: Makes commit history searchable and enables automated changelog generation


## [RULE 4] Branch Naming Convention [DISABLED]
# Consistent branch naming strategy

STATUS: DISABLED
DESCRIPTION:
- Use prefix-based naming: <type>/<description>
- Types: feature/, bugfix/, hotfix/, release/, docs/
- Use kebab-case for description
- Include ticket/issue number if applicable

Example:
✅ CORRECT:
  feature/user-authentication
  bugfix/login-validation-error
  hotfix/critical-security-patch
  feature/USER-123-payment-integration

❌ WRONG:
  new-feature
  fix
  john-changes

WHY: Clarifies branch purpose and makes repository easier to navigate


## [RULE 5] Code Review Requirements [DISABLED]
# Pull request and review guidelines

STATUS: DISABLED
DESCRIPTION:
- All code changes require PR (Pull Request) review before merging
- Minimum 1 reviewer approval required
- Self-review checklist before creating PR:
  * Code compiles/runs without errors
  * Tests added/updated
  * Documentation updated
  * No debug code or console.logs
- Address all review comments before merging

WHY: Maintains code quality and shares knowledge across team


## [RULE 6] Documentation Sync [ENABLED]
# Keep documentation in sync with code changes

STATUS: ENABLED
DESCRIPTION:
- Update relevant documentation when modifying code
- Update API docs when changing endpoints/interfaces
- Update README when adding new features or changing setup
- Update inline comments when changing function behavior
- Document breaking changes prominently

Files to check:
- README.md (setup, features, usage)
- API documentation
- Inline code comments
- Architecture diagrams (if applicable)

WHY: Prevents documentation drift and helps onboarding

CONSEQUENCES:
- Outdated docs lead to misuse, bugs, and onboarding delays
- API consumers implement wrong contracts



## [RULE 7] Test Coverage Requirements [DISABLED]
# Testing standards for new code

STATUS: DISABLED
DESCRIPTION:
- New features must include unit tests
- Bug fixes must include regression tests
- Maintain minimum 80% code coverage
- Test edge cases and error scenarios
- Mock external dependencies in tests

Test Types:
- Unit tests (individual functions/methods)
- Integration tests (component interactions)
- E2E tests (critical user flows)

WHY: Ensures code reliability and prevents regressions


## [RULE 8] Pre-deployment Checklist [DISABLED]
# Verification steps before deployment

STATUS: DISABLED
DESCRIPTION:
Before deploying to production:
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version number bumped
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Rollback plan prepared

WHY: Reduces deployment failures and downtime


## [RULE 9] Breaking Changes Protocol [ENABLED]
# How to handle breaking changes

STATUS: ENABLED
DESCRIPTION:
- Clearly document all breaking changes
- Provide migration guide for users
- Bump MAJOR version number
- Announce breaking changes in advance when possible
- Maintain backward compatibility when feasible
- Mark deprecated features before removal

Documentation must include:
- What changed
- Why it changed
- How to migrate (code examples)
- Timeline for deprecation

WHY: Minimizes disruption for users and maintainers

CONSEQUENCES:
- Surprise breaking changes cause outages and trust erosion
- Without migration guides, adoption stalls and issues spike



## [RULE 10] Dependency Update Policy [ENABLED]
# Managing third-party dependencies

STATUS: ENABLED
DESCRIPTION:
- Review dependency updates regularly
- Test thoroughly before updating major versions
- Document dependency changes in changelog
- Check for security vulnerabilities before adding new dependencies
- Avoid deprecated or unmaintained packages
- Pin exact versions in production (no ^ or ~)

Security:
- Run security audits (npm audit, pip-audit, etc.)
- Update security-critical dependencies immediately
- Subscribe to security advisories for key dependencies

WHY: Maintains security and stability while staying current

CONSEQUENCES:
- Vulnerable or deprecated deps expose the system to attacks
- Unpinned versions cause nondeterministic builds and production drift



## [RULE 11] File Organization Standards [DISABLED]
# Project structure and file placement

STATUS: DISABLED
DESCRIPTION:
- Follow established project structure
- Group related files in appropriate directories
- Keep files focused on single responsibility
- Use index files for clean exports
- Separate concerns (logic, UI, data, config)

Common structure:
```
src/
├── components/    # UI components
├── services/      # Business logic
├── utils/         # Helper functions
├── types/         # Type definitions
├── config/        # Configuration files
└── tests/         # Test files
```

WHY: Makes codebase easier to navigate and maintain


## [RULE 12] Error Handling Standards [ENABLED]
# Consistent error handling approach

STATUS: ENABLED
DESCRIPTION:
- Always handle errors, never silently fail
- Use try-catch for async operations
- Log errors with sufficient context
- Return meaningful error messages to users
- Don't expose sensitive information in error messages
- Use custom error classes for different error types

Example:
✅ CORRECT:
  try {
    await saveUser(data);
  } catch (error) {
    logger.error('Failed to save user', { userId: data.id, error });
    throw new DatabaseError('Unable to save user data');
  }

❌ WRONG:
  try {
    await saveUser(data);
  } catch (error) {
    // Silent failure
  }

WHY: Improves debugging and user experience

CONSEQUENCES:
- Silent failures hide defects and increase MTTR
- Leaking sensitive data in errors creates security incidents



# ============================================
# SUMMARY - Enabled Rules Only
# ============================================
# These rules are currently ACTIVE for your project:

✅ [RULE 1]  Change Log Management - Document all changes
✅ [RULE 2]  Version Number Management - Follow semantic versioning
✅ [RULE 6]  Documentation Sync - Keep docs updated with code
✅ [RULE 9]  Breaking Changes Protocol - Document breaking changes clearly
✅ [RULE 10] Dependency Update Policy - Manage dependencies securely
✅ [RULE 12] Error Handling Standards - Consistent error handling

# ============================================
# How to Enable/Disable Rules
# ============================================
# 1. Change STATUS from [ENABLED] to [DISABLED] or vice versa
# 2. Update the SUMMARY section to reflect current state
# 3. Commit changes to version control
# 4. AI will automatically follow only ENABLED rules
#
# ============================================
# Project Profiles
# ============================================
# Recommended workflow rules to ENABLE per project type

Profile: Web Application
- ENABLE: [RULE 1, 2, 6, 9, 10, 12]
- OPTIONAL: [RULE 3, 4, 5, 7, 8, 11]
- Notes: Web deployments benefit from strict docs sync, dependency hygiene, and clear error handling.

Profile: CLI Tool
- ENABLE: [RULE 1, 2, 6, 10, 12]
- OPTIONAL: [RULE 3, 4, 5, 7, 8, 9, 11]
- Notes: CLI focuses on reliability and minimal deps; breaking changes less frequent but documented when present.

Profile: Library/SDK
- ENABLE: [RULE 1, 2, 9, 10, 12]
- OPTIONAL: [RULE 3, 4, 5, 6, 7, 8, 11]
- Notes: Libraries need rigorous versioning, changelogs, dependency policy, and robust error semantics.

# ============================================
# Version History
# ============================================
# v1.0 (2025-11-09) - Initial workflow specification with 12 rules
# ============================================
