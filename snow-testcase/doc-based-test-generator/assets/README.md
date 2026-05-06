---
# 测试用例模板说明

## Word模板参考

当用户要求参考特定Word模板时，系统将从`assets/`目录中查找对应的模板文件，并按照模板的格式和结构来组织输出。

## 示例模板

在`assets/`目录下可以存放以下类型的模板：

- `test-case-template.docx`: 标准测试用例模板
- `api-test-template.docx`: API测试专用模板
- `performance-test-template.docx`: 性能测试模板
- `automation-test-template.docx`: 自动化测试用例模板

## 模板使用流程

1. 用户提供模板要求（如"参考XX模板"）
2. 在`assets/`目录中查找对应的模板文件
3. 按照模板的字段和格式生成测试用例
4. 保持与模板的一致性同时满足`references/`中的专业标准

---