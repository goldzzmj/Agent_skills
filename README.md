# Agent Skills Collection

面向 Claude Code / OpenCode 的 Skills 集合仓库，聚焦**文档自动化**、**项目深度分析**与**浏览器代理工作流**。

## 目录

- [仓库概览](#仓库概览)
- [Skills 清单](#skills-清单)
- [快速安装](#快速安装)
- [使用示例](#使用示例)
- [输出结构](#输出结构)
- [贡献指南](#贡献指南)

## 仓库概览

```text
Agent_skills/
├─ daily-reporting/
│  └─ daily-reporting.md
├─ comet-browser-control/
│  ├─ SKILL.md
│  ├─ README.md
│  └─ examples/
├─ project-deep-analyzer/
│  ├─ SKILL.md
│  ├─ references/
│  ├─ examples/
│  └─ scripts/
└─ README.md
```

## Skills 清单

| Skill | 位置 | 核心能力 | 典型使用场景 |
|---|---|---|---|
| `daily-reporting` | `daily-reporting/daily-reporting.md` | 自动生成结构化日报/周报 | 日常研发汇报、阶段性复盘、成果沉淀 |
| `comet-browser-control` | `comet-browser-control/SKILL.md` | 通过 OpenCode + Comet MCP 执行浏览器任务 | 深度网页调研、登录墙处理、动态页面、浏览器截图 |
| `project-deep-analyzer` | `project-deep-analyzer/SKILL.md` | 深度解析代码仓库/论文并产出技术白皮书 | 技术调研、架构梳理、面试准备、知识库建设 |

### 1) daily-reporting

- **定位**: 自动分析项目内容并生成 Markdown 日报文档。
- **适用任务**:
  - 生成项目日报
  - 记录工作进展
  - 汇报实施结果
  - 形成周报/月报素材
- **关键特点**:
  - 自动读取项目目录中的脚本、数据、日志、配置
  - 按固定结构生成可直接汇报的文档

### 2) project-deep-analyzer

- **定位**: 对项目/论文进行系统化技术深挖，输出结构化分析文档。
- **适用任务**:
  - GitHub 仓库解析
  - 本地项目深度剖析
  - 结合 arXiv 论文做“方法-代码”联动分析
- **关键特点**:
  - 支持 Mermaid 架构图、LaTeX 公式、逐行代码解析
  - 支持单文件输出或模块化多文件输出
  - 包含面试官视角 Q&A

### 3) comet-browser-control

- **定位**: 为 OpenCode 提供基于 Perplexity Comet 的浏览器代理工作流说明。
- **适用任务**:
  - 让 AI 控制 Comet 浏览器执行网页任务
  - 处理登录页和动态网站
  - 执行深度网页调研并截图验证
- **关键特点**:
  - 内置 OpenCode MCP 配置模板
  - 面向 Windows / WSL 的 `COMET_PATH` 说明
  - 提供 `connect -> ask -> poll -> screenshot` 推荐工作流

## 快速安装

将本仓库中的 Skill 目录复制到 Claude Code / OpenCode 的 Skills 目录。

OpenCode 常见自动发现目录：

- `~/.config/opencode/skills/`
- `.opencode/skills/`
- `.claude/skills/`
- `.agents/skills/`

### Windows

```bash
:: 安装 daily-reporting
xcopy /E /I daily-reporting "%USERPROFILE%\.claude\skills\daily-reporting"

:: 安装 comet-browser-control 到 OpenCode 项目目录
xcopy /E /I comet-browser-control ".opencode\skills\comet-browser-control"

:: 安装 project-deep-analyzer
xcopy /E /I project-deep-analyzer "%USERPROFILE%\.claude\skills\project-deep-analyzer"
```

### Linux / macOS

```bash
# 安装 daily-reporting
cp -r daily-reporting ~/.claude/skills/

# 安装 comet-browser-control 到 OpenCode 项目目录
cp -r comet-browser-control .opencode/skills/

# 安装 project-deep-analyzer
cp -r project-deep-analyzer ~/.claude/skills/
```

安装后请重启 Claude Code / OpenCode，使 Skills 生效。

## 使用示例

### daily-reporting

```text
请为项目 "C:\Projects\MyProject" 生成日报
```

```text
使用日报生成功能，项目路径是 "E:\Project\xxx"
```

### project-deep-analyzer

```text
分析这个项目：https://github.com/openai/whisper
```

```text
深度解析 E:/Project/my-model 这个项目
```

```text
分析 https://arxiv.org/abs/xxxxx 和对应代码仓库
```

### comet-browser-control

```text
用 Comet research 模式调研 2026 年主流 AI coding agents，输出中文对比表。
```

```text
用 Comet 打开 GitHub notifications；如果需要登录，就停在登录页等我接手。
```

```text
用 Comet 打开目标页面，完成后截图并告诉我当前页面状态。
```

## 输出结构

### daily-reporting 输出章节

标准输出通常包含以下 8 部分：

1. 项目背景与需求
2. 解决方案
3. 实施过程
4. 结果呈现
5. 技术亮点
6. 交付清单
7. 下一步计划
8. 附录

### project-deep-analyzer 输出模式

| 模式 | 适用场景 | 典型产物 |
|---|---|---|
| 单文件 | 小型项目、快速交付 | `output/{project_name}_ANALYSIS.md` |
| 模块化 | 大型项目、长期维护 | `00_OVERVIEW.md` + `01~05` 分章节文档 |

典型分析维度：

1. 论文精要与宏观架构
2. 核心源码深度剖析
3. 工程实践（部署与训练/推理）
4. 技术复盘与演进
5. 资深面试官 Q&A

## 贡献指南

欢迎提交新的 Skill 或改进现有 Skill。

1. Fork 本仓库
2. 新建或更新 Skill 目录
3. 在 `README.md` 中补充说明与示例
4. 提交 Pull Request

建议每个 Skill 包含 frontmatter：

```yaml
---
description: [技能描述]
tags: [标签1, 标签2, 标签3]
---
```

## License

MIT License

## 维护信息

- 贡献者: `goldzzmj`
- 更新时间: `2026-03-26`
- 版本: `v1.3`
