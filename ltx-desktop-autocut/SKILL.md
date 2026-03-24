---
name: LTX Desktop Autocut
description: This skill should be used when the user asks to "使用 LTX Desktop 自动剪辑视频", "自动控制 LTX Desktop", "用照片和音乐生成卡点视频", "在 LTX 里导入素材并导出成片", or mentions LTX Desktop video editing automation, beat-sync slideshow editing, or building an LTX-ready project from local photos and music.
version: 0.1.0
---

# LTX Desktop Autocut

用于把“本地照片 + 本地音乐”整理成适合 `LTX Desktop` 导入和导出的自动剪辑工作流。核心目标不是强行在未知 UI 上盲点，而是先把素材整理成易于导入的结构，再使用桌面自动化完成最少且稳定的 LTX 操作。

## 适用场景

- 用户已经安装好 `LTX Desktop`
- 需要把照片做成婚礼/纪念/相册类卡点视频
- 需要结合本地 BGM 做节奏感较强的成片
- 需要尽量自动化完成导入、时间线放置、导出

## 工作原则

1. 先确认 `LTX Desktop` 已正常启动且窗口可恢复。
2. 先确认本地音乐是否已经存在；不要帮助下载未授权音乐。
3. 先把素材预处理成 `LTX` 更容易吃进去的单个或少量媒体文件。
4. 优先自动化稳定步骤：窗口恢复、截图、OCR、导入、导出。
5. 遇到文件对话框、编码路径、OCR 识别不稳时，优先切换到 ASCII 路径。
6. 如果 LTX 内部复杂剪辑动作不稳定，先在外部脚本完成节奏和素材整理，再让 LTX 做最终装配/导出。

## 推荐工作流

### 第 1 步：确认环境

依次完成：

- 确认 `LTX Desktop` 进程存在
- 恢复窗口，避免最小化状态（最小化时常见坐标是 `-32000, -32000`）
- 确认本地自动化运行环境可用：`pyautogui`、`pywinctl`、`pillow`、`opencv-python`、`easyocr`
- 如果 `uvx` 不可用，不要卡住；直接使用 Python 脚本控制桌面

### 第 2 步：准备素材

优先将素材整理为：

- 照片目录：按时间顺序排序的 `.JPG`
- 音乐目录：本地 `.mp3/.wav`
- 输出目录：`output/ltx_assets/`

推荐先做两件事：

1. 选出更适合卡点的视频照片子集，而不是全量都塞进 LTX
2. 把音乐预拼接成一个目标时长（如 180 秒）的混音版本，减少 LTX 内时间线操作复杂度

### 第 3 步：外部预处理为 LTX-ready 资产

优先使用 `scripts/make_ltx_ready_video.py`：

- 把照片缩放到 `1280x720`
- 用固定节奏时长模式生成卡点感视频片段
- 拼接本地音乐，得到时长约 180 秒的成片
- 输出到 ASCII 友好目录，避免文件对话框路径乱码

这样做的优势：

- 避免在 LTX 内逐张调图片时长
- 避免在 LTX 内大量手动找卡点
- 把 LTX 的任务缩小到“导入成片/再加工/导出”

### 第 4 步：控制 LTX Desktop

优先顺序：

1. 恢复并激活窗口
2. 截图窗口
3. OCR 读取关键文字（如 `Import Media`、`Export`、`Assets`、`Timeline 1`）
4. 点击导入/导出等稳定按钮

不要一开始就尝试复杂拖拽。先验证：

- 是否能稳定找到 `Import Media`
- 是否能稳定找到 `Export`
- 文件选择器路径是否正常

### 第 5 步：导入策略

推荐两种导入策略：

#### 策略 A：导入单个 LTX-ready 成片（最稳）

适合自动化优先的场景。

- 导入一个已经带配乐的 `mp4`
- 在 LTX 中只做轻度复查、必要标题、最终导出

#### 策略 B：导入静音视频 + 独立音轨（次稳）

适合希望继续在 LTX 调整音轨的场景。

- 导入静音 `mp4`
- 导入拼好的 `bgm_mix.mp3`
- 在 LTX 中把视频放到视频轨，音频放到音频轨，再导出

## OCR 与坐标策略

使用 `scripts/ocr_image.py` 对窗口截图做 OCR。实践中常见可识别文本包括：

- `Import Media`
- `Drop clips here`
- `Assets`
- `Video Editor`
- `Timeline 1`
- `Export`

处理建议：

- 先用 OCR 锁定文字的大概框位置
- 再把点击坐标转成“窗口相对坐标”
- 每次点击前都先激活对应窗口
- 每次关键动作后都重新截图确认状态变化

## 常见问题

### 文件对话框路径乱码/打不开

优先处理方式：

- 复制待导入文件到 ASCII 路径，如 `E:\Project\temp\ltxdrop\ready.mp4`
- 再在 LTX 中导入这个路径

### OCR 模型下载失败

优先处理方式：

- 给 Python 设置 `HTTP_PROXY` / `HTTPS_PROXY`
- 再运行 `scripts/ocr_image.py`

### LTX 窗口最小化导致坐标异常

先调用窗口恢复，再继续：

- `restore()`
- `activate()`

### 无法稳定在 LTX 内逐素材剪辑

切换思路：

- 在外部脚本完成节奏剪辑
- 只让 LTX 做最终导入与导出

## 推荐产物结构

```text
output/
  ltx_assets/
    ltx_ready_beatcut.mp4
    frames/
```

如果要进一步拆分：

```text
output/
  ltx_assets/
    silent_slideshow.mp4
    bgm_mix.mp3
```

## 执行清单

按以下顺序执行：

1. 检查 `LTX Desktop` 是否运行
2. 恢复窗口并截图
3. OCR 识别关键按钮
4. 预处理照片与音乐
5. 输出 LTX-ready 文件到 ASCII 路径
6. 让 LTX 导入该文件
7. 导出最终 `mp4`

## Additional Resources

### Reference Files

- `references/workflow.md` - 详细操作流程、失败回退策略、适合婚礼卡点视频的实践总结

### Scripts

- `scripts/make_ltx_ready_video.py` - 将本地照片和本地音乐生成适合 LTX 使用的卡点成片
- `scripts/ocr_image.py` - 对 LTX 或资源管理器截图做 OCR，提取界面文字与坐标
