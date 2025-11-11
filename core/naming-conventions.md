---
trigger: manual
---

# Naming Conventions Specification v1.0
# ============================================
# Naming standards for AI-assisted code generation
# Enable/disable conventions by changing [ENABLED] to [DISABLED]
#
# Usage:
# 1. Place this file in project root directory
# 2. Enable/disable conventions based on your language/framework
# 3. Reference with @naming-conventions.txt in AI conversations
# 4. AI will follow only ENABLED conventions
#
# Last updated: 2025-11-09
# ============================================

## [CONVENTION 1] Variable Naming [ENABLED]
# How to name variables across the codebase

STATUS: ENABLED
LANGUAGE: All
DESCRIPTION:
- Use descriptive, meaningful names
- Avoid single-letter names except for iterators (i, j, k)
- Use nouns for variables
- Boolean variables should be questions (is, has, can, should)
- Avoid abbreviations unless widely understood

JavaScript/TypeScript Style: camelCase
✅ CORRECT:
  const userName = 'John';
  const isAuthenticated = true;
  const hasPermission = false;
  const itemCount = 10;

❌ WRONG:
  const un = 'John';
  const auth = true;
  const x = 10;

Python Style: snake_case
✅ CORRECT:
  user_name = 'John'
  is_authenticated = True
  has_permission = False
  item_count = 10

WHY: Improves code readability and maintainability


## [CONVENTION 2] Function/Method Naming [ENABLED]
# How to name functions and methods

STATUS: ENABLED
LANGUAGE: All
DESCRIPTION:
- Use verbs or verb phrases
- Name should describe what the function does
- Boolean-returning functions should start with is/has/can/should
- Event handlers should start with handle/on
- Async functions can include 'async' or use verb that implies async

JavaScript/TypeScript: camelCase
✅ CORRECT:
  function calculateTotal() { }
  function getUserById(id) { }
  function isValidEmail(email) { }
  function handleClick() { }
  async function fetchUserData() { }

❌ WRONG:
  function total() { }
  function user(id) { }
  function email(email) { }
  function click() { }

Python: snake_case
✅ CORRECT:
  def calculate_total():
  def get_user_by_id(id):
  def is_valid_email(email):
  async def fetch_user_data():

WHY: Makes function purpose immediately clear


## [CONVENTION 3] Class Naming [ENABLED]
# How to name classes and interfaces

STATUS: ENABLED
LANGUAGE: All
DESCRIPTION:
- Use PascalCase (UpperCamelCase)
- Use nouns or noun phrases
- Interface names can start with 'I' (optional, language-dependent)
- Abstract classes can start with 'Abstract' or 'Base'
- Avoid generic names like Manager, Helper, Util

✅ CORRECT:
  class UserAccount { }
  class EmailValidator { }
  class DatabaseConnection { }
  interface IUserRepository { }
  abstract class BaseController { }

❌ WRONG:
  class userAccount { }
  class validator { }
  class Manager { }
  class Helper { }

WHY: Distinguishes classes from variables/functions


## [CONVENTION 4] Constant Naming [ENABLED]
# How to name constants and configuration values

STATUS: ENABLED
LANGUAGE: All
DESCRIPTION:
- Use UPPER_SNAKE_CASE for true constants
- Group related constants in objects/enums
- Use descriptive names that explain the value's purpose

JavaScript/TypeScript:
✅ CORRECT:
  const MAX_RETRY_COUNT = 3;
  const API_BASE_URL = 'https://api.example.com';
  const DEFAULT_TIMEOUT_MS = 5000;

  enum UserRole {
    ADMIN = 'admin',
    USER = 'user',
    GUEST = 'guest'
  }

❌ WRONG:
  const maxRetry = 3;
  const apiUrl = 'https://api.example.com';
  const timeout = 5000;

Python:
✅ CORRECT:
  MAX_RETRY_COUNT = 3
  API_BASE_URL = 'https://api.example.com'
  DEFAULT_TIMEOUT_MS = 5000

WHY: Clearly identifies immutable configuration values


## [CONVENTION 5] File Naming [ENABLED]
# How to name files and directories

STATUS: ENABLED
LANGUAGE: All
DESCRIPTION:
- Use kebab-case for files (lowercase with hyphens)
- Match file name to primary export (for classes/components)
- Use .test or .spec suffix for test files
- Use .config suffix for configuration files
- Group related files in directories

JavaScript/TypeScript:
✅ CORRECT:
  user-account.ts
  email-validator.ts
  user-account.test.ts
  database.config.ts
  components/header/header-navigation.tsx

❌ WRONG:
  UserAccount.ts
  emailValidator.ts
  user_account.ts
  Test_UserAccount.ts

Python:
✅ CORRECT:
  user_account.py
  email_validator.py
  test_user_account.py
  database_config.py

WHY: Maintains consistency and follows language conventions


## [CONVENTION 6] Component Naming (Frontend) [DISABLED]
# Naming for UI components (React/Vue/Angular)

STATUS: DISABLED
LANGUAGE: JavaScript/TypeScript
DESCRIPTION:
- Use PascalCase for component names
- Use descriptive, specific names
- Prefix with type if helpful (Button, Input, Modal)
- Container components can end with 'Container'
- HOCs (Higher Order Components) should start with 'with'

React/Vue:
✅ CORRECT:
  UserProfile.tsx
  LoginForm.tsx
  NavigationButton.tsx
  UserListContainer.tsx
  withAuthentication.tsx

❌ WRONG:
  userProfile.tsx
  login.tsx
  button.tsx
  container.tsx

WHY: Aligns with framework conventions


## [CONVENTION 7] Database Table/Column Naming [DISABLED]
# Naming for database entities

STATUS: DISABLED
LANGUAGE: SQL
DESCRIPTION:
- Use snake_case for tables and columns
- Table names should be plural nouns
- Column names should be singular
- Use prefixes for foreign keys (user_id, order_id)
- Avoid reserved keywords
- Use consistent timestamp names (created_at, updated_at)

✅ CORRECT:
  Table: users
  Columns: id, user_name, email, created_at, updated_at
  
  Table: order_items
  Columns: id, order_id, product_id, quantity

❌ WRONG:
  Table: User, user
  Columns: ID, UserName, Email, CreatedDate
  Table: orderItem

WHY: Follows SQL conventions and improves query readability


## [CONVENTION 8] API Endpoint Naming [DISABLED]
# Naming for REST API routes

STATUS: DISABLED
LANGUAGE: REST APIs
DESCRIPTION:
- Use kebab-case for URLs
- Use nouns (not verbs) for resources
- Use plural nouns for collections
- Use HTTP methods for actions (GET, POST, PUT, DELETE)
- Nested resources should reflect hierarchy
- Version APIs with prefix (/v1/, /v2/)

✅ CORRECT:
  GET    /api/v1/users
  GET    /api/v1/users/:id
  POST   /api/v1/users
  PUT    /api/v1/users/:id
  DELETE /api/v1/users/:id
  GET    /api/v1/users/:id/orders

❌ WRONG:
  GET /api/getUsers
  POST /api/createUser
  GET /api/user/:id
  GET /api/Users

WHY: Follows RESTful conventions and improves API usability


## [CONVENTION 9] Environment Variable Naming [ENABLED]
# Naming for environment variables

STATUS: ENABLED
LANGUAGE: All
DESCRIPTION:
- Use UPPER_SNAKE_CASE
- Prefix with app/service name for clarity
- Group related variables with common prefix
- Be explicit about the variable purpose

✅ CORRECT:
  DATABASE_URL=postgresql://...
  DATABASE_MAX_CONNECTIONS=10
  API_SECRET_KEY=abc123
  API_BASE_URL=https://api.example.com
  REDIS_HOST=localhost
  REDIS_PORT=6379

❌ WRONG:
  dbUrl=postgresql://...
  apiKey=abc123
  host=localhost

WHY: Makes environment configuration clear and consistent


## [CONVENTION 10] Type/Interface Naming [DISABLED]
# Naming for TypeScript types and interfaces

STATUS: DISABLED
LANGUAGE: TypeScript
DESCRIPTION:
- Use PascalCase
- Interfaces can start with 'I' (optional, not always preferred)
- Types should be descriptive nouns
- Props interfaces should end with 'Props'
- State interfaces should end with 'State'
- Generic type parameters: single letter (T, K, V) or descriptive (TItem, TKey)

✅ CORRECT:
  interface User { }
  interface IUserRepository { }
  type UserId = string;
  type UserRole = 'admin' | 'user';
  interface ButtonProps { }
  interface AppState { }
  function map<TItem, TResult>(items: TItem[]): TResult[]

❌ WRONG:
  interface user { }
  type userId = string;
  interface buttonProperties { }
  function map<T1, T2>(items: T1[]): T2[]

WHY: Improves type system clarity


## [CONVENTION 11] Event Naming [DISABLED]
# Naming for events and event handlers

STATUS: DISABLED
LANGUAGE: JavaScript/TypeScript
DESCRIPTION:
- Event handlers: handleEventName or onEventName
- Custom events: use present tense verbs
- Event data: end with 'Event' or 'EventData'
- Use specific, descriptive names

✅ CORRECT:
  function handleClick() { }
  function handleUserLogin() { }
  function onModalClose() { }
  
  const userLoginEvent = new CustomEvent('userLogin', { ... });
  interface UserLoginEventData { }

❌ WRONG:
  function click() { }
  function loginHandler() { }
  function modalClosed() { }

WHY: Makes event flow clear and consistent


## [CONVENTION 12] Test Naming [DISABLED]
# Naming for test files and test cases

STATUS: DISABLED
LANGUAGE: All
DESCRIPTION:
- Test files: match source file with .test or .spec suffix
- Test suites: describe('ComponentName')
- Test cases: it('should do something') or test('does something')
- Use clear, descriptive test names that explain expected behavior

JavaScript/TypeScript:
✅ CORRECT:
  File: user-service.test.ts
  
  describe('UserService', () => {
    it('should create a new user with valid data', () => { });
    it('should throw error when email is invalid', () => { });
  });

❌ WRONG:
  File: test-user-service.ts
  
  describe('tests', () => {
    it('test1', () => { });
    it('works', () => { });
  });

WHY: Makes test purpose clear and failures easier to diagnose


# ============================================
# SUMMARY - Enabled Conventions Only
# ============================================
# These conventions are currently ACTIVE for your project:

✅ [CONVENTION 1] Variable Naming - camelCase/snake_case, descriptive
✅ [CONVENTION 2] Function/Method Naming - verbs, descriptive
✅ [CONVENTION 3] Class Naming - PascalCase, nouns
✅ [CONVENTION 4] Constant Naming - UPPER_SNAKE_CASE
✅ [CONVENTION 5] File Naming - kebab-case/snake_case
✅ [CONVENTION 9] Environment Variable Naming - UPPER_SNAKE_CASE

# ============================================
# Language-Specific Summary
# ============================================
# JavaScript/TypeScript:
#   - Variables: camelCase
#   - Functions: camelCase
#   - Classes: PascalCase
#   - Constants: UPPER_SNAKE_CASE
#   - Files: kebab-case
#
# Python:
#   - Variables: snake_case
#   - Functions: snake_case
#   - Classes: PascalCase
#   - Constants: UPPER_SNAKE_CASE
#   - Files: snake_case
#
# SQL:
#   - Tables: snake_case (plural)
#   - Columns: snake_case (singular)
#
# ============================================
# How to Enable/Disable Conventions
# ============================================
# 1. Change STATUS from [ENABLED] to [DISABLED] or vice versa
# 2. Update the SUMMARY section to reflect current state
# 3. Enable language-specific conventions based on your tech stack
# 4. AI will automatically follow only ENABLED conventions
#
# ============================================
# Project Profiles
# ============================================
# Recommended naming conventions to ENABLE per project type

Profile: Web Application
- ENABLE: [CONVENTION 1, 2, 3, 4, 5, 6, 9]
- OPTIONAL: [CONVENTION 7, 8, 10, 11, 12]
- Notes: Frontend components and environment configs benefit from strict naming clarity.

Profile: CLI Tool
- ENABLE: [CONVENTION 1, 2, 3, 4, 5, 9]
- OPTIONAL: [CONVENTION 6, 7, 8, 10, 11, 12]
- Notes: Emphasize variables, functions, constants, files, and env naming.

Profile: Library/SDK
- ENABLE: [CONVENTION 1, 2, 3, 4, 5, 10, 12]
- OPTIONAL: [CONVENTION 6, 7, 8, 9, 11]
- Notes: Libraries should prioritize class/type/test naming for API clarity and reliability.

# ============================================
# Version History
# ============================================
# v1.0 (2025-11-09) - Initial naming conventions with 12 conventions
# ============================================
