---
name: comet-browser-control
description: Use Perplexity Comet through OpenCode MCP for browser tasks, deep research, login-gated sites, dynamic pages, screenshots, and long-running web workflows.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  platform: windows-wsl-macos
---

# Comet Browser Control

通过 OpenCode + `comet-mcp` 把 Perplexity Comet 变成可调度的浏览器代理。

## What I do

- 把高层目标委托给 Comet，而不是让主模型自己逐步点网页
- 适合登录墙、动态页面、多步骤网页任务、深度 Research
- 提供标准调用顺序：connect -> mode -> ask -> poll/stop -> screenshot
- 在 Windows / WSL 场景下提醒 `COMET_PATH` 和联网注意事项

## When to use me

在这些场景优先加载本 skill：

- 用户要求“控制 Comet 浏览器去做事”
- 需要真实浏览器交互，而不是纯文本搜索
- 需要登录网站、打开动态内容、等待页面状态变化
- 需要让 Comet 执行长时间网页任务并持续轮询进度

## Preconditions

使用前先检查当前会话里是否已经有 Comet MCP 工具；如果没有，先提示用户配置 OpenCode MCP：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "comet-bridge": {
      "type": "local",
      "command": ["npx", "-y", "comet-mcp"],
      "enabled": true,
      "environment": {
        "COMET_PATH": "C:\\Users\\GX\\AppData\\Local\\Perplexity\\Comet\\Application\\comet.exe"
      }
    }
  }
}
```

说明：

- `COMET_PATH` 应优先写到 `comet.exe`
- 如果你想改用另一份安装，也可以填 `F:\\Comet\\comet.exe`
- Windows 默认端口是 `9222`
- WSL2 需要 mirrored networking，才能访问 Windows 上启动的 Comet

## Tool strategy

实际工具名可能带有 MCP server 前缀。优先使用当前会话中可见的 Comet 相关工具。

推荐流程：

1. 先调用 `comet_connect`
2. 根据任务切换 `comet_mode`
3. 用 `comet_ask` 下达高层目标，避免写成逐点击脚本
4. 如果任务较长，继续用 `comet_poll`
5. 如果浏览偏航，用 `comet_stop`
6. 需要验证界面时用 `comet_screenshot`

## Mode selection

- `search`: 快速网页搜索
- `research`: 深度调研、总结、信息汇总
- `labs`: 偏分析、可视化、代码/数据相关任务
- `learn`: 教学式解释和知识学习

默认建议：

- 普通网页查找 -> `search`
- 多来源调研/报告整理 -> `research`
- 数据分析/生成结构化结论 -> `labs`

## Prompting rules

给 Comet 的任务描述应聚焦目标、上下文、输出格式，不要写成底层点击指令。

好的例子：

- “登录 GitHub，查看未读通知，并按重要性列出前 5 条。”
- “去调研 2026 年主流 AI coding agents，对比价格、上下文窗口和 IDE 集成能力，输出表格。”
- “打开这个后台页面，找到最近 7 天报表并截图。”

避免：

- “点击左上角，再点第二个按钮，再输入 xxx”

## Long-running workflow

如果 `comet_ask` 返回任务仍在进行中：

1. 记录当前状态
2. 调用 `comet_poll`
3. 如果出现偏航、循环或明显错误，调用 `comet_stop`
4. 必要时重新发起更清晰的新任务，并使用 fresh/new chat 语义

## Safety notes

- 不替用户提交不可逆操作，除非用户明确要求
- 涉及账号登录时，只让 Comet 打开登录页和等待用户处理，不猜测或伪造凭据
- 涉及支付、删除、发布、修改生产数据时，必须在最终动作前再次核对目标

## Response pattern

完成任务后，输出应包含：

- Comet 做了什么
- 当前页面/当前状态
- 关键结果或提取信息
- 是否需要用户接手登录或二次确认
- 下一步最合理动作

## Example requests

```text
用 Comet 打开 Notion，检查今天的待办，然后总结我最先该处理的三件事。
```

```text
用 Comet research 模式调研 comet-mcp 和 browser-use 的差异，输出中文对比表。
```

```text
用 Comet 登录 GitHub，打开我的 notifications 页面，截图并总结重点。
```
