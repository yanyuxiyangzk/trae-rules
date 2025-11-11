---
trigger: manual
---

# 测试规范 v1.0
# ============================================
# AI 辅助开发的测试标准和要求
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据项目需求启用/禁用规则
# 3. 在 AI 对话中使用 @testing-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 依赖规范：requirements-spec.txt、naming-conventions.txt、workflow-spec.txt
# 最后更新：2025-11-10
# ============================================

## [规则 1] 测试完整性 [ENABLED]
# 新功能必须包含测试

STATUS: ENABLED
LANGUAGE: All
说明：
- 新功能代码必须包含对应的单元测试
- Bug 修复必须包含回归测试
- 公共 API 变更必须更新集成测试
- 不允许提交未测试的代码到主分支

后果：
- 未测试代码导致生产环境故障风险高
- 回归问题频发，修复成本指数增长

示例：
❌ 错误：
  // 只提交功能代码，没有测试
  function calculateDiscount(price: number): number {
    return price * 0.9;
  }

✅ 正确：
  // 功能代码
  function calculateDiscount(price: number): number {
    return price * 0.9;
  }
  
  // 对应测试
  describe('calculateDiscount', () => {
    it('should apply 10% discount', () => {
      expect(calculateDiscount(100)).toBe(90);
    });
    it('should handle zero price', () => {
      expect(calculateDiscount(0)).toBe(0);
    });
  });


## [规则 2] 测试覆盖率目标 [ENABLED]
# 按项目类型设置覆盖率目标

STATUS: ENABLED
说明：
- Web 应用：最低 70% 行覆盖率，关键路径 90%+
- CLI 工具：最低 80% 行覆盖率
- 库/SDK：最低 85% 行覆盖率，公共 API 100%
- 新增代码覆盖率不得低于现有基线

后果：
- 低覆盖率导致隐藏缺陷进入生产环境
- 重构时缺乏安全网，引入回归风险

配置示例：
```json
// jest.config.js
{
  "coverageThreshold": {
    "global": {
      "branches": 70,
      "functions": 75,
      "lines": 80,
      "statements": 80
    }
  }
}
```


## [规则 3] 测试分层策略 [ENABLED]
# 遵循测试金字塔原则

STATUS: ENABLED
说明：
- 单元测试（70%）：快速、隔离、针对单个函数/类
- 集成测试（20%）：验证模块间交互
- E2E 测试（10%）：关键业务流程端到端验证
- 避免过度依赖 E2E 测试（慢、脆弱、维护成本高）

分层示例：
```
     /\     E2E Tests (10%)
    /  \    Integration Tests (20%)
   /____\   Unit Tests (70%)
```

WHY: 平衡测试速度、覆盖率与维护成本


## [规则 4] Mock 和 Stub 使用规范 [ENABLED]
# 合理使用测试替身

STATUS: ENABLED
说明：
- 外部依赖（API、数据库、文件系统）必须 Mock
- 不要 Mock 被测试的核心逻辑
- 使用真实数据结构，避免过度简化的 Mock
- 集成测试中尽量减少 Mock，使用真实依赖

示例：
✅ 正确（Mock 外部 API）：
  const mockFetch = jest.fn().mockResolvedValue({
    json: () => Promise.resolve({ id: 1, name: 'Test' })
  });
  global.fetch = mockFetch;

❌ 错误（Mock 核心业务逻辑）：
  // 不要 Mock 被测试的计算逻辑本身
  const mockCalculate = jest.fn().mockReturnValue(100);


## [规则 5] 测试命名约定 [ENABLED]
# 清晰、描述性的测试名称

STATUS: ENABLED
LANGUAGE: All
说明：
- 测试文件：与源文件同名 + .test 或 .spec 后缀
- 测试套件：describe('被测试单元名称')
- 测试用例：it('should + 预期行为') 或 test('does something')
- 使用业务语言，不要技术黑话

示例：
✅ 正确：
  describe('UserService', () => {
    describe('createUser', () => {
      it('should create user with valid email', () => {});
      it('should throw ValidationError when email is invalid', () => {});
      it('should hash password before saving', () => {});
    });
  });

❌ 错误：
  describe('tests', () => {
    it('test1', () => {});
    it('works', () => {});
  });


## [规则 6] 测试数据管理 [ENABLED]
# 测试数据应独立、可重复

STATUS: ENABLED
说明：
- 使用工厂函数或 Fixture 生成测试数据
- 每个测试独立准备数据，避免共享状态
- 测试后清理数据（数据库、文件、缓存）
- 使用有意义的测试数据，不要随意字符串

示例：
✅ 正确：
  function createTestUser(overrides = {}) {
    return {
      id: 'test-user-1',
      email: 'test@example.com',
      name: 'Test User',
      ...overrides
    };
  }
  
  it('should update user email', () => {
    const user = createTestUser();
    // 测试逻辑
  });

❌ 错误：
  // 所有测试共享同一个用户对象
  const sharedUser = { id: 1, email: 'a@b.c' };


## [规则 7] 边界条件和异常测试 [ENABLED]
# 测试边界情况和错误路径

STATUS: ENABLED
说明：
- 测试空值、null、undefined
- 测试边界值（0、负数、最大值、最小值）
- 测试异常输入和错误处理路径
- 测试并发和竞态条件（如适用）

后果：
- 忽略边界条件导致生产环境崩溃
- 未测试错误路径使故障恢复失效

示例：
```typescript
describe('divide', () => {
  it('should divide two positive numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });
  it('should throw error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });
  it('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });
});
```


## [规则 8] 测试隔离性 [ENABLED]
# 测试之间互不影响

STATUS: ENABLED
说明：
- 每个测试独立运行，不依赖执行顺序
- 使用 beforeEach/afterEach 清理状态
- 避免修改全局变量或单例
- 并行运行测试时不应失败

WHY: 测试顺序依赖导致间歇性失败，难以调试


## [规则 9] 测试性能要求 [ENABLED]
# 测试应快速执行

STATUS: ENABLED
说明：
- 单元测试：每个 < 100ms
- 集成测试：每个 < 1s
- E2E 测试：每个 < 10s
- 整体测试套件 < 5 分钟
- 慢测试应异步化或并行化

后果：
- 慢测试降低开发效率，开发者跳过测试


## [规则 10] TDD/BDD 实践指南 [DISABLED]
# 测试驱动开发可选实践

STATUS: DISABLED
说明：
- TDD：先写失败测试，再写实现，最后重构
- BDD：使用 Given-When-Then 结构描述行为
- 适用于复杂业务逻辑和公共 API

示例（BDD）：
```typescript
describe('购物车结算', () => {
  it('Given 购物车有商品 When 用户结算 Then 生成订单', () => {
    // Given
    const cart = createCart();
    cart.addItem({ id: '1', price: 100 });
    
    // When
    const order = cart.checkout();
    
    // Then
    expect(order.total).toBe(100);
    expect(order.status).toBe('pending');
  });
});
```


## [规则 11] 集成测试数据库策略 [DISABLED]
# 数据库测试最佳实践

STATUS: DISABLED
说明：
- 使用内存数据库（SQLite、H2）或容器化数据库
- 每个测试使用事务回滚
- 使用迁移脚本初始化 Schema
- 避免依赖生产数据库

WHY: 真实数据库测试提供更高置信度


## [规则 12] 快照测试使用规范 [DISABLED]
# 快照测试适用场景

STATUS: DISABLED
LANGUAGE: JavaScript/TypeScript
说明：
- 适用于 UI 组件、配置文件、序列化输出
- 不适用于随机数据、时间戳
- 定期审查快照，避免盲目更新
- 快照应小且易读

示例：
```typescript
it('should render user profile correctly', () => {
  const profile = render(<UserProfile user={testUser} />);
  expect(profile).toMatchSnapshot();
});
```


# ============================================
# 项目类型配置
# ============================================

Web 应用：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9]
- 可选： [规则 10, 11, 12]
- 覆盖率目标：70% 行覆盖率，关键路径 90%

CLI 工具：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9]
- 可选： [规则 10, 11]
- 覆盖率目标：80% 行覆盖率

库/SDK：
- 启用： [规则 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
- 可选： [规则 11]
- 覆盖率目标：85% 行覆盖率，公共 API 100%


# ============================================
# 与其他规范的集成
# ============================================

DEPENDENCIES:
  testing-spec.txt::RULE 5 -> naming-conventions.txt::CONVENTION 12
    note: 测试命名遵循命名约定规范
  testing-spec.txt::RULE 1 -> workflow-spec.txt::RULE 7
    note: 测试覆盖率要求对齐工作流规范


# ============================================
# 摘要 - 启用的规则
# ============================================

✅ [规则 1]  测试完整性 - 新功能必须包含测试
✅ [规则 2]  测试覆盖率目标 - 按项目类型设置
✅ [规则 3]  测试分层策略 - 遵循测试金字塔
✅ [规则 4]  Mock 和 Stub 使用 - 合理使用测试替身
✅ [规则 5]  测试命名约定 - 清晰描述性名称
✅ [规则 6]  测试数据管理 - 独立可重复
✅ [规则 7]  边界条件测试 - 测试边界和异常
✅ [规则 8]  测试隔离性 - 测试互不影响
✅ [规则 9]  测试性能要求 - 快速执行


# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-10) - 初始测试规范，包含 12 条规则
# ============================================
