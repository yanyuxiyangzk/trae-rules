#!/usr/bin/env node
/**
 * Spec Report - 规范遵守情况报告生成器
 * 生成项目遵守 spec-presets 规范的详细报告
 * 
 * 使用方法:
 *   node spec-report.js
 *   node spec-report.js --spec-dir ../spec-presets/core --target-dir ./src --output report.json
 */

const fs = require('fs');
const path = require('path');

class SpecReporter {
  constructor(specDir, targetDir, outputPath) {
    this.specDir = specDir;
    this.targetDir = targetDir;
    this.outputPath = outputPath;
    this.report = {
      timestamp: new Date().toISOString(),
      specDir,
      targetDir,
      specs: {},
      summary: {
        totalRules: 0,
        enabledRules: 0,
        complianceRate: 0,
        issues: []
      }
    };
  }

  /**
   * 解析规范文件
   */
  parseSpecFile(specPath) {
    const content = fs.readFileSync(specPath, 'utf-8');
    const rules = [];
    
    // 匹配规则或约定
    const rulePattern = /##\s*\[(?:规则|约定)\s+(\d+)\]\s+([^\[]+)\s+\[(ENABLED|DISABLED)\]/g;
    let match;
    
    while ((match = rulePattern.exec(content)) !== null) {
      const [, number, title, status] = match;
      rules.push({
        number: parseInt(number),
        title: title.trim(),
        enabled: status === 'ENABLED'
      });
    }
    
    return rules;
  }

  /**
   * 扫描代码文件
   */
  scanCodeFiles() {
    const stats = {
      totalFiles: 0,
      totalLines: 0,
      filesByType: {}
    };

    const scanDir = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          // 跳过常见的非代码目录
          if (['node_modules', 'dist', 'build', '__pycache__', '.venv', '.git'].includes(entry.name)) {
            continue;
          }
          scanDir(fullPath);
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name);
          if (['.ts', '.tsx', '.js', '.jsx', '.py'].includes(ext)) {
            stats.totalFiles++;
            
            // 统计行数
            const content = fs.readFileSync(fullPath, 'utf-8');
            const lines = content.split('\n').length;
            stats.totalLines += lines;
            
            // 按类型统计
            if (!stats.filesByType[ext]) {
              stats.filesByType[ext] = { count: 0, lines: 0 };
            }
            stats.filesByType[ext].count++;
            stats.filesByType[ext].lines += lines;
          }
        }
      }
    };

    if (fs.existsSync(this.targetDir)) {
      scanDir(this.targetDir);
    }

    return stats;
  }

  /**
   * 检查测试覆盖率
   */
  checkTestCoverage() {
    const coveragePath = path.join(this.targetDir, '..', 'coverage', 'coverage-summary.json');
    
    if (fs.existsSync(coveragePath)) {
      try {
        const coverage = JSON.parse(fs.readFileSync(coveragePath, 'utf-8'));
        const total = coverage.total;
        
        return {
          lines: total.lines.pct,
          statements: total.statements.pct,
          functions: total.functions.pct,
          branches: total.branches.pct
        };
      } catch (err) {
        return null;
      }
    }
    
    return null;
  }

  /**
   * 生成报告
   */
  async generate() {
    console.log('🔍 扫描规范文件...');
    
    // 读取所有规范文件
    const specFiles = [
      'requirements-spec.zh-CN.txt',
      'naming-conventions.zh-CN.txt',
      'error-handling-spec.zh-CN.txt',
      'testing-spec.zh-CN.txt',
      'security-spec.zh-CN.txt'
    ];

    for (const specFile of specFiles) {
      const specPath = path.join(this.specDir, specFile);
      
      if (fs.existsSync(specPath)) {
        const rules = this.parseSpecFile(specPath);
        const enabledCount = rules.filter(r => r.enabled).length;
        
        this.report.specs[specFile] = {
          totalRules: rules.length,
          enabledRules: enabledCount,
          rules
        };
        
        this.report.summary.totalRules += rules.length;
        this.report.summary.enabledRules += enabledCount;
      }
    }

    console.log('📊 扫描代码文件...');
    this.report.codeStats = this.scanCodeFiles();

    console.log('🧪 检查测试覆盖率...');
    this.report.testCoverage = this.checkTestCoverage();

    // 计算合规率（简化版本）
    if (this.report.summary.totalRules > 0) {
      this.report.summary.complianceRate = Math.round(
        (this.report.summary.enabledRules / this.report.summary.totalRules) * 100
      );
    }

    // 输出报告
    this.printReport();

    // 保存 JSON 报告
    if (this.outputPath) {
      fs.writeFileSync(this.outputPath, JSON.stringify(this.report, null, 2));
      console.log(`\n📄 报告已保存至: ${this.outputPath}`);
    }
  }

  /**
   * 打印报告到控制台
   */
  printReport() {
    console.log('\n' + '='.repeat(60));
    console.log('📋 规范遵守情况报告');
    console.log('='.repeat(60));

    console.log(`\n📅 生成时间: ${this.report.timestamp}`);
    console.log(`📁 目标目录: ${this.targetDir}`);

    console.log('\n📊 代码统计:');
    console.log(`  总文件数: ${this.report.codeStats.totalFiles}`);
    console.log(`  总行数: ${this.report.codeStats.totalLines}`);
    console.log('  文件类型分布:');
    for (const [ext, stats] of Object.entries(this.report.codeStats.filesByType)) {
      console.log(`    ${ext}: ${stats.count} 个文件, ${stats.lines} 行`);
    }

    if (this.report.testCoverage) {
      console.log('\n🧪 测试覆盖率:');
      console.log(`  行覆盖率: ${this.report.testCoverage.lines.toFixed(2)}%`);
      console.log(`  语句覆盖率: ${this.report.testCoverage.statements.toFixed(2)}%`);
      console.log(`  函数覆盖率: ${this.report.testCoverage.functions.toFixed(2)}%`);
      console.log(`  分支覆盖率: ${this.report.testCoverage.branches.toFixed(2)}%`);
    }

    console.log('\n📋 规范启用情况:');
    for (const [specFile, data] of Object.entries(this.report.specs)) {
      const specName = specFile.replace('.zh-CN.txt', '').replace(/-/g, ' ');
      console.log(`\n  ${specName}:`);
      console.log(`    总规则数: ${data.totalRules}`);
      console.log(`    已启用: ${data.enabledRules}`);
      console.log(`    启用率: ${Math.round((data.enabledRules / data.totalRules) * 100)}%`);
      
      const enabledRules = data.rules.filter(r => r.enabled);
      if (enabledRules.length > 0) {
        console.log('    已启用的规则:');
        enabledRules.forEach(rule => {
          console.log(`      ✅ [${rule.number}] ${rule.title}`);
        });
      }
    }

    console.log('\n' + '='.repeat(60));
    console.log(`总体合规率: ${this.report.summary.complianceRate}%`);
    console.log(`已启用规则: ${this.report.summary.enabledRules}/${this.report.summary.totalRules}`);
    console.log('='.repeat(60) + '\n');
  }
}

// CLI
function main() {
  const args = process.argv.slice(2);
  const options = {
    specDir: path.join(__dirname, '..', 'core'),
    targetDir: process.cwd(),
    outputPath: null
  };

  // 简单参数解析
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--spec-dir' && args[i + 1]) {
      options.specDir = args[i + 1];
      i++;
    } else if (args[i] === '--target-dir' && args[i + 1]) {
      options.targetDir = args[i + 1];
      i++;
    } else if (args[i] === '--output' && args[i + 1]) {
      options.outputPath = args[i + 1];
      i++;
    }
  }

  const reporter = new SpecReporter(
    options.specDir,
    options.targetDir,
    options.outputPath
  );

  reporter.generate().catch(err => {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  });
}

if (require.main === module) {
  main();
}

module.exports = { SpecReporter };
