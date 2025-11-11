---
trigger: manual
---

# 错误处理规范 v1.0
# ============================================
# AI 辅助开发的错误处理标准和要求
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据项目需求启用/禁用规则
# 3. 在 AI 对话中使用 @error-handling-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 依赖规范：requirements-spec.txt、security-spec.txt、workflow-spec.txt
# 最后更新：2025-11-10
# ============================================

## [规则 1] 错误分类体系 [ENABLED]
# 建立清晰的错误分类

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 业务错误：验证失败、业务规则违反（用户可恢复）
- 系统错误：数据库连接失败、文件 I/O 错误（需运维介入）
- 第三方错误：外部 API 调用失败、支付网关错误（需降级处理）
- 客户端错误：4xx - 请求错误
- 服务端错误：5xx - 服务器内部错误

后果：
- 混淆错误类型导致错误处理策略失效
- 用户无法理解错误含义，支持成本增加

示例：
```typescript
// 错误分类
class BusinessError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = 'BusinessError';
  }
}

class SystemError extends Error {
  constructor(message: string, public originalError?: Error) {
    super(message);
    this.name = 'SystemError';
  }
}

class ExternalServiceError extends Error {
  constructor(public service: string, message: string) {
    super(message);
    this.name = 'ExternalServiceError';
  }
}

// 使用示例
if (!user.isActive) {
  throw new BusinessError('账户已被禁用', 'ACCOUNT_DISABLED');
}

if (!dbConnection) {
  throw new SystemError('数据库连接失败');
}
```


## [规则 2] 自定义错误类 [ENABLED]
# 创建领域特定的错误类

STATUS: ENABLED
说明：
- 为不同领域创建专用错误类
- 继承标准 Error 类
- 包含错误代码、元数据、原始错误
- 提供结构化错误信息

示例：
```typescript
class ValidationError extends BusinessError {
  constructor(
    public field: string,
    public value: any,
    message: string
  ) {
    super(message, 'VALIDATION_ERROR');
    this.name = 'ValidationError';
  }
}

class AuthenticationError extends BusinessError {
  constructor(message: string = '认证失败') {
    super(message, 'AUTH_FAILED');
    this.name = 'AuthenticationError';
  }
}

class NotFoundError extends BusinessError {
  constructor(public resource: string, public id: string) {
    super(`${resource} 未找到: ${id}`, 'NOT_FOUND');
    this.name = 'NotFoundError';
  }
}

// 使用
throw new ValidationError('email', userInput.email, '邮箱格式无效');
throw new NotFoundError('User', userId);
```


## [规则 3] 错误日志记录 [ENABLED]
# 标准化日志记录

STATUS: ENABLED
说明：
- 业务错误：INFO 或 WARN 级别
- 系统错误：ERROR 级别
- 关键错误：FATAL 级别
- 记录上下文：用户 ID、请求 ID、时间戳、堆栈跟踪
- 不记录敏感数据（密码、令牌、信用卡）

后果：
- 日志缺失导致故障排查困难
- 过度日志导致存储成本高、信噪比低

示例：
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// 业务错误
logger.warn('用户登录失败', {
  userId: user.id,
  email: user.email,
  reason: 'INVALID_PASSWORD',
  timestamp: new Date().toISOString()
});

// 系统错误
logger.error('数据库连接失败', {
  error: err.message,
  stack: err.stack,
  database: 'users_db',
  timestamp: new Date().toISOString()
});
```


## [规则 4] 用户友好的错误提示 [ENABLED]
# 提供清晰、可操作的错误消息

STATUS: ENABLED
说明：
- 向用户显示：简洁、友好、可操作的消息
- 向开发者记录：详细、技术性、包含堆栈
- 避免技术术语和内部实现细节
- 提供下一步操作建议

后果：
- 技术性错误消息困扰用户
- 模糊消息导致用户无法自助解决

示例：
❌ 错误（技术性消息）：
  "Database query failed: connection timeout at line 42"

✅ 正确（用户友好）：
  "抱歉，服务暂时不可用，请稍后再试。"

❌ 错误（模糊消息）：
  "操作失败"

✅ 正确（可操作）：
  "邮箱格式无效，请输入有效的邮箱地址（例如：user@example.com）"


## [规则 5] Try-Catch 最佳实践 [ENABLED]
# 正确使用异常捕获

STATUS: ENABLED
说明：
- 只捕获可以处理的异常
- 不要捕获后静默忽略（空 catch 块）
- 在合适的层级捕获（控制器、服务边界）
- 捕获后记录日志或重新抛出
- 使用 finally 清理资源

示例：
❌ 错误（静默忽略）：
  try {
    await saveUser(user);
  } catch (err) {
    // 什么都不做
  }

✅ 正确（记录并处理）：
  try {
    await saveUser(user);
  } catch (err) {
    logger.error('保存用户失败', { error: err, userId: user.id });
    throw new SystemError('无法保存用户数据', err);
  }

✅ 正确（资源清理）：
  let connection;
  try {
    connection = await db.connect();
    await connection.query(sql);
  } catch (err) {
    logger.error('数据库操作失败', { error: err });
    throw err;
  } finally {
    if (connection) {
      await connection.close();
    }
  }


## [规则 6] 错误恢复策略 [ENABLED]
# 实施优雅降级和重试机制

STATUS: ENABLED
说明：
- 外部服务失败：重试 + 指数退避
- 非关键功能失败：降级到默认值
- 数据库连接失败：重连 + 断路器
- 设置最大重试次数和超时时间

示例（重试机制）：
```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delayMs: number = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      
      const delay = delayMs * Math.pow(2, i); // 指数退避
      logger.warn(`重试 ${i + 1}/${maxRetries}，等待 ${delay}ms`, { error: err });
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('重试次数已用尽');
}

// 使用
const data = await fetchWithRetry(() => externalApi.getData());
```

示例（降级处理）：
```typescript
async function getRecommendations(userId: string): Promise<Product[]> {
  try {
    return await recommendationService.getPersonalized(userId);
  } catch (err) {
    logger.warn('个性化推荐服务失败，使用默认推荐', { userId, error: err });
    return defaultRecommendations; // 降级到默认值
  }
}
```


## [规则 7] 全局错误处理器 [ENABLED]
# 实施统一的错误处理中间件

STATUS: ENABLED
说明：
- Web 框架：全局错误中间件
- Promise：unhandledRejection 处理器
- 进程：uncaughtException 处理器
- 前端：React Error Boundary、window.onerror

示例（Express 全局错误处理）：
```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // 记录错误
  logger.error('未处理的错误', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    userId: req.user?.id
  });

  // 区分错误类型
  if (err instanceof BusinessError) {
    return res.status(400).json({
      error: err.message,
      code: err.code
    });
  }

  if (err instanceof AuthenticationError) {
    return res.status(401).json({
      error: '认证失败，请重新登录'
    });
  }

  if (err instanceof NotFoundError) {
    return res.status(404).json({
      error: err.message
    });
  }

  // 默认服务器错误
  res.status(500).json({
    error: process.env.NODE_ENV === 'production' 
      ? '服务器内部错误' 
      : err.message
  });
});

// Promise 错误
process.on('unhandledRejection', (reason, promise) => {
  logger.error('未处理的 Promise 拒绝', { reason, promise });
});

// 未捕获异常
process.on('uncaughtException', (err) => {
  logger.fatal('未捕获的异常', { error: err });
  process.exit(1); // 优雅关闭
});
```


## [规则 8] 前端错误边界 [ENABLED]
# React/Vue 错误边界处理

STATUS: ENABLED
LANGUAGE: JavaScript/TypeScript
说明：
- React：使用 Error Boundary 组件
- Vue：使用 errorHandler 钩子
- 显示友好的错误 UI
- 上报错误到监控服务

示例（React Error Boundary）：
```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // 记录错误到监控服务
    logger.error('React 组件错误', {
      error: error.message,
      componentStack: errorInfo.componentStack
    });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>抱歉，出现了一些问题</h2>
          <button onClick={() => window.location.reload()}>刷新页面</button>
        </div>
      );
    }

    return this.props.children;
  }
}

// 使用
<ErrorBoundary>
  <App />
</ErrorBoundary>
```


## [规则 9] 错误监控和告警 [ENABLED]
# 集成错误监控服务

STATUS: ENABLED
说明：
- 集成 Sentry、Datadog、New Relic 等监控服务
- 上报关键错误和异常
- 设置告警阈值
- 包含环境、版本、用户信息

示例（Sentry 集成）：
```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
  tracesSampleRate: 0.1
});

// 捕获异常
try {
  processPayment(order);
} catch (err) {
  Sentry.captureException(err, {
    tags: { feature: 'payment' },
    user: { id: user.id, email: user.email },
    extra: { orderId: order.id, amount: order.total }
  });
  throw err;
}
```


## [规则 10] 错误码标准化 [ENABLED]
# 使用统一的错误代码

STATUS: ENABLED
说明：
- 定义错误码常量或枚举
- 错误码格式：DOMAIN_OPERATION_REASON
- 文档化所有错误码
- 客户端可据错误码采取特定操作

示例：
```typescript
enum ErrorCode {
  // 认证相关
  AUTH_INVALID_CREDENTIALS = 'AUTH_INVALID_CREDENTIALS',
  AUTH_TOKEN_EXPIRED = 'AUTH_TOKEN_EXPIRED',
  AUTH_INSUFFICIENT_PERMISSIONS = 'AUTH_INSUFFICIENT_PERMISSIONS',
  
  // 验证相关
  VALIDATION_REQUIRED_FIELD = 'VALIDATION_REQUIRED_FIELD',
  VALIDATION_INVALID_FORMAT = 'VALIDATION_INVALID_FORMAT',
  VALIDATION_OUT_OF_RANGE = 'VALIDATION_OUT_OF_RANGE',
  
  // 业务相关
  PAYMENT_INSUFFICIENT_BALANCE = 'PAYMENT_INSUFFICIENT_BALANCE',
  PAYMENT_CARD_DECLINED = 'PAYMENT_CARD_DECLINED',
  ORDER_ALREADY_SHIPPED = 'ORDER_ALREADY_SHIPPED'
}

// 错误响应格式
interface ErrorResponse {
  code: ErrorCode;
  message: string;
  field?: string;
  details?: Record<string, any>;
}

// 使用
throw new ValidationError('email', userInput.email, '邮箱格式无效', {
  code: ErrorCode.VALIDATION_INVALID_FORMAT
});
```


## [规则 11] 超时和限流处理 [ENABLED]
# 设置合理的超时和限流

STATUS: ENABLED
说明：
- 所有外部调用设置超时
- API 实施速率限制
- 长时间操作使用异步处理
- 超时后抛出明确的错误

示例：
```typescript
// 请求超时
async function fetchWithTimeout(url: string, timeoutMs: number = 5000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const response = await fetch(url, { signal: controller.signal });
    return response;
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new ExternalServiceError(url, `请求超时（${timeoutMs}ms）`);
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}
```


## [规则 12] 错误文档化 [DISABLED]
# 文档化错误场景和处理方式

STATUS: DISABLED
说明：
- API 文档包含所有可能的错误响应
- 错误码文档和示例
- 故障排查指南


# ============================================
# 项目类型配置
# ============================================

Web 应用：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
- 可选： [规则 12]
- 关键：错误分类、用户友好提示、全局处理、前端边界

CLI 工具：
- 启用： [规则 1, 2, 3, 4, 5, 6, 10, 11]
- 可选： [规则 7, 9, 12]
- 关键：错误分类、日志记录、退出码标准化

库/SDK：
- 启用： [规则 1, 2, 5, 6, 10, 12]
- 可选： [规则 3, 4, 7, 9, 11]
- 关键：自定义错误类、错误码、清晰文档


# ============================================
# 与其他规范的集成
# ============================================

DEPENDENCIES:
  error-handling-spec.txt::RULE 3 -> security-spec.txt::RULE 6
    note: 日志记录遵循安全规范，不记录敏感数据
  error-handling-spec.txt::RULE 7 -> workflow-spec.txt::RULE 12
    note: 全局错误处理对齐工作流规范的错误处理标准


# ============================================
# 摘要 - 启用的规则
# ============================================

✅ [规则 1]  错误分类体系 - 业务/系统/第三方错误
✅ [规则 2]  自定义错误类 - 领域特定错误
✅ [规则 3]  错误日志记录 - 标准化日志级别
✅ [规则 4]  用户友好提示 - 清晰可操作消息
✅ [规则 5]  Try-Catch 最佳实践 - 正确捕获处理
✅ [规则 6]  错误恢复策略 - 重试和降级
✅ [规则 7]  全局错误处理器 - 统一错误中间件
✅ [规则 8]  前端错误边界 - React/Vue 错误处理
✅ [规则 9]  错误监控告警 - Sentry 等集成
✅ [规则 10] 错误码标准化 - 统一错误代码
✅ [规则 11] 超时限流处理 - 防止资源耗尽


# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-10) - 初始错误处理规范，包含 12 条规则
# ============================================
