---
name: project-deep-analyzer
description: This skill should be used when the user asks to "analyze this project", "understand this codebase", "generate technical whitepaper", "deep dive into this repository", "analyze GitHub repo", "解析项目", "了解这个代码库", or provides a GitHub URL / local project path for comprehensive technical analysis. Produces structured technical documentation with architecture diagrams, code deep dives, and expert Q&A.
version: 1.0.0
tags: [Analysis, Documentation, Research, CodeReview, Architecture]
---

# Project Deep Analyzer

深度技术解析技能，用于快速理解并剖析任意项目或论文，生成结构化技术白皮书级别的 Markdown 文档。

## Core Capabilities

1. **多源输入支持**：GitHub 链接、本地项目路径、arXiv 论文链接
2. **智能文档生成**：自动生成架构图（Mermaid）、数学公式（LaTeX）、代码解析
3. **灵活输出模式**：单文件或模块化多文件输出，根据项目复杂度自适应
4. **专家视角分析**：包含面试级 Q&A，适合技术调研和面试准备

## Workflow

### Phase 1: Input Collection

与用户确认分析目标和输入形式：

```
支持的输入类型：
1. GitHub 仓库链接 → 克隆并分析
2. 本地项目路径 → 直接分析
3. arXiv 论文链接 → 结合论文与代码分析
```

**确认问题示例**：
- "请提供项目链接或本地路径"
- "是否有关联的论文需要参考？"
- "是否有特别关注的模块或功能？"

### Phase 2: Scope Definition

与用户确认输出范围：

| 输出模式 | 适用场景 | 文件结构 |
|---------|---------|---------|
| 单文件 | 小型项目、快速概览 | `TECHNICAL_ANALYSIS.md` |
| 模块化 | 大型项目、完整文档 | `docs/` 目录，按章节拆分 |

**确认问题示例**：
- "项目规模较大，建议采用模块化输出，是否同意？"
- "是否需要生成独立的面试 Q&A 文件？"

### Phase 3: Deep Analysis

执行五维度分析，详见 `references/analysis-template.md`：

1. **论文精要与宏观架构** - 核心思想、数学原理、Mermaid 架构图
2. **核心源码深度剖析** - 精选 2-3 个核心模块，逐行解析
3. **工程实践** - 环境依赖、推理 Demo、训练配置
4. **技术复盘与演进** - 优势、瓶颈、改进方向
5. **资深面试官 Q&A** - 5 个高阶问题与解答

### Phase 4: Document Generation

根据确定的输出模式生成文档：

**单文件模式**：
```
output/
└── {project_name}_ANALYSIS.md
```

**模块化模式**：
```
output/
├── 00_OVERVIEW.md          # 总览与快速入门
├── 01_ARCHITECTURE.md      # 架构设计
├── 02_CODE_DEEP_DIVE.md    # 核心代码解析
├── 03_DEPLOYMENT.md        # 部署与训练
├── 04_EVALUATION.md        # 评估与改进
├── 05_INTERVIEW_QA.md      # 面试问答
└── assets/
    └── diagrams/           # Mermaid 图表源码
```

## Input Handling

### GitHub Repository

```bash
# 克隆仓库到临时目录
git clone --depth 1 {repo_url} /temp/repo_analysis/

# 分析完成后提示用户是否保留
```

### Local Project

直接读取指定路径，无需额外处理。

### arXiv Paper

使用 `mcp__web_reader__webReader` 获取论文内容，结合代码仓库进行联合分析。

## Quality Standards

### Architecture Diagrams

使用 Mermaid 语法，确保：
- 数据流向清晰（Input → Processing → Output）
- 模块边界明确
- 关键组件标注

### Code Analysis

- 精选核心模块，避免罗列 Utils
- 逐行注释使用中文
- 解释 "What" 和 "Why"
- 关联论文公式

### Mathematical Formulas

使用 LaTeX 语法：
- 行内公式：`$formula$`
- 块级公式：`$$formula$$`
- 必须包含变量解释

## Additional Resources

### Reference Files

- **`references/analysis-template.md`** - 完整的分析模板与章节要求
- **`references/output-examples.md`** - 各章节的输出示例
- **`references/interview-patterns.md`** - 高阶面试问题模式库

### Scripts

- **`scripts/clone_repo.py`** - Git 仓库克隆工具
- **`scripts/analyze_structure.py`** - 项目结构分析工具

### Examples

- **`examples/single-file-output.md`** - 单文件输出示例
- **`examples/modular-output/`** - 模块化输出示例目录

## Usage Examples

**触发方式 1：直接提供链接**
```
用户：https://github.com/openai/whisper
助手：[加载 skill] 开始分析 Whisper 项目...
```

**触发方式 2：明确指令**
```
用户：帮我深度解析这个项目的架构和核心代码
助手：[加载 skill] 请提供项目链接或本地路径...
```

**触发方式 3：本地项目**
```
用户：分析一下 E:/Project/my-model 这个项目
助手：[加载 skill] 开始分析本地项目...
```

## Error Handling

| 场景 | 处理方式 |
|-----|---------|
| 仓库不存在/私有 | 提示用户提供正确链接或本地路径 |
| 项目过大 | 建议模块化输出，分批分析 |
| 无关联论文 | 跳过论文精要章节，专注代码分析 |
| 依赖安装失败 | 记录问题，继续分析已解析部分 |

## Notes

- 大型项目建议使用模块化输出，便于维护和阅读
- 分析前可先浏览项目 README 和目录结构
- 生成后可根据用户反馈迭代优化特定章节
