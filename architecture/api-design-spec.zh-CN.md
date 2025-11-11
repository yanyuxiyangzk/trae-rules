---
trigger: manual
---

# API 设计规范 v1.0
# ============================================
# AI 辅助开发的 API 设计标准和要求
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据项目需求启用/禁用规则
# 3. 在 AI 对话中使用 @api-design-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 依赖规范：requirements-spec.txt、naming-conventions.txt、security-spec.txt
# 最后更新：2025-11-10
# ============================================

## [规则 1] RESTful 设计原则 [ENABLED]
# 遵循 REST 架构风格

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 使用 HTTP 方法表示操作（GET/POST/PUT/PATCH/DELETE）
- 资源使用名词，不使用动词
- 集合使用复数形式
- URL 应该是层次化的，反映资源关系
- 使用 HTTP 状态码表示结果

示例：
✅ 正确：
  GET    /api/v1/users           # 获取用户列表
  GET    /api/v1/users/:id       # 获取单个用户
  POST   /api/v1/users           # 创建用户
  PUT    /api/v1/users/:id       # 完整更新用户
  PATCH  /api/v1/users/:id       # 部分更新用户
  DELETE /api/v1/users/:id       # 删除用户
  GET    /api/v1/users/:id/orders  # 获取用户的订单

❌ 错误：
  GET  /api/getUsers
  POST /api/createUser
  GET  /api/user/:id
  POST /api/users/delete/:id

WHY: 统一的 RESTful 设计提高 API 可预测性和易用性


## [规则 2] API 版本控制 [ENABLED]
# 实施明确的版本管理

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 在 URL 中包含版本号（/v1/、/v2/）
- 版本号使用整数，不使用小数
- 主要版本变更时增加版本号
- 保持旧版本向后兼容一段时间
- 提前通知废弃计划

后果：
- 无版本控制导致破坏性变更影响现有客户端
- 难以并行维护多个 API 版本

示例：
✅ 正确：
  /api/v1/users
  /api/v2/users
  /api/v3/users

❌ 错误：
  /api/users
  /api/v1.2/users
  /api/2023-11-10/users

配置示例：
```typescript
// Express 路由
app.use('/api/v1', routerV1);
app.use('/api/v2', routerV2);

// 版本废弃响应头
res.set('X-API-Deprecation-Date', '2025-12-31');
res.set('X-API-Sunset-Date', '2026-06-30');
```


## [规则 3] 请求与响应格式 [ENABLED]
# 统一的数据格式标准

STATUS: ENABLED
说明：
- 使用 JSON 作为默认格式
- 请求使用 Content-Type: application/json
- 响应统一结构：data, error, meta
- 时间使用 ISO 8601 格式
- 分页使用统一参数（page, limit, offset）

示例（响应格式）：
```json
// 成功响应
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com",
    "createdAt": "2025-11-10T10:30:00Z"
  },
  "meta": {
    "timestamp": "2025-11-10T10:30:05Z",
    "version": "v1"
  }
}

// 错误响应
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "field": "email",
    "details": {
      "value": "invalid-email",
      "expected": "user@example.com"
    }
  },
  "meta": {
    "timestamp": "2025-11-10T10:30:05Z",
    "requestId": "abc-123-def"
  }
}

// 分页响应
{
  "data": [...],
  "meta": {
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```


## [规则 4] HTTP 状态码使用 [ENABLED]
# 正确使用 HTTP 状态码

STATUS: ENABLED
说明：
- 2xx - 成功
  - 200 OK - 成功（GET, PUT, PATCH）
  - 201 Created - 资源已创建（POST）
  - 204 No Content - 成功但无返回内容（DELETE）
- 4xx - 客户端错误
  - 400 Bad Request - 请求格式错误
  - 401 Unauthorized - 未认证
  - 403 Forbidden - 已认证但无权限
  - 404 Not Found - 资源不存在
  - 409 Conflict - 资源冲突
  - 422 Unprocessable Entity - 验证失败
- 5xx - 服务器错误
  - 500 Internal Server Error - 服务器内部错误
  - 503 Service Unavailable - 服务不可用

示例：
```typescript
// 创建资源
app.post('/api/v1/users', async (req, res) => {
  const user = await createUser(req.body);
  res.status(201).json({ data: user });
});

// 删除资源
app.delete('/api/v1/users/:id', async (req, res) => {
  await deleteUser(req.params.id);
  res.status(204).send();
});

// 验证失败
if (!isValidEmail(email)) {
  return res.status(422).json({
    error: {
      code: 'VALIDATION_ERROR',
      message: 'Invalid email format'
    }
  });
}

// 权限不足
if (!user.isAdmin) {
  return res.status(403).json({
    error: {
      code: 'FORBIDDEN',
      message: 'Admin access required'
    }
  });
}
```


## [规则 5] 查询参数规范 [ENABLED]
# 统一的查询参数命名

STATUS: ENABLED
说明：
- 分页：page, limit, offset
- 排序：sort (格式：field:asc 或 field:desc)
- 过滤：使用字段名直接过滤
- 搜索：q 或 search
- 字段选择：fields（逗号分隔）
- 关联资源：include 或 expand

示例：
```
GET /api/v1/users?page=1&limit=20
GET /api/v1/users?sort=createdAt:desc
GET /api/v1/users?status=active&role=admin
GET /api/v1/users?q=john
GET /api/v1/users?fields=id,name,email
GET /api/v1/users?include=orders,profile
GET /api/v1/users?createdAt[gte]=2025-01-01&createdAt[lte]=2025-12-31
```


## [规则 6] 认证与授权 [ENABLED]
# API 安全机制

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 使用 JWT 或 OAuth 2.0 认证
- API 密钥用于服务间调用
- 敏感操作需要额外验证（MFA）
- 使用 HTTPS 传输
- 实施速率限制

示例：
```typescript
// JWT 认证中间件
async function authenticate(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({
      error: { code: 'UNAUTHORIZED', message: 'Token required' }
    });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({
      error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token' }
    });
  }
}

// 速率限制
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 最多100个请求
  message: { error: { code: 'RATE_LIMIT_EXCEEDED' } }
});

app.use('/api/', limiter);
```


## [规则 7] 错误处理标准 [ENABLED]
# 统一的错误响应格式

STATUS: ENABLED
说明：
- 使用标准化的错误码
- 提供清晰的错误消息
- 包含错误详情和建议
- 生产环境不暴露堆栈跟踪
- 记录错误日志

示例：
```typescript
// 错误响应格式
interface ErrorResponse {
  error: {
    code: string;          // 错误码
    message: string;       // 用户友好的消息
    field?: string;        // 错误字段（验证错误）
    details?: any;         // 额外详情
    suggestion?: string;   // 解决建议
  };
  meta: {
    timestamp: string;
    requestId: string;
  };
}

// 全局错误处理
app.use((err, req, res, next) => {
  logger.error('API Error', { error: err, path: req.path });
  
  const response: ErrorResponse = {
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production' 
        ? 'Internal server error' 
        : err.message
    },
    meta: {
      timestamp: new Date().toISOString(),
      requestId: req.id
    }
  };
  
  res.status(err.statusCode || 500).json(response);
});
```


## [规则 8] API 文档化 [ENABLED]
# 完整的 API 文档

STATUS: ENABLED
说明：
- 使用 OpenAPI/Swagger 规范
- 文档包含所有端点、参数、响应
- 提供请求示例和响应示例
- 文档与代码同步更新
- 提供交互式 API 测试界面

示例（OpenAPI 3.0）：
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /api/v1/users:
    get:
      summary: Get user list
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
        '401':
          description: Unauthorized
```


## [规则 9] 幂等性设计 [ENABLED]
# 确保操作幂等性

STATUS: ENABLED
说明：
- GET, PUT, DELETE 操作应该是幂等的
- POST 使用幂等键避免重复创建
- 使用乐观锁处理并发更新
- 提供操作去重机制

示例：
```typescript
// 幂等键处理
app.post('/api/v1/orders', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];
  
  if (idempotencyKey) {
    // 检查是否已处理过
    const existing = await cache.get(idempotencyKey);
    if (existing) {
      return res.status(200).json(existing);
    }
  }
  
  const order = await createOrder(req.body);
  
  if (idempotencyKey) {
    await cache.set(idempotencyKey, order, 3600);
  }
  
  res.status(201).json({ data: order });
});

// 乐观锁
app.put('/api/v1/users/:id', async (req, res) => {
  const { version } = req.body;
  const user = await User.findById(req.params.id);
  
  if (user.version !== version) {
    return res.status(409).json({
      error: {
        code: 'CONFLICT',
        message: 'Resource has been modified by another request'
      }
    });
  }
  
  user.version += 1;
  await user.save();
  res.json({ data: user });
});
```


## [规则 10] 批量操作支持 [DISABLED]
# 支持批量操作

STATUS: DISABLED
说明：
- 提供批量创建/更新/删除接口
- 限制单次批量操作数量
- 返回每个操作的结果
- 支持部分成功场景

示例：
```typescript
app.post('/api/v1/users/batch', async (req, res) => {
  const { users } = req.body;
  
  if (users.length > 100) {
    return res.status(400).json({
      error: { code: 'BATCH_TOO_LARGE', message: 'Maximum 100 items' }
    });
  }
  
  const results = await Promise.allSettled(
    users.map(user => createUser(user))
  );
  
  const response = {
    data: {
      success: results.filter(r => r.status === 'fulfilled').length,
      failed: results.filter(r => r.status === 'rejected').length,
      results: results.map((r, i) => ({
        index: i,
        status: r.status,
        data: r.status === 'fulfilled' ? r.value : null,
        error: r.status === 'rejected' ? r.reason.message : null
      }))
    }
  };
  
  res.status(207).json(response); // 207 Multi-Status
});
```


## [规则 11] CORS 配置 [ENABLED]
# 跨域资源共享配置

STATUS: ENABLED
说明：
- 配置允许的域名白名单
- 设置允许的 HTTP 方法
- 配置允许的请求头
- 启用凭证支持（如需要）

示例：
```typescript
import cors from 'cors';

const corsOptions = {
  origin: process.env.NODE_ENV === 'production'
    ? ['https://example.com', 'https://app.example.com']
    : '*',
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  exposedHeaders: ['X-Total-Count', 'X-Page-Count'],
  credentials: true,
  maxAge: 86400 // 预检请求缓存时间
};

app.use(cors(corsOptions));
```


## [规则 12] 性能优化 [ENABLED]
# API 性能最佳实践

STATUS: ENABLED
说明：
- 实施响应缓存（ETag, Cache-Control）
- 支持字段过滤减少传输数据
- 使用分页避免大数据集
- 实施压缩（gzip）
- 提供批量端点减少请求次数

示例：
```typescript
// ETag 缓存
app.get('/api/v1/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  const etag = generateETag(user);
  
  if (req.headers['if-none-match'] === etag) {
    return res.status(304).send();
  }
  
  res.set('ETag', etag);
  res.set('Cache-Control', 'max-age=300');
  res.json({ data: user });
});

// 字段过滤
app.get('/api/v1/users', async (req, res) => {
  const fields = req.query.fields?.split(',') || [];
  const users = await User.find().select(fields.join(' '));
  res.json({ data: users });
});

// 压缩
import compression from 'compression';
app.use(compression());
```


# ============================================
# 项目类型配置
# ============================================

Web 应用（后端 API）：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
- 可选： [规则 10]
- 关键：RESTful 设计、版本控制、认证授权、错误处理

微服务 API：
- 启用： [规则 1, 2, 3, 4, 6, 7, 9, 12]
- 可选： [规则 5, 8, 10, 11]
- 关键：版本控制、幂等性、性能优化

公共 API/SDK：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
- 可选： [规则 10]
- 关键：完整文档、版本控制、向后兼容


# ============================================
# 与其他规范的集成
# ============================================

DEPENDENCIES:
  api-design-spec.txt::RULE 6 -> security-spec.txt::RULE 2
    note: API 认证授权遵循安全规范
  api-design-spec.txt::RULE 7 -> error-handling-spec.txt::RULE 1
    note: API 错误响应遵循错误处理规范
  api-design-spec.txt::RULE 5 -> naming-conventions.txt::CONVENTION 8
    note: API 端点命名遵循命名约定


# ============================================
# 摘要 - 启用的规则
# ============================================

✅ [规则 1]  RESTful 设计原则 - HTTP方法和资源命名
✅ [规则 2]  API 版本控制 - URL版本号管理
✅ [规则 3]  请求响应格式 - 统一JSON结构
✅ [规则 4]  HTTP 状态码 - 正确使用状态码
✅ [规则 5]  查询参数规范 - 统一参数命名
✅ [规则 6]  认证与授权 - JWT/OAuth安全
✅ [规则 7]  错误处理标准 - 标准化错误响应
✅ [规则 8]  API 文档化 - OpenAPI/Swagger
✅ [规则 9]  幂等性设计 - 操作去重机制
✅ [规则 11] CORS 配置 - 跨域资源共享
✅ [规则 12] 性能优化 - 缓存和压缩


# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-10) - 初始 API 设计规范，包含 12 条规则
# ============================================
