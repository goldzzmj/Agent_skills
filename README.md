# Agent Skills Collection

这是一个收集了多个Claude Code Skills的仓库，用于增强AI开发效率。

## 📁 Skills 目录

### daily-reporting

**文件**: `daily-reporting/daily-reporting.md`

**功能**: 自动生成项目日报markdown文档

**用途**:
- 生成项目日报
- 记录工作进展
- 汇报项目成果
- 创建周报/月报

---

### project-deep-analyzer

**文件**: `project-deep-analyzer/SKILL.md`

**功能**: 深度技术解析技能，用于快速理解并剖析任意项目或论文

**用途**:
- 分析 GitHub 仓库或本地项目
- 生成结构化技术白皮书
- 架构图（Mermaid）和代码深度解析
- 专家级面试 Q&A

**特性**:
- 多源输入支持：GitHub 链接、本地项目路径、arXiv 论文链接
- 智能文档生成：自动生成架构图、数学公式、代码解析
- 灵活输出模式：单文件或模块化多文件输出
- 专家视角分析：包含面试级 Q&A

---

## 🚀 快速开始

### 安装 Skill

1. 将 skill 文件夹复制到你的 Claude skills 目录：

**Windows**:
```bash
# 安装 daily-reporting
copy daily-reporting\daily-reporting.md %USERPROFILE%\.claude\skills\

# 安装 project-deep-analyzer
xcopy /E /I project-deep-analyzer %USERPROFILE%\.claude\skills\project-deep-analyzer
```

**Linux/Mac**:
```bash
# 安装 daily-reporting
cp daily-reporting/daily-reporting.md ~/.claude/skills/

# 安装 project-deep-analyzer
cp -r project-deep-analyzer ~/.claude/skills/
```

2. 重启 Claude Code 使 skill 生效

---

## 📖 使用指南

### daily-reporting Skill

#### 功能概述

自动分析项目文件夹，读取脚本、数据、日志等信息，生成结构化的markdown日报。

#### 使用方式

**方式1: 直接描述需求**
```
请为项目 "C:\Projects\MyProject" 生成日报
```

**方式2: 指定项目路径**
```
使用日报生成功能，项目路径是 "C:\Projects\MyProject"
```

#### 日报结构

生成的日报包含以下章节：

```
一、项目背景与需求
   ├─ 1.1 业务背景
   ├─ 1.2 核心需求
   └─ 1.3 技术挑战

二、解决方案
   ├─ 2.1 系统架构
   └─ 2.2 核心模块设计

三、实施过程
   ├─ 3.1 阶段1
   ├─ 3.2 阶段2
   └─ 3.3 阶段3

四、结果呈现
   ├─ 4.1 输出文件
   ├─ 4.2 数据结构
   └─ 4.3 数据分析报告

五、技术亮点
   ├─ 5.1 健壮性设计
   ├─ 5.2 性能优化
   └─ 5.3 可维护性

六、交付清单
   ├─ 6.1 代码交付
   ├─ 6.2 数据交付
   └─ 6.3 文档交付

七、下一步计划
   ├─ 7.1 短期计划
   ├─ 7.2 中期计划
   └─ 7.3 长期规划

八、附录
   ├─ 8.1 项目目录树
   ├─ 8.2 关键指标
   └─ 8.3 团队协作
```

---

### project-deep-analyzer Skill

#### 功能概述

深度技术解析技能，生成结构化技术白皮书级别的 Markdown 文档。

#### 使用方式

**方式1: 提供 GitHub 链接**
```
分析这个项目：https://github.com/openai/whisper
```

**方式2: 提供本地项目路径**
```
深度解析 E:/Project/my-model 这个项目
```

**方式3: 结合 arXiv 论文**
```
分析 https://arxiv.org/abs/xxxxx 和对应的代码仓库
```

#### 输出结构

```
1. 论文精要与宏观架构
   ├─ 核心思想
   ├─ 数学原理（LaTeX 公式）
   └─ 架构逻辑图（Mermaid）

2. 核心源码深度剖析
   ├─ 精选 2-3 个核心模块
   └─ 逐行代码解析

3. 工程实践：部署与训练
   ├─ 环境与依赖
   ├─ 快速推理
   └─ 训练与微调

4. 技术复盘与演进
   ├─ 优势亮点
   ├─ 瓶颈与不足
   └─ 改进方向

5. 资深面试官 Q&A
   └─ 5 个高阶问题与解答
```

#### 目录结构

```
project-deep-analyzer/
├── SKILL.md                          # 主技能文件
├── references/
│   ├── analysis-template.md          # 分析模板
│   └── interview-patterns.md         # 面试问题模式库
├── examples/
│   └── single-file-output.md         # 输出示例
└── scripts/
    ├── clone_repo.py                 # Git 仓库克隆工具
    └── analyze_structure.py          # 项目结构分析工具
```

---

## 🔧 技术支持

### Skill 文件格式

每个 skill 文件需要包含以下 frontmatter：

```yaml
---
description: [技能描述]
tags: [标签1, 标签2, 标签3]
---
```

### 贡献指南

欢迎提交新的 skill！

1. Fork 本仓库
2. 创建新的 skill 文件
3. 添加使用说明到 README
4. 提交 Pull Request

---

## 📄 License

MIT License

---

## 🤝 贡献者

- goldzzmj

---

**更新时间**: 2026-03-22
**版本**: v1.1
