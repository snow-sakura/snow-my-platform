# 基于文档的测试用例生成技能 (doc-based-test-generator)

## 简介
这是一个专门用于根据需求文档自动生成标准化测试用例的技能。该技能可以根据不同的测试需求，智能识别测试类型，并按照相应的企业级测试规范生成结构清晰的测试用例。

## 功能特性
- 自动识别测试类型（功能、API、自动化、性能测试）
- 遵循标准化的测试用例编写规范
- 生成结构化的Markdown格式测试用例
- 支持导出为多种格式（如Excel）

## 目录结构
```
doc-based-test-generator/
├── SKILL.md                # 技能总说明文档
├── README.md               # 当前文件，使用说明
├── references/             # 各类测试规范文档
│   ├── functional-testing-standard.md     # 功能测试规范
│   ├── api-testing-standard.md           # API测试规范
│   ├── automation-testing-standard.md    # 自动化测试规范
│   └── performance-testing-standard.md   # 性能测试规范
└── scripts/                # 辅助脚本
    └── export-to-excel.sh  # 导出到Excel的脚本
```

## 使用方法
1. 提供测试需求或功能描述
2. 该技能会自动识别测试类型
3. 根据对应的规范文档生成测试用例
4. 输出标准化的Markdown格式测试用例

## 支持的测试类型

### 功能测试 (Functional Testing)
- 验证系统功能是否符合需求规格
- 遵循 `references/functional-testing-standard.md` 规范
- 生成符合标准的功能测试用例

### API测试 (API Testing)
- 验证API接口的正确性和性能
- 遵循 `references/api-testing-standard.md` 规范
- 生成包含请求/响应详情的API测试用例

### 自动化测试 (Automation Testing)
- 为自动化测试框架生成测试脚本
- 遵循 `references/automation-testing-standard.md` 规范
- 生成适合自动化执行的测试用例

### 性能测试 (Performance Testing)
- 验证系统在各种负载下的性能表现
- 遵循 `references/performance-testing-standard.md` 规范
- 生成包含性能指标的测试用例

## 扩展功能
- 通过 `scripts/export-to-excel.sh` 可将测试用例导出为Excel格式
- 支持自定义测试规范（在references目录下添加新的规范文档）

## 贡献
如果您需要添加新的测试类型或修改现有规范，请更新相应的文档文件并提交PR。