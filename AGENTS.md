# AGENTS.md

本文档是「论文速览」的格式与流程规范。本仓库里的每份速览、以及后续新增或续写的主题，都应遵守；这样跨主题、跨轮次产出的东西才是一致的。

## 目标

用户要的是**单文件 HTML 速览**：把某个领域一段时间的论文系统归类，每篇用「配方 + 一句话」讲清楚，面向没读过原文的初学者，全程中文。领域不限——生成模型、NLP、系统、理论、评测、数据集……都能套这套格式。

## 每篇论文的固定写法

每篇只写两样：一个「配方」+ 一句「三段总结」。HTML 结构如下，照抄：

```html
<p class="paper"><b>论文名（作者 年份）</b>（<a href="链接">出处</a>）<br>
<code class="recipe">…… -&gt; …… + ……</code><br>
<span class="idea"><span class="p">问题</span> ……；<span class="p">方法</span> ……；<span class="p">核心</span> ……。</span></p>
```

### 配方（`<code class="recipe">`）

统一写成：

```
<对象 / 方法> -> <产出 / 结论> + <目标 / 机制 / 条件>
```

一句话说：**「它产出/做了什么」和「靠什么做到/怎么验证」两部分都要写全**，这是信息完整性的保证。不写完整公式，只写类型。

按论文类型，「产出」和「靠什么」对应不同的东西，但「成对出现、缺一不可」这个要求不变：

| 论文类型 | 产出 | 靠什么 |
|---|---|---|
| 学习方法 / 生成模型 | 预测目标（pred） | 损失 / 目标（loss） |
| 理论 / 分析 | 结论 | 假设 / 证明手段 |
| 评测 / 基准 | 指标 | 评测协议 |
| 数据集 | 数据内容 | 采集方式 / 许可 |
| 综述 | 分类体系 | 划分标准 |

学习方法类的具体词汇（最常用）：

- 预测：`ε-pred / v-pred / x-pred / consistency / next-token / score / 成分树 / 依存树 / 文法`
- 损失：`ε-loss / v-loss / x-loss / consistency-loss / next-token-loss / MLE / EM / ELBO / 重建 / SVD`
- 例：`flow(patch + noise) -> x-pred + v-loss`、`pcfg(sentence) -> 成分树 + MLE`

> 学习方法类里，pred 和 loss 必须都写；只写 `v-pred` 不写 loss 是反面教材。其他类型同理：只写「得出一个结论」而不写「在什么假设下成立」，或只写「给个榜单」而不写「用什么协议」，都是不完整的。

### 一句话（`<span class="idea">`）

固定三段，顺序是 **问题 → 方法 → 核心/效果**，每段都要有信息量：

- **问题**：要解决的具体问题。
- **方法**：怎么解决的，写关键机制。
- **核心 / 效果**：默认写「核心」（最关键的贡献 / insight，一句话能让人记住）；如果用户明确要「问题方法效果」（常见于深读单篇/单家族），第三段就写「效果」，落到具体 benchmark 数字（如 GenEval 0.87、MMMU 51.7），别写「效果很好」这种空话。

反面教材（被否过的空壳）：「系统梳理了 XX」「验证了可行性」「做了系统比较」——等于什么都没说。

## 示例（配方 + 一句话）

几个真实条目，覆盖不同论文类型，看「产出 + 靠什么」怎么落（HTML 里箭头用 `-&gt;`）：

### 学习方法 / 生成模型（pred + loss）

```html
<p class="paper"><b>JiT（Back to Basics）</b>（<a href="https://arxiv.org/abs/2511.13720">2511.13720</a>）<br>
<code class="recipe">flow(patch + noise) -&gt; x-pred + v-loss</code><br>
<span class="idea"><span class="p">问题</span> 高维像素空间预测噪声/速度会崩；<span class="p">方法</span> 让网络直接预测干净图 x，损失用 v-loss（把 x̂ 换算成 v̂ 再回归）；<span class="p">核心</span> 干净图在低维流形、噪声图在高维全空间，所以 x-pred 让普通 ViT + 大 patch 训得动。</span></p>
```

### 理论 / 分析（结论 + 假设 / 证明手段）

```html
<p class="paper"><b>Towards a Theory of Structure Acquisition</b>（<a href="https://arxiv.org/abs/2406.00048">2406.00048</a>）<br>
<code class="recipe">analysis(PCFG 合成数据 + next-token) -&gt; 语法习得的理论刻画 + 训练动力学分析</code><br>
<span class="idea"><span class="p">问题</span> DNN 学语法的理论机制是什么；<span class="p">方法</span> 在 PCFG 合成数据上分析 next-token 预测如何一步步学出语法；<span class="p">核心</span> 给出「结构如何在 DNN 中习得」的理论刻画。</span></p>
```

### 评测 / 基准（指标 + 评测协议）

```html
<p class="paper"><b>An Empirical Comparison of Unsupervised Parsing</b>（<a href="https://aclanthology.org/2020.acl-main.302/">ACL 2020</a>）<br>
<code class="recipe">benchmark(统一重训重评 8 方法) -&gt; F1 + 统一协议</code><br>
<span class="idea"><span class="p">问题</span> 各方法用不同树库/评估、数字不可比；<span class="p">方法</span> 统一在 PTB 重训重评；<span class="p">核心</span> 给出第一个可比排行榜，暴露 F1 虚高来自评估差异。</span></p>
```

### 数据集（内容 + 采集 / 许可）

```html
<p class="paper"><b>ImageNet</b>（Deng et al. 2009）<br>
<code class="recipe">dataset(自然图像) -&gt; 1000 类千万级标注 + WordNet 层级 / 众包清洗</code><br>
<span class="idea"><span class="p">问题</span> 缺一个足够大、类别清晰的图像基准；<span class="p">方法</span> 用 WordNet 层级组织、众包清洗出千万级标注图；<span class="p">核心</span> 成为 CV 深度学习的通用基准。</span></p>
```

> 看共性：`-&gt;` 左边是研究对象/方法，右边第一段是「产出/结论」，`+` 后是「靠什么做到/怎么验证」——两部分缺一不可，这就是「配方」要保证的信息完整性。

## 数据空间 / 结构记法

- **数据在哪个空间**：写清方法直接在原始输入上做，还是先过某种编码/压缩。例：有 VAE 就写 `vae(patch)`，没有就写 `patch`；句法里写 `sentence` / `pos-seq`。
- **统一 / 多组件模型要说清 share 关系**：
  - `X_shared` —— X 由多方共享
  - `X_und + X_gen` —— 各方各一套 X
  - `X (Y_und + Y_gen)` —— X 共享，内部 Y 拆开
  - 例：`transformer_shared (head_lm + head_diffuse)`、`transformer (moe_und + moe_gen)`

## 归类与趋势段

- 用 `<h3>` 分大类（按主题或年代），每类开头先写一段 `<p class="trend">` 的**发展趋势**（这一块在解决什么、从哪到哪、代表是什么），再逐篇列。
- 时间窗口**之前**的关键「源头 / 地基」也要收，单独成一节标「源头」，别硬塞。
- 文末写「共识与分歧」：几条共识 + 几条分歧 / 开放难点。

## 质量底线（被反复纠正过）

1. **两部分都写全**：pred+loss（或对应等价物）缺一不可。
2. **一句话三段都要有**，且不能是空壳。
3. **抽象概括落到具体条件**：说「用 X 解决 Y」要具体到机制（比如「浅层重建 + 深层语义对齐、CLIP/DINOv2/SAM 监督」，而不是「统一了重建与语义」）。
4. 面向初学者：说人话，不堆公式、不甩术语。
5. 全文中文，配方记号除外。

## 检索与核实流程

1. 去读原文（摘要 + 参考文献），不是只看标题。
2. 交叉引用找缺口：拉几篇「hub 论文」的参考文献（arXiv 的 ar5iv HTML、Semantic Scholar Graph API），跟已有清单 diff，找漏掉的关键论文——范式「地基」最容易被漏。
3. 查 follow-up / 续作（被引方向），别漏（曾漏过 R2D2 → Fast-R2D2）。
4. 核实再写：arXiv / venue / 作者回原文或搜索引擎核对，不许编。近期用 arXiv，经典用 aclanthology / JMLR / DOI。
5. 拿不准的元数据在文末 `<p class="note">` 说明，别硬给可能错的链接。

## 交付

- 直接手写 HTML（不要 Markdown 转 HTML），内联 CSS，单文件自包含，风格对齐本仓库已有文件。
- 成品放仓库根目录，更新 `index.html` 和 `README.md` 的索引。
