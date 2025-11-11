#!/usr/bin/env python3
"""
Spec Lint - 规范检查工具
检查代码是否符合 spec-presets 中启用的规范

使用方法:
    python spec-lint.py [目录路径]
    python spec-lint.py --spec-dir ../spec-presets/core --target-dir ./src

遵循规范:
- requirements-spec.zh-CN.txt
- naming-conventions.zh-CN.txt
- error-handling-spec.zh-CN.txt
- testing-spec.zh-CN.txt
- security-spec.zh-CN.txt
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass


@dataclass
class LintIssue:
    """Lint 检查问题"""
    file_path: str
    line_number: int
    rule: str
    severity: str  # ERROR, WARNING, INFO
    message: str


class SpecLinter:
    """规范检查器"""
    
    def __init__(self, spec_dir: Path, target_dir: Path):
        self.spec_dir = spec_dir
        self.target_dir = target_dir
        self.issues: List[LintIssue] = []
        self.enabled_rules = self._load_enabled_rules()
    
    def _load_enabled_rules(self) -> Dict[str, Set[str]]:
        """加载启用的规则"""
        enabled = {}
        
        spec_files = [
            'requirements-spec.zh-CN.txt',
            'naming-conventions.zh-CN.txt',
            'error-handling-spec.zh-CN.txt',
            'testing-spec.zh-CN.txt',
            'security-spec.zh-CN.txt'
        ]
        
        for spec_file in spec_files:
            spec_path = self.spec_dir / spec_file
            if spec_path.exists():
                enabled[spec_file] = self._parse_enabled_rules(spec_path)
        
        return enabled
    
    def _parse_enabled_rules(self, spec_path: Path) -> Set[str]:
        """解析启用的规则"""
        enabled = set()
        
        with open(spec_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 匹配 [规则 N] 或 [约定 N] [ENABLED]
            pattern = r'\[(?:规则|约定)\s+(\d+)\].*?\[ENABLED\]'
            matches = re.finditer(pattern, content, re.MULTILINE)
            
            for match in matches:
                rule_num = match.group(1)
                enabled.add(f"RULE_{rule_num}")
        
        return enabled
    
    def check_naming_conventions(self, file_path: Path):
        """检查命名约定"""
        if file_path.suffix not in ['.ts', '.tsx', '.js', '.jsx', '.py']:
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        is_python = file_path.suffix == '.py'
        
        for i, line in enumerate(lines, 1):
            # 检查变量命名 (CONVENTION 1)
            if 'RULE_1' in self.enabled_rules.get('naming-conventions.zh-CN.txt', set()):
                # Python: snake_case, JS/TS: camelCase
                if is_python:
                    # 检查是否有驼峰命名的变量
                    var_pattern = r'\b([a-z]+[A-Z][a-zA-Z]*)\s*='
                    if re.search(var_pattern, line):
                        self.issues.append(LintIssue(
                            file_path=str(file_path),
                            line_number=i,
                            rule='naming-conventions CONVENTION 1',
                            severity='WARNING',
                            message='Python 应使用 snake_case 命名变量'
                        ))
    
    def check_security(self, file_path: Path):
        """检查安全问题"""
        if file_path.suffix not in ['.ts', '.tsx', '.js', '.jsx', '.py']:
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # 检查硬编码密钥 (RULE 8)
        if 'RULE_8' in self.enabled_rules.get('security-spec.zh-CN.txt', set()):
            suspicious_patterns = [
                (r'API_KEY\s*=\s*["\'][^"\']+["\']', '可能硬编码了 API 密钥'),
                (r'SECRET\s*=\s*["\'][^"\']+["\']', '可能硬编码了密钥'),
                (r'PASSWORD\s*=\s*["\'][^"\']+["\']', '可能硬编码了密码'),
                (r'TOKEN\s*=\s*["\'][^"\']+["\']', '可能硬编码了令牌'),
            ]
            
            for i, line in enumerate(lines, 1):
                for pattern, message in suspicious_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # 排除 process.env 的使用
                        if 'process.env' not in line and 'os.getenv' not in line:
                            self.issues.append(LintIssue(
                                file_path=str(file_path),
                                line_number=i,
                                rule='security-spec RULE 8',
                                severity='ERROR',
                                message=message
                            ))
    
    def check_error_handling(self, file_path: Path):
        """检查错误处理"""
        if file_path.suffix not in ['.ts', '.tsx', '.js', '.jsx', '.py']:
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # 检查空 catch 块 (RULE 5)
        if 'RULE_5' in self.enabled_rules.get('error-handling-spec.zh-CN.txt', set()):
            # 简单检测空 catch 块
            catch_pattern = r'catch\s*\([^)]*\)\s*\{\s*\}'
            if re.search(catch_pattern, content):
                self.issues.append(LintIssue(
                    file_path=str(file_path),
                    line_number=0,
                    rule='error-handling-spec RULE 5',
                    severity='ERROR',
                    message='检测到空 catch 块，应记录错误或重新抛出'
                ))
    
    def check_completeness(self, file_path: Path):
        """检查代码完整性"""
        if file_path.suffix not in ['.ts', '.tsx', '.js', '.jsx', '.py']:
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 检查 TODO/FIXME (RULE 1)
        if 'RULE_1' in self.enabled_rules.get('requirements-spec.zh-CN.txt', set()):
            for i, line in enumerate(lines, 1):
                if re.search(r'(TODO|FIXME|XXX|HACK):', line, re.IGNORECASE):
                    self.issues.append(LintIssue(
                        file_path=str(file_path),
                        line_number=i,
                        rule='requirements-spec RULE 1',
                        severity='WARNING',
                        message='代码包含 TODO/FIXME，应在提交前完成'
                    ))
    
    def lint_file(self, file_path: Path):
        """检查单个文件"""
        self.check_naming_conventions(file_path)
        self.check_security(file_path)
        self.check_error_handling(file_path)
        self.check_completeness(file_path)
    
    def lint_directory(self):
        """检查整个目录"""
        extensions = {'.ts', '.tsx', '.js', '.jsx', '.py'}
        
        for file_path in self.target_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                # 跳过 node_modules, dist, build 等目录
                if any(part in file_path.parts for part in ['node_modules', 'dist', 'build', '__pycache__', '.venv']):
                    continue
                
                self.lint_file(file_path)
    
    def report(self) -> int:
        """输出报告并返回退出码"""
        if not self.issues:
            print("✅ 所有检查通过！未发现问题。")
            return 0
        
        # 按严重程度分组
        errors = [i for i in self.issues if i.severity == 'ERROR']
        warnings = [i for i in self.issues if i.severity == 'WARNING']
        
        print(f"\n发现 {len(self.issues)} 个问题:")
        print(f"  ❌ 错误: {len(errors)}")
        print(f"  ⚠️  警告: {len(warnings)}\n")
        
        # 按文件分组输出
        issues_by_file: Dict[str, List[LintIssue]] = {}
        for issue in self.issues:
            if issue.file_path not in issues_by_file:
                issues_by_file[issue.file_path] = []
            issues_by_file[issue.file_path].append(issue)
        
        for file_path, file_issues in sorted(issues_by_file.items()):
            print(f"\n📄 {file_path}")
            for issue in file_issues:
                icon = "❌" if issue.severity == "ERROR" else "⚠️"
                line_info = f"L{issue.line_number}" if issue.line_number > 0 else ""
                print(f"  {icon} {line_info} [{issue.rule}] {issue.message}")
        
        return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(
        description='规范检查工具 - 检查代码是否符合 spec-presets 规范'
    )
    parser.add_argument(
        '--spec-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'core',
        help='规范文件目录 (默认: ../core)'
    )
    parser.add_argument(
        '--target-dir',
        type=Path,
        default=Path.cwd(),
        help='要检查的目标目录 (默认: 当前目录)'
    )
    
    args = parser.parse_args()
    
    if not args.spec_dir.exists():
        print(f"❌ 错误: 规范目录不存在: {args.spec_dir}", file=sys.stderr)
        return 1
    
    if not args.target_dir.exists():
        print(f"❌ 错误: 目标目录不存在: {args.target_dir}", file=sys.stderr)
        return 1
    
    print(f"🔍 检查目录: {args.target_dir}")
    print(f"📋 规范目录: {args.spec_dir}\n")
    
    linter = SpecLinter(args.spec_dir, args.target_dir)
    linter.lint_directory()
    
    return linter.report()


if __name__ == '__main__':
    sys.exit(main())
