# 功能开发进度追踪

> 本文档用于追踪所有功能模块的开发状态，后续所有更新、迭代、迁移等变更均需同步记录到本文档中。

---

## 状态说明

- [x] 已完成（前后端打通，可正常使用）
- [~] 部分完成（后端/前端有一方未完成，或核心流程通但边缘功能缺失）
- [ ] 未完成（尚未开发或仅预留接口）

---

## 一、项目管理

| 功能 | 状态 | 备注 |
|------|------|------|
| 项目列表展示 | [x] | ProjectList.vue 已完成，展示文档/测试点/用例统计 |
| 新建项目 | [x] | 前后端打通，含表单校验 |
| 删除项目 | [x] | 前后端打通，含二次确认 |
| 编辑项目 | [x] | 后端 API 已完成（PUT /projects/{id}），前端 Edit 对话框已接入 API |
| 项目详情页 Tab 切换 | [x] | ProjectDetail.vue 已完成，含文档/测试点/知识库/测试用例四个 Tab |

---

## 二、文档管理

| 功能 | 状态 | 备注 |
|------|------|------|
| 多格式文档上传 | [x] | 支持 PDF/DOCX/MD/YAML/CSV，前后端打通 |
| 文档列表展示 | [x] | 展示文件名、类型、上传时间 |
| 文档解析 | [x] | DocumentParser 支持 PDF/DOCX/MD/YAML/CSV，解析后文本存入数据库 |
| 查看文档内容 | [x] | 后端新增 GET /projects/{id}/documents/{doc_id}，前端弹窗展示文档内容 |
| 重新解析文档 | [ ] | Documents.vue 显示"重新解析功能开发中" |
| 删除文档 | [x] | 后端新增 DELETE /projects/{id}/documents/{doc_id}，前端已接入 |
| 文档大小显示 | [~] | 已改为显示上传时间，大小字段在后端未采集文件元信息 |

---

## 三、测试点管理

| 功能 | 状态 | 备注 |
|------|------|------|
| AI 自动提取测试点 | [x] | 核心流程已通：选择文档 → 后台异步提取 → 保存到 TestPoint 表 |
| 测试点列表展示 | [x] | 展示标题、描述、优先级、分类、校验状态、用例数 |
| 手动新增测试点 | [x] | 后端新增 POST /test-points/，前端已接入编辑/创建对话框 |
| 编辑测试点 | [x] | 后端 API 已完成（PUT /test-points/{id}），前端编辑对话框已接入 API |
| 删除测试点 | [x] | 后端 API 已完成，前端已接入实际 API 调用 |
| 批量删除测试点 | [x] | 后端 API 已完成，前端批量删除已接入 API |
| 测试点校验/确认 | [x] | 前端新增"确认"按钮，调用 updateTestPoint 设置 is_verified=true |
| 测试点筛选 | [x] | 前端已实现 computed 过滤（按优先级/分类），下拉框绑定实际值 |
| 关联知识库提取 | [x] | 前端知识库选择框已改为动态加载；后端已实际查询 ChromaDB |

---

## 四、测试用例管理

| 功能 | 状态 | 备注 |
|------|------|------|
| AI 自动生成测试用例 | [x] | 核心流程已通：选择测试点 → 后台异步生成 → 保存到 TestCase 表，含 case_number 编号 |
| 测试用例列表展示 | [x] | 展示用例编号、标题、前置条件、优先级、类型 |
| 手动新增测试用例 | [x] | 后端新增 POST /test-cases/，前端创建/编辑对话框已接入 API |
| 编辑测试用例 | [x] | 后端 API 已完成（PUT /test-cases/{id}），前端编辑对话框已接入 |
| 删除测试用例 | [x] | 后端 API 已完成，前端已接入实际 API 调用 |
| 批量删除测试用例 | [x] | 后端 API 已完成，前端批量删除已接入 |
| 查看测试用例详情 | [x] | 前端详情弹窗展示完整步骤和预期结果 |
| 测试用例导出 Excel | [x] | 后端接口和 ExcelExporter 均已完成，前端已接入下载 |
| 测试用例再生成 | [ ] | 无独立接口和 UI |
| 用例筛选 | [x] | 前端已实现 computed 过滤（按优先级/类型） |

---

## 五、RAG 知识库管理

| 功能 | 状态 | 备注 |
|------|------|------|
| 创建知识库 | [x] | 后端 API 已完成，前端创建对话框已接入 API |
| 知识库列表展示 | [x] | 前端 loadKnowledgeBases 已接入 API，支持展开查看文档 |
| 编辑知识库 | [x] | 后端新增 PUT /knowledge-bases/{id}，前端编辑对话框已接入 API |
| 删除知识库 | [x] | 后端 API 已完成，前端已接入实际 API 调用 |
| 上传知识库文档 | [x] | 后端接口已完成，前端上传后自动刷新文档列表 |
| 删除知识库文档 | [ ] | 前端无删除按钮（后端也未提供单独删除 KB 文档的路由） |
| RAG 参与 AI 生成 | [x] | 提取测试点和生成用例均已实际查询 ChromaDB 获取相关知识片段 |
| 多知识库关联 | [x] | 前端知识库选择框已改为动态加载，后端已查询向量库拼接 rag_context |

---

## 六、系统设置

| 功能 | 状态 | 备注 |
|------|------|------|
| LLM 配置持久化（API Key / 模型 / Base URL） | [x] | 后端 CRUD + 运行时同步均完成，前端已接入 API 保存，启动时自动加载 |
| 飞书 Webhook 配置持久化 | [x] | 后端 CRUD + 运行时同步均完成，前端已接入 API 保存 |
| 配置项重启后恢复 | [~] | 前端 onMounted 从数据库加载历史配置显示，但应用冷启动仍以 .env 初始值为主 |
| 系统设置列表查询 | [x] | 后端 API 已完成 |

---

## 七、通知服务

| 功能 | 状态 | 备注 |
|------|------|------|
| 飞书 Webhook 发送通知 | [x] | FeishuService 已实现，支持 post 类型消息卡片 |
| 测试点提取完成通知 | [x] | 异步任务完成后自动触发，含项目名称和提取数量 |
| 测试用例生成完成通知 | [x] | 异步任务完成后自动触发，含项目名称和生成数量 |
| 通知失败处理 | [x] | 失败只记录日志，不阻断主流程 |

---

## 八、任务批次与异步任务

| 功能 | 状态 | 备注 |
|------|------|------|
| 后台异步提取测试点 | [x] | 使用 FastAPI BackgroundTasks，TaskBatch 表记录进度 |
| 后台异步生成测试用例 | [x] | 同上 |
| 任务批次状态追踪 | [x] | 后端 TaskBatch 模型含 status / progress / error_message 等字段 |
| 任务批次查询 API | [x] | batches.py 提供按 ID、按项目查询接口 |
| 前端任务进度展示 | [x] | 新增 BatchTracker.vue 组件，集成到项目详情页，运行中任务每 3 秒自动轮询 |
| 任务失败重试 | [ ] | 无重试机制 |
| 任务取消 | [x] | 后端新增 PUT /batches/{id}/cancel，前端支持取消 PENDING/RUNNING 批次 |
| 任务完成通知 | [x] | BatchTracker 检测状态变化时自动弹出 ElNotification |
| 任务批次详情 | [x] | BatchTracker 新增详情弹窗，展示开始/完成时间、错误信息 |

---

## 九、基础设施与通用能力

| 功能 | 状态 | 备注 |
|------|------|------|
| FastAPI 异步架构 | [x] | 全异步，含 CORS / 自动建表 / 健康检查 |
| SQLAlchemy 2.0 async ORM | [x] | 含 get_db() 自动 commit/rollback |
| 数据库模型 | [x] | 8 张表全部定义完成 |
| Pydantic Schema | [x] | 全部定义完成，响应模型配置 from_attributes |
| Alembic 迁移 | [x] | 配置完成，支持 autogenerate |
| 日志系统 | [x] | loguru 双输出（stderr + 文件），自动轮转 |
| LiteLLM 多模型支持 | [x] | 支持 OpenAI / Claude / DeepSeek / 硅基流动等第三方平台 |
| 自定义 LLM Base URL | [x] | 通过 .env 或 SystemSettings 配置 |
| 数据初始化脚本 | [x] | seed_data.py 可批量生成测试数据 |
| 前端 Vite 代理 | [x] | /api 代理到 localhost:8000 |
| 前端 Element Plus 中文 | [x] | 已配置 zhCn 语言包 |
| 前端 Axios 封装 | [x] | 含 baseURL / timeout / 错误拦截 |

---

## 变更日志

> 后续所有迭代、修复、迁移、重构等操作，请在对应日期下方按模块记录变更内容。

### 2026-05-11（全面补齐实现）
**后端新增 API 端点：**
- `GET /api/v1/projects/{id}/documents/{doc_id}` — 文档详情
- `DELETE /api/v1/projects/{id}/documents/{doc_id}` — 删除文档
- `POST /api/v1/test-points/?project_id={id}` — 手动创建测试点
- `POST /api/v1/test-cases/?project_id={id}` — 手动创建测试用例
- `PUT /api/v1/knowledge-bases/{id}` — 更新知识库

**后端 RAG 集成修复：**
- `test_points.py` extract_test_points_task — 实际查询 ChromaDB 获取相关知识片段
- `test_cases.py` generate_test_cases_task — 同理修复，支持按测试点内容精确查询

**前端新增 API 封装文件：**
- `src/api/knowledgeBase.ts` — 知识库 CRUD + 文档上传/列表
- `src/api/settings.ts` — 系统设置 CRUD

**前端 API 封装补充：**
- `project.ts` — 新增 getDocument、deleteDocument
- `test.ts` — 新增 createTestPoint、createTestCase、updateTestCase、deleteTestCase、getTestCase 及其 TypeScript 接口

**前端视图全面修复：**
- `ProjectList.vue` — 编辑按钮接入 API，新增编辑对话框
- `Documents.vue` — 删除/查看接入 API，知识库选择框动态加载，移除"重新解析"按钮，大小列改为上传时间
- `TestPoints.vue` — 新增/编辑/删除/批量删除/确认全部接入 API，筛选实现 computed 过滤，下拉改为实际值（HIGH/MEDIUM/LOW）
- `TestCases.vue` — 新增/编辑/删除/批量删除全部接入 API，查看详情弹窗显示完整步骤，导出 Excel 接入下载，筛选实现 computed 过滤
- `KnowledgeBases.vue` — 列表加载/创建/编辑/删除/文档上传全部接入 API，展开时懒加载文档列表
- `Settings.vue` — LLM 配置和飞书配置保存接入 API，启动时自动从数据库加载已有配置

**新增组件：**
- `BatchTracker.vue` — 任务批次进度追踪组件，集成到 ProjectDetail.vue，运行中任务每 3 秒自动轮询

### 2026-05-11（PDF 乱码修复）
**问题：** PDF 中文文档解析后预览显示乱码（macOS Quartz PDFContext 不嵌入 ToUnicode CMap，CID 字体无法映射回 Unicode）

**修复方案：**
- `document_parser.py` parse_pdf — 先用 fitz.get_text() 提取文本，再通过 CJK 字符比例检测（`一-鿿` Unicode 范围，阈值 15%）判断是否乱码
- 乱码时降级为 Tesseract OCR（chi_sim+eng），通过 pdf2image 转图片后识别
- 新增依赖：`pytesseract`、`pdf2image`，系统安装 `tesseract` + `tesseract-lang` + `poppler`

### 2026-05-11（任务批次功能完善）
**后端：**
- `batches.py` — 新增 `PUT /{batch_id}/cancel` 端点，将 PENDING/RUNNING 批次标记为 FAILED（error_message 设为"用户手动取消"）

**前端 BatchTracker.vue 重写：**
- 始终显示面板，空状态显示 `el-empty`（"暂无任务批次"）
- 新增详情弹窗（`el-dialog`），展示任务类型、状态、进度、创建/开始/完成时间、错误信息
- 新增"取消"按钮（仅 PENDING/RUNNING 状态可操作），二次确认后调用 `cancelBatch()` API
- 新增任务完成/失败 `ElNotification` 弹窗提醒（通过 `prevStates` 追踪状态变化）
- 保留 3 秒轮询逻辑（仅在有 RUNNING/PENDING 任务时轮询）

**前端 ProjectDetail.vue 改造：**
- 新增"任务批次" Tab（`name="batches"`），标签显示运行中任务数量 Badge
- 批次 Tab 内嵌 `<BatchTracker>`，其他 Tab 使用 `<router-view>`
- 路由同步新增 `batches` 支持

**前端路由：**
- `router/index.ts` — 新增 `batches` 子路由（`path: 'batches', name: 'Batches', component: BatchTracker`）

**前端 API：**
- `test.ts` — 新增 `cancelBatch(batchId)` 封装

### 2026-05-11（初始梳理）
- 创建本文件，基于项目需求文档对全部功能模块进行前后端穿透式梳理。
- 标记各功能为 [x] / [~] / [ ] 三种状态。
- 识别核心已打通链路：项目 → 文档上传 → AI 提取测试点 → AI 生成用例 → 列表展示。
- 识别高优先级缺口：前端编辑/删除操作未调 API、Excel 导出未接入、任务进度追踪页面缺失、RAG 未真正参与 LLM 生成。
