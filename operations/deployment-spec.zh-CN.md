---
trigger: manual
---

# 部署规范 v1.0
# ============================================
# AI 辅助开发的部署标准和要求
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据项目需求启用/禁用规则
# 3. 在 AI 对话中使用 @deployment-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 依赖规范：workflow-spec.txt、security-spec.txt、error-handling-spec.txt
# 最后更新：2025-11-10
# ============================================

## [规则 1] 环境分离 [ENABLED]
# 明确区分不同部署环境

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 开发环境（Development）- 开发者本地或共享开发服务器
- 测试环境（Testing/QA）- 质量保证和集成测试
- 预发布环境（Staging）- 生产环境的完整镜像
- 生产环境（Production）- 用户访问的生产系统
- 每个环境独立配置，互不影响

后果：
- 环境混淆导致测试数据污染生产环境
- 配置错误导致安全漏洞或系统故障

配置示例：
```bash
# .env.development
NODE_ENV=development
API_URL=http://localhost:3000
DATABASE_URL=postgresql://localhost/myapp_dev

# .env.staging
NODE_ENV=staging
API_URL=https://staging-api.example.com
DATABASE_URL=postgresql://staging-db.example.com/myapp

# .env.production
NODE_ENV=production
API_URL=https://api.example.com
DATABASE_URL=postgresql://prod-db.example.com/myapp
```


## [规则 2] CI/CD 流水线 [ENABLED]
# 自动化构建、测试和部署

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 代码推送触发自动构建
- 运行所有测试（单元、集成、E2E）
- 执行代码质量检查（lint, 安全扫描）
- 构建 Docker 镜像或部署包
- 自动部署到目标环境
- 部署失败自动回滚

后果：
- 手动部署易出错，增加故障风险
- 缺少自动化测试导致问题进入生产环境

示例（GitHub Actions）：
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
      - name: Run lint
        run: npm run lint
      - name: Security scan
        run: npm audit

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.sha }}
```


## [规则 3] 容器化部署 [ENABLED]
# 使用 Docker 容器化应用

STATUS: ENABLED
说明：
- 使用 Dockerfile 定义应用环境
- 多阶段构建减小镜像体积
- 使用 .dockerignore 排除不必要的文件
- 镜像标签使用语义化版本或 Git SHA
- 使用非 root 用户运行容器

示例（Dockerfile）：
```dockerfile
# 多阶段构建
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 生产镜像
FROM node:18-alpine
WORKDIR /app

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# 复制构建产物
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs package.json ./

# 切换到非 root 用户
USER nodejs

EXPOSE 3000
CMD ["node", "dist/main.js"]
```

.dockerignore:
```
node_modules
npm-debug.log
.git
.env
.vscode
coverage
*.md
```


## [规则 4] 配置管理 [ENABLED]
# 环境变量和配置外部化

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 所有配置通过环境变量注入
- 不在代码中硬编码配置
- 使用配置管理工具（Kubernetes ConfigMap, AWS Secrets Manager）
- 敏感信息加密存储
- 配置变更无需重新构建镜像

后果：
- 硬编码配置导致环境切换困难
- 敏感信息泄露导致安全风险

示例：
```typescript
// config.ts
export const config = {
  port: parseInt(process.env.PORT || '3000'),
  database: {
    url: process.env.DATABASE_URL,
    poolSize: parseInt(process.env.DB_POOL_SIZE || '10')
  },
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT || '6379')
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '1h'
  }
};

// 验证必需的配置
const requiredEnvVars = [
  'DATABASE_URL',
  'JWT_SECRET',
  'REDIS_HOST'
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

Kubernetes ConfigMap:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  PORT: "3000"
  DB_POOL_SIZE: "20"
  REDIS_PORT: "6379"
```


## [规则 5] 健康检查 [ENABLED]
# 实施应用健康检查

STATUS: ENABLED
说明：
- 实现 /health 端点检查应用状态
- 实现 /readiness 端点检查依赖服务
- 检查数据库连接
- 检查外部服务可用性
- 返回详细的健康状态信息

示例：
```typescript
// health.controller.ts
interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  uptime: number;
  checks: {
    database: 'up' | 'down';
    redis: 'up' | 'down';
    [key: string]: 'up' | 'down';
  };
}

app.get('/health', async (req, res) => {
  const health: HealthStatus = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks: {
      database: 'up',
      redis: 'up'
    }
  };

  try {
    // 检查数据库
    await db.ping();
  } catch (err) {
    health.checks.database = 'down';
    health.status = 'unhealthy';
  }

  try {
    // 检查 Redis
    await redis.ping();
  } catch (err) {
    health.checks.redis = 'down';
    health.status = 'unhealthy';
  }

  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});

app.get('/readiness', async (req, res) => {
  // 简化版，只检查应用是否启动
  res.status(200).json({ ready: true });
});
```

Kubernetes 配置：
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /readiness
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5
```


## [规则 6] 日志聚合 [ENABLED]
# 集中化日志管理

STATUS: ENABLED
说明：
- 使用结构化日志（JSON 格式）
- 输出到标准输出/标准错误
- 使用日志聚合工具（ELK, Datadog, CloudWatch）
- 包含请求 ID 追踪
- 设置合理的日志级别

示例：
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'user-service',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console()
  ]
});

// 中间件添加请求 ID
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] || generateId();
  res.setHeader('x-request-id', req.id);
  next();
});

// 使用
logger.info('User logged in', {
  requestId: req.id,
  userId: user.id,
  ip: req.ip
});
```


## [规则 7] 蓝绿部署或金丝雀发布 [DISABLED]
# 零停机部署策略

STATUS: DISABLED
说明：
- **蓝绿部署** - 维护两个相同的生产环境，切换流量
- **金丝雀发布** - 逐步将流量切换到新版本
- **滚动更新** - 逐个替换实例

蓝绿部署示例（Kubernetes）：
```yaml
# 蓝色环境
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: myapp
        version: blue

---
# 绿色环境
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: myapp
        version: green

---
# Service 切换
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: green  # 切换到绿色环境
```

金丝雀发布示例（Istio）：
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp
  http:
    - match:
        - headers:
            canary:
              exact: "true"
      route:
        - destination:
            host: myapp
            subset: v2
    - route:
        - destination:
            host: myapp
            subset: v1
          weight: 90
        - destination:
            host: myapp
            subset: v2
          weight: 10  # 10% 流量到新版本
```


## [规则 8] 回滚机制 [ENABLED]
# 快速回滚到稳定版本

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 保留最近 N 个版本的镜像/部署包
- 实施一键回滚命令
- 回滚后验证健康状态
- 记录回滚操作和原因
- 数据库迁移支持回滚

后果：
- 无回滚机制导致故障恢复时间长
- 数据不兼容导致回滚失败

示例：
```bash
# Kubernetes 回滚
kubectl rollout undo deployment/myapp

# 回滚到特定版本
kubectl rollout undo deployment/myapp --to-revision=2

# 查看回滚历史
kubectl rollout history deployment/myapp

# 检查回滚状态
kubectl rollout status deployment/myapp
```

数据库迁移回滚（Knex.js）：
```typescript
// migrations/20251110_add_user_column.ts
export async function up(knex: Knex): Promise<void> {
  await knex.schema.table('users', (table) => {
    table.string('phone');
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.table('users', (table) => {
    table.dropColumn('phone');
  });
}
```


## [规则 9] 数据库迁移管理 [ENABLED]
# 版本化数据库变更

STATUS: ENABLED
说明：
- 使用迁移工具（Flyway, Liquibase, Knex, TypeORM）
- 迁移脚本版本控制
- 先迁移数据库，再部署应用
- 向后兼容的迁移策略
- 生产环境迁移需备份

示例（TypeORM）：
```typescript
// migration/1699000000000-CreateUserTable.ts
import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class CreateUserTable1699000000000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: 'users',
        columns: [
          {
            name: 'id',
            type: 'uuid',
            isPrimary: true,
            default: 'uuid_generate_v4()'
          },
          {
            name: 'email',
            type: 'varchar',
            isUnique: true
          },
          {
            name: 'created_at',
            type: 'timestamp',
            default: 'now()'
          }
        ]
      })
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('users');
  }
}
```

部署脚本：
```bash
#!/bin/bash
# 备份数据库
pg_dump myapp_production > backup_$(date +%Y%m%d_%H%M%S).sql

# 运行迁移
npm run migration:run

# 检查迁移状态
if [ $? -eq 0 ]; then
  echo "Migration successful"
  # 部署应用
  kubectl apply -f deployment.yaml
else
  echo "Migration failed, rolling back"
  npm run migration:revert
  exit 1
fi
```


## [规则 10] 监控和告警 [ENABLED]
# 应用性能监控

STATUS: ENABLED
说明：
- 监控关键指标（响应时间、错误率、吞吐量）
- 监控资源使用（CPU、内存、磁盘）
- 设置告警阈值
- 集成告警通知（Slack, Email, PagerDuty）
- 使用 APM 工具（New Relic, Datadog, Prometheus）

示例（Prometheus 指标）：
```typescript
import { register, Counter, Histogram } from 'prom-client';

// 请求计数器
const httpRequestCounter = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
});

// 响应时间直方图
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.3, 0.5, 1, 3, 5]
});

// 中间件
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    
    httpRequestCounter.inc({
      method: req.method,
      route: req.route?.path || req.path,
      status: res.statusCode
    });
    
    httpRequestDuration.observe(
      {
        method: req.method,
        route: req.route?.path || req.path
      },
      duration
    );
  });
  
  next();
});

// 暴露指标端点
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

告警规则（Prometheus）：
```yaml
groups:
  - name: app_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} requests/sec"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High response time"
```


## [规则 11] 安全加固 [ENABLED]
# 生产环境安全配置

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 最小权限原则
- 使用非 root 用户运行
- 扫描镜像漏洞
- 更新依赖到安全版本
- 启用网络策略限制访问
- 定期安全审计

后果：
- 安全配置不当导致系统被攻陷
- 容器逃逸导致主机被控制

示例（Kubernetes Security Context）：
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
      containers:
        - name: myapp
          image: myapp:latest
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          resources:
            limits:
              cpu: "1"
              memory: "512Mi"
            requests:
              cpu: "0.5"
              memory: "256Mi"
```


## [规则 12] 部署前检查清单 [ENABLED]
# 上线前验证清单

STATUS: ENABLED
说明：
部署前必须确认：
- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 配置正确（环境变量、ConfigMap）
- [ ] 数据库迁移脚本测试
- [ ] 回滚计划准备
- [ ] 监控和告警配置
- [ ] 性能测试通过
- [ ] 安全扫描无高危漏洞
- [ ] 文档更新
- [ ] 相关团队已通知

部署流程：
```bash
#!/bin/bash
# 部署脚本

echo "1. 运行测试..."
npm test || exit 1

echo "2. 构建镜像..."
docker build -t myapp:${VERSION} . || exit 1

echo "3. 扫描漏洞..."
trivy image myapp:${VERSION} || exit 1

echo "4. 推送镜像..."
docker push myapp:${VERSION} || exit 1

echo "5. 备份数据库..."
./backup-db.sh || exit 1

echo "6. 运行数据库迁移..."
npm run migration:run || exit 1

echo "7. 部署应用..."
kubectl set image deployment/myapp myapp=myapp:${VERSION}

echo "8. 等待部署完成..."
kubectl rollout status deployment/myapp

echo "9. 健康检查..."
./health-check.sh || {
  echo "Health check failed, rolling back..."
  kubectl rollout undo deployment/myapp
  exit 1
}

echo "✅ 部署成功!"
```


# ============================================
# 项目类型配置
# ============================================

Web 应用（生产环境）：
- 启用： [规则 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
- 可选： [规则 7]
- 关键：环境分离、CI/CD、容器化、健康检查、监控告警

微服务：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
- 可选： 无
- 关键：容器化、健康检查、蓝绿部署、监控告警

小型项目：
- 启用： [规则 1, 2, 4, 5, 8, 12]
- 可选： [规则 3, 6, 7, 9, 10, 11]
- 关键：环境分离、CI/CD、配置管理


# ============================================
# 与其他规范的集成
# ============================================

DEPENDENCIES:
  deployment-spec.txt::RULE 4 -> security-spec.txt::RULE 8
    note: 配置管理遵循安全配置规范
  deployment-spec.txt::RULE 6 -> error-handling-spec.txt::RULE 3
    note: 日志聚合遵循日志记录规范
  deployment-spec.txt::RULE 2 -> workflow-spec.txt::RULE 8
    note: CI/CD 流水线集成部署前检查清单


# ============================================
# 摘要 - 启用的规则
# ============================================

✅ [规则 1]  环境分离 - Dev/Staging/Production
✅ [规则 2]  CI/CD 流水线 - 自动化部署
✅ [规则 3]  容器化部署 - Docker多阶段构建
✅ [规则 4]  配置管理 - 环境变量外部化
✅ [规则 5]  健康检查 - /health 和 /readiness
✅ [规则 6]  日志聚合 - 结构化日志
✅ [规则 8]  回滚机制 - 快速回滚
✅ [规则 9]  数据库迁移 - 版本化变更
✅ [规则 10] 监控告警 - Prometheus/Datadog
✅ [规则 11] 安全加固 - 最小权限原则
✅ [规则 12] 部署清单 - 上线前验证


# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-10) - 初始部署规范，包含 12 条规则
# ============================================
