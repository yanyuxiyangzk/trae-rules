---
trigger: manual
---

# 安全规范 v1.0
# ============================================
# AI 辅助开发的安全标准和要求
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据项目需求启用/禁用规则
# 3. 在 AI 对话中使用 @security-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 依赖规范：requirements-spec.txt、error-handling-spec.txt、workflow-spec.txt
# 最后更新：2025-11-10
# ============================================

## [规则 1] 输入验证与清理 [ENABLED]
# 所有外部输入必须验证和清理

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 验证所有用户输入、API 参数、文件上传
- 使用白名单验证，不要黑名单
- 清理 HTML/SQL/命令注入风险字符
- 验证数据类型、长度、格式、范围

后果：
- 未验证输入导致 SQL 注入、XSS、命令注入
- 数据泄露、系统被攻陷、法律责任

示例：
❌ 错误（SQL 注入风险）：
  const query = `SELECT * FROM users WHERE email = '${userEmail}'`;
  db.execute(query);

✅ 正确（参数化查询）：
  const query = 'SELECT * FROM users WHERE email = ?';
  db.execute(query, [userEmail]);

❌ 错误（XSS 风险）：
  element.innerHTML = userInput;

✅ 正确（转义输出）：
  element.textContent = userInput;
  // 或使用框架的安全 API
  element.innerHTML = DOMPurify.sanitize(userInput);


## [规则 2] 认证与授权 [ENABLED]
# 实施强认证和细粒度授权

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 使用成熟的认证库（Passport.js、Spring Security）
- 密码至少 8 位，强制复杂度要求
- 实施多因素认证（MFA）用于敏感操作
- 授权检查在服务端，不依赖客户端
- 遵循最小权限原则

后果：
- 弱认证导致账户被盗、数据泄露
- 缺少授权检查导致越权访问

示例：
✅ 正确（服务端权限检查）：
  async function deleteUser(req, res) {
    const { userId } = req.params;
    const currentUser = req.user;
    
    // 验证权限
    if (!currentUser.isAdmin && currentUser.id !== userId) {
      throw new ForbiddenError('无权删除其他用户');
    }
    
    await userService.delete(userId);
    res.status(204).send();
  }

❌ 错误（仅客户端检查）：
  // 前端隐藏删除按钮，但后端未验证权限
  if (user.isAdmin) {
    showDeleteButton();
  }


## [规则 3] 敏感数据保护 [ENABLED]
# 加密存储和传输敏感数据

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 密码使用 bcrypt/Argon2 单向哈希，加盐
- 敏感数据（信用卡、身份证）加密存储
- 使用 HTTPS/TLS 传输敏感数据
- 不在日志、错误消息、URL 中暴露敏感数据
- 定期轮换密钥和令牌

后果：
- 明文存储密码导致大规模账户泄露
- 传输未加密导致中间人攻击

示例：
✅ 正确（密码哈希）：
  import bcrypt from 'bcrypt';
  
  async function hashPassword(plainPassword: string): Promise<string> {
    const saltRounds = 12;
    return bcrypt.hash(plainPassword, saltRounds);
  }
  
  async function verifyPassword(plain: string, hashed: string): Promise<boolean> {
    return bcrypt.compare(plain, hashed);
  }

❌ 错误（明文存储）：
  const user = {
    email: 'user@example.com',
    password: '12345678' // 绝不明文存储
  };


## [规则 4] 依赖安全管理 [ENABLED]
# 审计和更新第三方依赖

STATUS: ENABLED
说明：
- 定期运行安全扫描（npm audit、Snyk）
- 不使用已知漏洞的依赖版本
- 固定依赖版本，避免自动更新引入漏洞
- 最小化依赖数量，减少攻击面
- 订阅安全公告

后果：
- 依赖漏洞被利用导致系统被攻陷
- 供应链攻击（依赖包被投毒）

命令示例：
```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
safety check

# 自动化
npm install -g snyk
snyk test
```


## [规则 5] OWASP Top 10 防护 [ENABLED]
# 防护常见 Web 安全漏洞

STATUS: ENABLED
说明：
遵循 OWASP Top 10 最佳实践：
1. Broken Access Control - 访问控制失效
2. Cryptographic Failures - 加密失败
3. Injection - 注入攻击
4. Insecure Design - 不安全设计
5. Security Misconfiguration - 安全配置错误
6. Vulnerable Components - 易受攻击的组件
7. Authentication Failures - 认证失败
8. Data Integrity Failures - 数据完整性失败
9. Logging Failures - 日志记录失败
10. SSRF - 服务端请求伪造

关键防护措施：
- 使用 CSP (Content Security Policy) 头
- 启用 CORS 策略
- 设置安全的 Cookie 属性（HttpOnly, Secure, SameSite）
- 防止点击劫持（X-Frame-Options）


## [规则 6] 日志安全 [ENABLED]
# 安全记录日志，不泄露敏感信息

STATUS: ENABLED
说明：
- 日志中禁止记录：密码、令牌、密钥、信用卡号、身份证
- 记录安全事件：登录失败、权限拒绝、异常访问
- 日志文件权限受限，只有授权人员可访问
- 定期归档和清理旧日志

后果：
- 日志泄露导致凭证被盗
- 缺少安全日志无法追溯攻击

示例：
❌ 错误（泄露密码）：
  logger.info(`用户登录: ${email}, 密码: ${password}`);

✅ 正确（安全日志）：
  logger.info(`用户登录成功: ${email}`);
  logger.warn(`登录失败: ${email}, IP: ${req.ip}`);


## [规则 7] API 安全 [ENABLED]
# 保护 API 端点安全

STATUS: ENABLED
说明：
- 实施速率限制（Rate Limiting）防止暴力破解
- 使用 API 密钥或 JWT 令牌认证
- 验证 Content-Type 防止 MIME 混淆
- 限制请求大小防止 DoS 攻击
- 实施 CORS 策略，限制跨域访问

示例（速率限制）：
```javascript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 5, // 最多 5 次尝试
  message: '登录尝试次数过多，请 15 分钟后再试'
});

app.post('/api/login', loginLimiter, handleLogin);
```


## [规则 8] 安全配置管理 [ENABLED]
# 安全管理配置和密钥

STATUS: ENABLED
说明：
- 不在代码中硬编码密钥、密码、API 令牌
- 使用环境变量或密钥管理服务（AWS Secrets Manager、HashiCorp Vault）
- 不提交 .env 文件到版本控制
- 生产环境关闭调试模式和详细错误信息
- 定期轮换密钥

后果：
- 硬编码密钥泄露导致系统被攻陷
- 调试信息暴露内部实现细节

示例：
❌ 错误（硬编码密钥）：
  const API_KEY = 'sk-1234567890abcdef';
  const DB_PASSWORD = 'password123';

✅ 正确（环境变量）：
  const API_KEY = process.env.API_KEY;
  const DB_PASSWORD = process.env.DB_PASSWORD;
  
  // .env（不提交到 Git）
  API_KEY=sk-1234567890abcdef
  DB_PASSWORD=password123
  
  // .gitignore
  .env
  .env.local


## [规则 9] 会话管理安全 [ENABLED]
# 安全管理用户会话

STATUS: ENABLED
说明：
- 会话 ID 随机生成，不可预测
- 登录后重新生成会话 ID
- 设置会话超时（空闲 30 分钟，绝对 24 小时）
- 注销时销毁会话
- Cookie 设置 HttpOnly、Secure、SameSite 属性

示例：
```javascript
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,    // 防止 XSS 读取
    secure: true,      // 仅 HTTPS 传输
    sameSite: 'strict', // 防止 CSRF
    maxAge: 30 * 60 * 1000 // 30 分钟
  }
}));
```


## [规则 10] 文件上传安全 [ENABLED]
# 安全处理文件上传

STATUS: ENABLED
说明：
- 验证文件类型（MIME type 和扩展名双重验证）
- 限制文件大小
- 扫描病毒和恶意代码
- 存储在非 Web 目录或使用对象存储
- 随机重命名文件，不使用原始文件名

后果：
- 恶意文件上传导致代码执行、XSS
- 大文件上传导致 DoS 攻击

示例：
```javascript
import multer from 'multer';
import path from 'path';

const storage = multer.diskStorage({
  destination: '/uploads/',
  filename: (req, file, cb) => {
    // 随机文件名
    const uniqueName = `${Date.now()}-${Math.random().toString(36)}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!allowed.includes(file.mimetype)) {
      return cb(new Error('不允许的文件类型'));
    }
    cb(null, true);
  }
});
```


## [规则 11] 错误处理安全 [ENABLED]
# 安全处理错误，不暴露敏感信息

STATUS: ENABLED
说明：
- 生产环境返回通用错误消息
- 不暴露堆栈跟踪、数据库架构、内部路径
- 详细错误仅记录到服务端日志
- 实施全局错误处理器

示例：
✅ 正确（生产环境）：
  app.use((err, req, res, next) => {
    logger.error('错误详情', { error: err.stack, user: req.user });
    
    if (process.env.NODE_ENV === 'production') {
      res.status(500).json({ error: '服务器内部错误' });
    } else {
      res.status(500).json({ error: err.message, stack: err.stack });
    }
  });


## [规则 12] 安全开发生命周期 [DISABLED]
# 将安全集成到开发流程

STATUS: DISABLED
说明：
- 设计阶段进行威胁建模
- 代码审查关注安全问题
- 自动化安全扫描集成到 CI/CD
- 定期进行渗透测试
- 建立安全响应流程


# ============================================
# 项目类型配置
# ============================================

Web 应用：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
- 可选： [规则 12]
- 关键：输入验证、认证授权、敏感数据保护、OWASP 防护

CLI 工具：
- 启用： [规则 1, 3, 4, 6, 8, 11]
- 可选： [规则 2, 5, 7, 9, 10, 12]
- 关键：输入验证、配置安全、依赖安全

库/SDK：
- 启用： [规则 1, 3, 4, 6, 8, 11]
- 可选： [规则 2, 5, 7, 9, 10, 12]
- 关键：输入验证、API 安全、依赖安全


# ============================================
# 与其他规范的集成
# ============================================

DEPENDENCIES:
  security-spec.txt::RULE 11 -> error-handling-spec.txt::RULE 3
    note: 安全错误处理遵循错误处理规范
  security-spec.txt::RULE 4 -> workflow-spec.txt::RULE 10
    note: 依赖安全审计对齐依赖更新策略


# ============================================
# 摘要 - 启用的规则
# ============================================

✅ [规则 1]  输入验证与清理 - 防止注入攻击
✅ [规则 2]  认证与授权 - 强认证细粒度授权
✅ [规则 3]  敏感数据保护 - 加密存储和传输
✅ [规则 4]  依赖安全管理 - 审计更新依赖
✅ [规则 5]  OWASP Top 10 防护 - 防护常见漏洞
✅ [规则 6]  日志安全 - 不泄露敏感信息
✅ [规则 7]  API 安全 - 速率限制和认证
✅ [规则 8]  安全配置管理 - 不硬编码密钥
✅ [规则 9]  会话管理安全 - 安全会话配置
✅ [规则 10] 文件上传安全 - 验证和隔离
✅ [规则 11] 错误处理安全 - 不暴露内部信息


# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-10) - 初始安全规范，包含 12 条规则
# ============================================
