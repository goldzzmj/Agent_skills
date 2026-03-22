# Analysis Template

完整的技术分析模板，定义各章节的具体要求和内容规范。

---

## 1. 论文精要与宏观架构 (Top-level Architecture)

### 1.1 核心思想

**要求**：
- 用 3-5 句精炼语言概括项目解决的根本痛点
- 明确创新点和与现有方法的区别
- 不超过 200 字

**模板**：
```markdown
{项目名称} 旨在解决 {领域} 中的 {具体问题}。传统方法存在 {痛点1} 和 {痛点2} 的局限。
本项目通过 {核心创新} 实现了 {关键突破}，在 {指标} 上取得了 {提升幅度} 的改进。
```

### 1.2 数学原理

**要求**：
- 提取论文中最核心的 1-3 个公式
- 使用 LaTeX 语法，必须包含变量解释
- 公式需与代码实现对应

**模板**：
```markdown
### 目标函数

$$
\mathcal{L} = \mathcal{L}_{task} + \lambda \mathcal{L}_{reg}
$$

**变量解释**：
- $\mathcal{L}_{task}$：主任务损失（如交叉熵）
- $\mathcal{L}_{reg}$：正则化项
- $\lambda$：平衡系数，默认 0.1

### 核心算法

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

**变量解释**：
- $Q \in \mathbb{R}^{n \times d_k}$：查询矩阵
- $K \in \mathbb{R}^{m \times d_k}$：键矩阵
- $V \in \mathbb{R}^{m \times d_v}$：值矩阵
- $d_k$：缩放因子，防止梯度消失
```

### 1.3 架构逻辑图

**要求**：
- 使用 Mermaid flowchart 或 sequenceDiagram
- 展示完整数据流：Input → Preprocessing → Model → Output
- 标注关键模块和数据格式

**模板**：
```markdown
\`\`\`mermaid
flowchart TB
    subgraph Input["📥 输入层"]
        A[原始数据] --> B[数据预处理]
        B --> C[Tokenization]
    end

    subgraph Encoder["🔄 编码器"]
        C --> D[Embedding Layer]
        D --> E[Multi-Head Attention]
        E --> F[FFN]
        F --> G[Layer Norm]
    end

    subgraph Output["📤 输出层"]
        G --> H[Linear Projection]
        H --> I[Softmax]
        I --> J[预测结果]
    end

    style Input fill:#e1f5fe
    style Encoder fill:#fff3e0
    style Output fill:#e8f5e9
\`\`\`
```

---

## 2. 核心源码深度剖析 (Core Code Deep Dive)

### 2.1 模块选择原则

**优先分析**：
1. 核心网络结构（Model class）
2. 特殊的 Attention/Memory 机制
3. 关键的数据处理/采样逻辑
4. 自定义的 Loss 函数

**避免分析**：
- 通用 Utils 工具函数
- 标准的配置加载代码
- 常规的日志记录

### 2.2 代码解析格式

**要求**：
- 每行关键逻辑配中文注释
- 解释 "What" 和 "Why"
- 关联论文公式

**模板**：
````markdown
### 2.X {模块名称}

**文件位置**：`src/models/transformer.py`

**对应论文**：Section 3.2, Equation 4

```python
class MultiHeadAttention(nn.Module):
    """多头注意力机制实现

    对应论文公式 (2)：
    $$\text{MultiHead}(Q,K,V) = \text{Concat}(head_1,...,head_h)W^O$$
    """

    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.d_model = d_model      # 模型维度，如 512
        self.num_heads = num_heads  # 注意力头数，如 8
        self.head_dim = d_model // num_heads  # 每个头的维度：64

        # Q/K/V 投影矩阵，对应论文中的 W^Q, W^K, W^V
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)  # 输出投影 W^O

    def forward(self, x: Tensor, mask: Optional[Tensor] = None) -> Tensor:
        batch_size, seq_len, _ = x.shape

        # Step 1: 线性投影，生成 Q/K/V
        # Why: 将输入映射到不同的表示空间，增强表达能力
        Q = self.q_proj(x)  # [batch, seq, d_model]
        K = self.k_proj(x)
        V = self.v_proj(x)

        # Step 2: 重塑为多头形式
        # Why: 允许模型同时关注不同位置的不同表示子空间
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        # 现在形状: [batch, num_heads, seq_len, head_dim]

        # Step 3: 计算注意力分数
        # 对应论文公式：Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V
        scores = torch.matmul(Q, K.transpose(-2, -1))  # QK^T
        scores = scores / math.sqrt(self.head_dim)     # 缩放，防止梯度消失

        if mask is not None:
            # Why: 将 padding 位置的分数设为负无穷，softmax 后变为 0
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attn_weights = F.softmax(scores, dim=-1)  # 注意力权重

        # Step 4: 加权求和
        attn_output = torch.matmul(attn_weights, V)  # [batch, heads, seq, head_dim]

        # Step 5: 拼接多头并投影
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, seq_len, self.d_model)
        output = self.out_proj(attn_output)

        return output
```

**关键设计解析**：

1. **缩放因子 $\sqrt{d_k}$**：当 $d_k$ 较大时，点积结果也会很大，导致 softmax 梯度接近 0。除以 $\sqrt{d_k}$ 可以稳定训练。

2. **多头机制**：每个头学习不同的注意力模式，例如一个头关注语法，另一个头关注语义。
````

---

## 3. 工程实践：部署与训练 (Deployment & Training)

### 3.1 环境与依赖

**要求**：
- 列出系统要求（OS、GPU、CUDA）
- 核心依赖及版本
- 安装命令

**模板**：
```markdown
### 系统要求

| 项目 | 要求 |
|-----|------|
| OS | Linux (Ubuntu 20.04+) / macOS |
| Python | 3.8+ |
| CUDA | 11.7+ (GPU 训练) |
| GPU 显存 | 16GB+ (训练), 4GB+ (推理) |

### 核心依赖

```bash
# 使用 pip
pip install torch>=2.0.0 transformers>=4.30.0

# 或使用 uv (推荐)
uv pip install torch>=2.0.0 transformers>=4.30.0
```
```

### 3.2 快速推理

**要求**：
- 最简明的代码示例
- 可直接运行
- 包含输入输出示例

**模板**：
````markdown
```python
from model import load_model, inference

# 加载预训练模型
model = load_model("path/to/checkpoint")
model.eval()

# 推理
input_text = "Hello, world!"
output = inference(model, input_text)
print(output)  # 预期输出: ...
```
````

### 3.3 训练与微调

**要求**：
- 关键超参数说明
- 调参建议
- 显存/收敛影响分析

**模板**：
```markdown
### 关键超参数

| 参数 | 默认值 | 说明 | 调参建议 |
|-----|-------|------|---------|
| `learning_rate` | 1e-4 | 学习率 | 从 1e-5 开始逐步增大，观察 loss 曲线 |
| `batch_size` | 32 | 批大小 | 受显存限制，可配合 gradient_accumulation |
| `warmup_steps` | 1000 | 预热步数 | 约为总步数的 10% |
| `weight_decay` | 0.01 | 权重衰减 | 防止过拟合，通常 0.01-0.1 |

### 显存优化技巧

1. **Gradient Checkpointing**：牺牲 20% 速度换取 50% 显存节省
2. **Mixed Precision (FP16)**：显存减半，速度提升 2x
3. **Gradient Accumulation**：小 batch 模拟大 batch
```

---

## 4. 技术复盘与演进 (Evaluation & Improvements)

### 4.1 优势亮点

**维度**：
- 算法创新
- 工程实现
- 计算效率
- 可扩展性

**模板**：
```markdown
| 维度 | 亮点 | 说明 |
|-----|------|------|
| 算法 | 动态路由机制 | 根据输入自适应选择专家，提升 15% 准确率 |
| 工程 | 模块化设计 | 各组件可独立替换，便于二次开发 |
| 效率 | Flash Attention | 训练速度提升 2x，显存降低 40% |
```

### 4.2 瓶颈与不足

**要求**：
- 明确指出局限性
- 量化影响程度
- 提供场景说明

**模板**：
```markdown
| 瓶颈 | 影响场景 | 严重程度 |
|-----|---------|---------|
| 长上下文处理 | 超过 4K tokens 时性能下降 | ⭐⭐⭐ |
| 分布式通信 | 多卡训练时梯度同步开销大 | ⭐⭐ |
| 特定幻觉 | 涉及数值计算时可能出错 | ⭐⭐ |
```

### 4.3 改进方向

**要求**：
- 提出至少 2 个建设性建议
- 说明预期效果
- 给出实现思路

**模板**：
```markdown
### 改进方向 1：长上下文优化

**问题**：当前模型在超长序列上显存占用过高

**方案**：引入 Ring Attention 或 Blockwise Parallel Decoding

**预期效果**：支持 100K+ tokens，显存占用降低 60%

### 改进方向 2：推理加速

**问题**：推理延迟较高，难以满足实时需求

**方案**：实现 Speculative Decoding + 量化 (INT8/INT4)

**预期效果**：推理速度提升 3x，精度损失 < 1%
```

---

## 5. 资深面试官 Q&A (Expert Interview)

### 5.1 问题设计原则

**好问题特征**：
- 考察底层原理理解
- 需要综合多个知识点
- 没有标准答案，需要分析权衡
- 能区分初级和高级工程师

**问题类型**：
1. **原理深入型**：为什么这样设计？
2. **对比分析型**：A 和 B 的区别？
3. **场景应用型**：在 X 场景下如何选择？
4. **优化改进型**：如何解决 Y 问题？
5. **权衡取舍型**：性能和精度如何平衡？

### 5.2 Q&A 格式

**模板**：
```markdown
### Q1: {问题标题}

**问题**：{具体问题}

**参考答案**：

{分点解答，包含原理、代码、示例}

**关键要点**：
- 要点 1
- 要点 2

**延伸思考**：{相关的更深层问题}
```

### 5.3 问题示例

```markdown
### Q1: 为什么 Transformer 使用缩放点积注意力而不是原始点积？

**问题**：Transformer 的注意力公式中为什么要除以 $\sqrt{d_k}$？不除会怎样？

**参考答案**：

**原因分析**：

假设 $q$ 和 $k$ 是独立同分布的随机变量，均值为 0，方差为 1。
则 $q \cdot k = \sum_{i=1}^{d_k} q_i k_i$ 的方差为 $d_k$。

当 $d_k$ 较大时（如 512），点积结果的方差也会很大（512），导致：
- 部分值极大，部分值极小
- softmax 输出接近 one-hot（最大值接近 1，其余接近 0）
- 梯度接近 0，训练困难

**数学推导**：

$$
\text{Var}(q \cdot k) = d_k \cdot \text{Var}(q) \cdot \text{Var}(k) = d_k
$$

除以 $\sqrt{d_k}$ 后：

$$
\text{Var}\left(\frac{q \cdot k}{\sqrt{d_k}}\right) = \frac{d_k}{d_k} = 1
$$

**实验验证**：

```python
import torch
import torch.nn.functional as F

d_k = 512
q = torch.randn(1, 10, d_k)
k = torch.randn(1, 10, d_k)

# 不缩放
scores_no_scale = torch.matmul(q, k.transpose(-2, -1))
print(f"不缩放: max={scores_no_scale.max():.2f}, min={scores_no_scale.min():.2f}")
# 输出: max=50.32, min=-48.67

# 缩放后
scores_scaled = scores_no_scale / (d_k ** 0.5)
print(f"缩放后: max={scores_scaled.max():.2f}, min={scores_scaled.min():.2f}")
# 输出: max=2.22, min=-2.15
```

**关键要点**：
- 缩放保证 softmax 输入在合理范围
- 防止梯度消失，稳定训练
- 适用于任何点积注意力的实现

**延伸思考**：除了 $\sqrt{d_k}$，还有其他缩放方式吗？比如可学习的缩放参数？
```

---

## 6. 输出检查清单

生成文档前，确认以下内容：

- [ ] 所有数学公式使用 LaTeX 语法
- [ ] Mermaid 图表可正常渲染
- [ ] 代码示例可直接运行
- [ ] 变量解释完整
- [ ] 5 个面试问题涵盖不同类型
- [ ] 改进方向具体可行
- [ ] 文件路径准确
- [ ] 中文注释清晰
