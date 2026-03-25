# comet-browser-control

给 OpenCode 增加一套面向 Perplexity Comet 的浏览器控制说明与 Skill 模板。

## 这个 Skill 解决什么问题

`comet-mcp` 的核心思路不是“让主模型自己点浏览器”，而是：

- OpenCode 负责总体目标和结果整合
- Comet 负责真实网页导航、搜索、登录墙、动态内容与长任务执行

这很适合：

- 深度网页调研
- 打开需要登录的网站
- 处理动态页面
- 让浏览器自主跑一段时间再回报结果

## 你当前环境的建议配置

你已经有两个相关路径：

- `F:\Comet`
- `C:\Users\GX\AppData\Local\Perplexity\Comet\Application`

按 `comet-mcp` 源码，`COMET_PATH` 最稳妥的写法是直接指向可执行文件：

- 推荐：`C:\Users\GX\AppData\Local\Perplexity\Comet\Application\comet.exe`
- 备选：`F:\Comet\comet.exe`

如果不写 `COMET_PATH`，Windows 下它会优先尝试 `%LOCALAPPDATA%\Perplexity\Comet\Application\comet.exe`。

## OpenCode 配置示例

把下面内容放到你的 `opencode.json`，或合并到已有配置：

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

## 推荐安装位置

OpenCode 会自动发现这些目录中的 Skill：

- `.opencode/skills/`
- `.claude/skills/`
- `.agents/skills/`
- `~/.config/opencode/skills/`

你当前把 Skill 存在 `E:\Project\Agent_skills` 没问题，适合作为技能仓库；要让 OpenCode 自动加载，建议再复制一份到：

```text
E:\Project\.opencode\skills\comet-browser-control\SKILL.md
```

或：

```text
C:\Users\GX\.config\opencode\skills\comet-browser-control\SKILL.md
```

## 最常见使用方式

### 1. 快速网页任务

```text
用 Comet 打开官网，帮我找 pricing 页面并总结关键套餐。
```

### 2. 深度调研

```text
用 Comet research 模式调研 2026 年主流 AI coding agents，输出中文对比表。
```

### 3. 登录后页面

```text
用 Comet 打开 GitHub notifications；如果需要登录，就停在登录页等我接手。
```

### 4. 需要截图

```text
用 Comet 打开目标页面，完成后截图并告诉我当前页面状态。
```

## 推荐工作流

1. `comet_connect`：连接并自动启动 Comet
2. `comet_mode`：切到 `search` / `research` / `labs`
3. `comet_ask`：给高层目标
4. `comet_poll`：任务长时轮询
5. `comet_stop`：偏航时停止
6. `comet_screenshot`：做结果校验

## 注意事项

- 涉及登录时，让 Comet 导航到登录页即可；凭据应由用户自行处理
- 涉及支付、删除、发布等动作，必须先确认目标
- WSL2 下如果连不上 Windows 的 Comet，请开启 mirrored networking

## 参考结论

基于 `hanzili/comet-mcp` 当前 README 与源码：

- 服务通过 `npx -y comet-mcp` 启动
- 主要工具为 `comet_connect`、`comet_ask`、`comet_poll`、`comet_stop`、`comet_screenshot`、`comet_mode`
- Windows 默认使用 `comet.exe`，并支持 `COMET_PATH` 覆盖
- 默认 remote debugging 端口为 `9222`
