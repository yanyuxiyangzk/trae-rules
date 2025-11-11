---
trigger: manual
---

# 命名约定规范 v1.0
# ============================================
# AI 辅助代码生成的命名标准
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用约定
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据您的语言/框架启用/禁用约定
# 3. 在 AI 对话中使用 @naming-conventions.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的约定
#
# 最后更新：2025-11-09
# ============================================

## [约定 1] 变量命名 [ENABLED]
# 如何在代码库中命名变量

STATUS: ENABLED
LANGUAGE: All
说明：
- 使用描述性、有意义的名称
- 避免单字母名称，除了迭代器（i、j、k）
- 变量使用名词
- 布尔变量应该是问题形式（is、has、can、should）
- 避免缩写，除非广泛理解

JavaScript/TypeScript 风格：camelCase
✅ 正确：
  const userName = 'John';
  const isAuthenticated = true;
  const hasPermission = false;
  const itemCount = 10;

❌ 错误：
  const un = 'John';
  const auth = true;
  const x = 10;

Python 风格：snake_case
✅ 正确：
  user_name = 'John'
  is_authenticated = True
  has_permission = False
  item_count = 10

原因：提高代码可读性和可维护性


## [约定 2] 函数/方法命名 [ENABLED]
# 如何命名函数和方法

STATUS: ENABLED
LANGUAGE: All
说明：
- 使用动词或动词短语
- 名称应描述函数的作用
- 返回布尔值的函数应以 is/has/can/should 开头
- 事件处理器应以 handle/on 开头
- 异步函数可以包含 'async' 或使用暗示异步的动词

JavaScript/TypeScript：camelCase
✅ 正确：
  function calculateTotal() { }
  function getUserById(id) { }
  function isValidEmail(email) { }
  function handleClick() { }
  async function fetchUserData() { }

❌ 错误：
  function total() { }
  function user(id) { }
  function email(email) { }
  function click() { }

Python：snake_case
✅ 正确：
  def calculate_total():
  def get_user_by_id(id):
  def is_valid_email(email):
  async def fetch_user_data():

原因：使函数目的立即清晰


## [约定 3] 类命名 [ENABLED]
# 如何命名类和接口

STATUS: ENABLED
LANGUAGE: All
说明：
- 使用 PascalCase（大驼峰命名法）
- 使用名词或名词短语
- 接口名称可以以 'I' 开头（可选，取决于语言）
- 抽象类可以以 'Abstract' 或 'Base' 开头
- 避免通用名称如 Manager、Helper、Util

✅ 正确：
  class UserAccount { }
  class EmailValidator { }
  class DatabaseConnection { }
  interface IUserRepository { }
  abstract class BaseController { }

❌ 错误：
  class userAccount { }
  class validator { }
  class Manager { }
  class Helper { }

原因：区分类与变量/函数


## [约定 4] 常量命名 [ENABLED]
# 如何命名常量和配置值

STATUS: ENABLED
LANGUAGE: All
说明：
- 对真正的常量使用 UPPER_SNAKE_CASE
- 在对象/枚举中分组相关常量
- 使用描述性名称解释值的用途

JavaScript/TypeScript：
✅ 正确：
  const MAX_RETRY_COUNT = 3;
  const API_BASE_URL = 'https://api.example.com';
  const DEFAULT_TIMEOUT_MS = 5000;

  enum UserRole {
    ADMIN = 'admin',
    USER = 'user',
    GUEST = 'guest'
  }

❌ 错误：
  const maxRetry = 3;
  const apiUrl = 'https://api.example.com';
  const timeout = 5000;

Python：
✅ 正确：
  MAX_RETRY_COUNT = 3
  API_BASE_URL = 'https://api.example.com'
  DEFAULT_TIMEOUT_MS = 5000

原因：清楚地识别不可变的配置值


## [约定 5] 文件命名 [ENABLED]
# 如何命名文件和目录

STATUS: ENABLED
LANGUAGE: All
说明：
- 文件使用 kebab-case（小写带连字符）
- 文件名匹配主要导出（对于类/组件）
- 测试文件使用 .test 或 .spec 后缀
- 配置文件使用 .config 后缀
- 在目录中分组相关文件

JavaScript/TypeScript：
✅ 正确：
  user-account.ts
  email-validator.ts
  user-account.test.ts
  database.config.ts
  components/header/header-navigation.tsx

❌ 错误：
  UserAccount.ts
  emailValidator.ts
  user_account.ts
  Test_UserAccount.ts

Python：
✅ 正确：
  user_account.py
  email_validator.py
  test_user_account.py
  database_config.py

原因：保持一致性并遵循语言约定


## [约定 6] 组件命名（前端）[DISABLED]
# UI 组件的命名（React/Vue/Angular）

STATUS: DISABLED
LANGUAGE: JavaScript/TypeScript
说明：
- 组件名称使用 PascalCase
- 使用描述性、具体的名称
- 如果有帮助，使用类型前缀（Button、Input、Modal）
- 容器组件可以以 'Container' 结尾
- HOC（高阶组件）应以 'with' 开头

React/Vue：
✅ 正确：
  UserProfile.tsx
  LoginForm.tsx
  NavigationButton.tsx
  UserListContainer.tsx
  withAuthentication.tsx

❌ 错误：
  userProfile.tsx
  login.tsx
  button.tsx
  container.tsx

原因：与框架约定保持一致


## [约定 7] 数据库表/列命名 [DISABLED]
# 数据库实体的命名

STATUS: DISABLED
LANGUAGE: SQL
说明：
- 表和列使用 snake_case
- 表名应该是复数名词
- 列名应该是单数
- 外键使用前缀（user_id、order_id）
- 避免保留关键字
- 使用一致的时间戳名称（created_at、updated_at）

✅ 正确：
  Table: users
  Columns: id, user_name, email, created_at, updated_at
  
  Table: order_items
  Columns: id, order_id, product_id, quantity

❌ 错误：
  Table: User, user
  Columns: ID, UserName, Email, CreatedDate
  Table: orderItem

原因：遵循 SQL 约定并提高查询可读性


## [约定 8] API 端点命名 [DISABLED]
# REST API 路由的命名

STATUS: DISABLED
LANGUAGE: REST APIs
说明：
- URL 使用 kebab-case
- 资源使用名词（不是动词）
- 集合使用复数名词
- 操作使用 HTTP 方法（GET、POST、PUT、DELETE）
- 嵌套资源应反映层次结构
- 使用前缀对 API 进行版本控制（/v1/、/v2/）

✅ 正确：
  GET    /api/v1/users
  GET    /api/v1/users/:id
  POST   /api/v1/users
  PUT    /api/v1/users/:id
  DELETE /api/v1/users/:id
  GET    /api/v1/users/:id/orders

❌ 错误：
  GET /api/getUsers
  POST /api/createUser
  GET /api/user/:id
  GET /api/Users

原因：遵循 RESTful 约定并提高 API 可用性


## [约定 9] 环境变量命名 [ENABLED]
# 环境变量的命名

STATUS: ENABLED
LANGUAGE: All
说明：
- 使用 UPPER_SNAKE_CASE
- 使用应用/服务名称前缀以提高清晰度
- 使用公共前缀分组相关变量
- 明确说明变量用途

✅ 正确：
  DATABASE_URL=postgresql://...
  DATABASE_MAX_CONNECTIONS=10
  API_SECRET_KEY=abc123
  API_BASE_URL=https://api.example.com
  REDIS_HOST=localhost
  REDIS_PORT=6379

❌ 错误：
  dbUrl=postgresql://...
  apiKey=abc123
  host=localhost

原因：使环境配置清晰一致


## [约定 10] 类型/接口命名 [DISABLED]
# TypeScript 类型和接口的命名

STATUS: DISABLED
LANGUAGE: TypeScript
说明：
- 使用 PascalCase
- 接口可以以 'I' 开头（可选，并不总是首选）
- 类型应该是描述性名词
- Props 接口应以 'Props' 结尾
- State 接口应以 'State' 结尾
- 泛型类型参数：单字母（T、K、V）或描述性（TItem、TKey）

✅ 正确：
  interface User { }
  interface IUserRepository { }
  type UserId = string;
  type UserRole = 'admin' | 'user';
  interface ButtonProps { }
  interface AppState { }
  function map<TItem, TResult>(items: TItem[]): TResult[]

❌ 错误：
  interface user { }
  type userId = string;
  interface buttonProperties { }
  function map<T1, T2>(items: T1[]): T2[]

原因：提高类型系统清晰度


## [约定 11] 事件命名 [DISABLED]
# 事件和事件处理器的命名

STATUS: DISABLED
LANGUAGE: JavaScript/TypeScript
说明：
- 事件处理器：handleEventName 或 onEventName
- 自定义事件：使用现在时动词
- 事件数据：以 'Event' 或 'EventData' 结尾
- 使用具体、描述性的名称

✅ 正确：
  function handleClick() { }
  function handleUserLogin() { }
  function onModalClose() { }
  
  const userLoginEvent = new CustomEvent('userLogin', { ... });
  interface UserLoginEventData { }

❌ 错误：
  function click() { }
  function loginHandler() { }
  function modalClosed() { }

原因：使事件流清晰一致


## [约定 12] 测试命名 [DISABLED]
# 测试文件和测试用例的命名

STATUS: DISABLED
LANGUAGE: All
说明：
- 测试文件：匹配源文件，使用 .test 或 .spec 后缀
- 测试套件：describe('ComponentName')
- 测试用例：it('should do something') 或 test('does something')
- 使用清晰、描述性的测试名称，解释预期行为

JavaScript/TypeScript：
✅ 正确：
  File: user-service.test.ts
  
  describe('UserService', () => {
    it('should create a new user with valid data', () => { });
    it('should throw error when email is invalid', () => { });
  });

❌ 错误：
  File: test-user-service.ts
  
  describe('tests', () => {
    it('test1', () => { });
    it('works', () => { });
  });

原因：使测试目的清晰，失败更易诊断


# ============================================
# 摘要 - 仅启用的约定
# ============================================
# 这些约定当前对您的项目是激活的：

✅ [约定 1] 变量命名 - camelCase/snake_case，描述性
✅ [约定 2] 函数/方法命名 - 动词，描述性
✅ [约定 3] 类命名 - PascalCase，名词
✅ [约定 4] 常量命名 - UPPER_SNAKE_CASE
✅ [约定 5] 文件命名 - kebab-case/snake_case
✅ [约定 9] 环境变量命名 - UPPER_SNAKE_CASE

# ============================================
# 语言特定摘要
# ============================================
# JavaScript/TypeScript：
#   - 变量：camelCase
#   - 函数：camelCase
#   - 类：PascalCase
#   - 常量：UPPER_SNAKE_CASE
#   - 文件：kebab-case
#
# Python：
#   - 变量：snake_case
#   - 函数：snake_case
#   - 类：PascalCase
#   - 常量：UPPER_SNAKE_CASE
#   - 文件：snake_case
#
# SQL：
#   - 表：snake_case（复数）
#   - 列：snake_case（单数）
#
# ============================================
# 如何启用/禁用约定
# ============================================
# 1. 将 STATUS 从 [ENABLED] 改为 [DISABLED]，或反之
# 2. 更新 SUMMARY 部分以反映当前状态
# 3. 根据您的技术栈启用语言特定约定
# 4. AI 将自动只遵循 ENABLED 的约定
#
# ============================================
# 项目类型配置
# ============================================
# 不同项目类型推荐启用的命名约定

Web 应用：
- 启用： [约定 1, 2, 3, 4, 5, 6, 9]
- 可选： [约定 7, 8, 10, 11, 12]
- 说明：前端组件与环境配置需要严格的命名清晰度。

CLI 工具：
- 启用： [约定 1, 2, 3, 4, 5, 9]
- 可选： [约定 6, 7, 8, 10, 11, 12]
- 说明：强调变量、函数、常量、文件与环境变量命名。

库/SDK：
- 启用： [约定 1, 2, 3, 4, 5, 10, 12]
- 可选： [约定 6, 7, 8, 9, 11]
- 说明：库应优先保证类/类型/测试命名的 API 清晰性与可靠性。

# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-09) - 初始命名约定，包含 12 个约定
# ============================================
