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

> **每个领域先定自己的「最大公约数」记法**（2~3 个关键对比轴），再写配方。上面的 pred+loss 只是「学习方法 / 生成模型」这一类的一个例子，**不是所有领域都套 pred+loss**——真正不变的是「产出 + 靠什么」这两段，两边填什么由领域自己定。例：RL 用 `advantage / credit / critic-free / on-policy`，harness 用 `aci / context / tools / sandbox`，注意力用 `linear / sparse / delta / ssm`，长上下文用 `dense / sparse / evict / rope`。每个 HTML 的 `§0 记法` 就是这组最大公约数的落地。

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

> **领域里最重要的那几篇（源头 / 地基 / 范式转折点）不要限字数**：可以比「一句话」多写几句，把这些写透——它给后续文章奠定了什么基础、做到了什么、**没做到什么**（缺口正是后续文章发散出来的起点）、和后续哪几篇是什么承接关系。后面很多文章都是从这里长出来的，只写一句会断掉整条线。

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

- 用 `<h3>` 分大类（按主题或年代）。`<h3>` 标题要「年代 / 主题 + 一句话标签」，让人不看正文也知道这段是什么：例 `2.1 经典/谱方法（2010-2015）`、`2.0 源头（2002-2009，奠定问题与 baseline）`。
- 每个 `<h3>` 开头写一段 `<p class="trend">` 引言，再逐篇列。这段引言是**本文件最重要的可读性来源**（`grammar-induction.html` 是标杆），要写满五件事，缺一不可：
  1. **这一块在解决什么**：一句话把问题域定住（「在 2010 年之前，这个问题已经被定义清楚：从裸文本学出成分树或依存树」）。
  2. **枚举具体关键思想 / 代表，带短名或作者**：点名这段的代表，而不是泛泛说「各种方法」（「上下文特征（CCM）、贝叶斯正则（Johnson）、对比估计（Smith & Eisner）、在线 EM（Liang & Klein）」）。
  3. **点出核心矛盾 / 痛点**：这段卡在哪（「都困在局部最优 + 无标注里」）。
  4. **往前桥接**：说清这条线怎么流到下一段，给后面埋伏笔（「后来几乎全部被神经一代继承」「成为进入 LLM 时代的桥」）。
  5. **有数字就给数字**：能落到具体量就落（「F1 从 40+ 一路推到 50+」），别停在「显著提升」这种空话。
- 引言可以有「两条主线」「三个方向」这类并行枚举（「两条主线：一是怎么跳出局部最优…，二是怎么给出有理论保证的估计…」），帮读者一眼看到这段的分叉结构。
- 时间窗口**之前**的关键「源头 / 地基」也要收，单独成一节标「源头」，别硬塞。
- 文末写「共识与分歧」：几条共识 + 几条分歧 / 开放难点。

`<h2>` 的「主线」一节建议三段式（`grammar-induction.html` §1 是标杆）：① 分代列表（每代 = 时间 + 一句话总结 + 一个具体结果）；② 一个「几个轴在收敛」的表格（从 → 到 → 代表）；③ 一个开放问题收尾（「语法是显式学出来的文法，还是 LLM 里天然涌现的隐式结构？」）。

## 质量底线（被反复纠正过）

1. **两部分都写全**：pred+loss（或对应等价物）缺一不可。
2. **一句话三段都要有**，且不能是空壳。
3. **抽象概括落到具体条件**：说「用 X 解决 Y」要具体到机制（比如「浅层重建 + 深层语义对齐、CLIP/DINOv2/SAM 监督」，而不是「统一了重建与语义」）。
4. 面向初学者：说人话，不堆公式、不甩术语。
5. 全文中文，配方记号除外。
6. **逻辑优先、可 quick start**：先让读者快速抓住主线，再展开细节——每节先写「这一块在解决什么、从哪到哪」的引言，关键论文用 `.deep` 标出来当锚点；读者只看引言 + 锚点就能建立脉络，不必从第一篇啃起。

## 三层阅读（初级 / 中级 / 高级）

每份 HTML 顶部放一个「脉络 / 完整 / 深读」三档切换，让初学者能 quick start、老手能看全：

- **初级（脉络）**：只显示 `.deep` 关键论文（+ 每节的 trend 引言和章节标题）。读者只看这一档就能抓住行业主线——这是「最关键的几篇」，不是所有论文。
- **中级（完整）**：显示全部论文（默认档）。
- **高级（深读）**：全部论文 + 底部 `.note` 的「说明 / 交叉引用 / 哪些读了原文哪些只看标题」脚注。

写法约束：<b>真正奠定脉络的节点性论文</b>（源头 / 地基 / 转折 / 引爆点）用 `<div class="deep">` 包住，数量克制——每个主题通常 3~8 篇，宁缺毋滥；其余论文用普通 `<p class="paper">`。判断标准：删掉这篇，这条线的「从哪到哪」就断了，它就该是 `.deep`。顶部三档按钮照抄已有文件，过滤逻辑统一放 `assets/js/main.js`，页面用 `<script src="../assets/js/main.js" defer></script>` 引用，不要内联 JS。

## 检索与核实流程

> **先找 survey**：arXiv 上往往已有该领域的 survey / 综述论文，这类 PDF 要重点优先读——它直接给你一套分类体系、共识与分歧、以及一份现成的参考文献清单，能省掉大量从零找论文、猜脉络的功夫。读完 survey 再拿它的引用清单做交叉比对，命中率最高。

1. 去读原文（摘要 + 参考文献），不是只看标题。
2. 交叉引用找缺口：拉几篇「hub 论文」的参考文献（arXiv 的 ar5iv HTML、Semantic Scholar Graph API），跟已有清单 diff，找漏掉的关键论文——范式「地基」最容易被漏。
3. 查 follow-up / 续作（被引方向），别漏（曾漏过 R2D2 → Fast-R2D2）。
4. 核实再写：arXiv / venue / 作者回原文或搜索引擎核对，不许编。近期用 arXiv，经典用 aclanthology / JMLR / DOI。
5. 拿不准的元数据在文末 `<p class="note">` 说明，别硬给可能错的链接。

## 交付

- 直接手写 HTML（不要 Markdown 转 HTML），风格对齐 `surveys/` 下已有文件。CSS 不内联，统一引用共享样式：入口页 `assets/css/main.css`、速览页 `../assets/css/main.css`；JS 不内联，统一引用 `../assets/js/main.js`。
- **数学公式用 MathJax 渲染**。写法：LaTeX 放在 `$…$`（行内）或 `$$…$$`（独立行）。每页 `<head>` 在 `<script src="../assets/js/main.js" defer></script>` 前配置 `window.MathJax` 并引用：
  - `<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" defer></script>`
- **配方 / 伪公式里的数学记号一律写 LaTeX**，别再用 Unicode 伪上标：`O(n²)` 写 `$O(n^2)$`、`O(n√n)` 写 `$O(n\sqrt{n})$`、`k·vᵀ` 写 `$k\cdot v^{\top}$`、希腊字母 `ε / φ / γ / β` 写 `$\varepsilon$` 等。配方里非数学的箭头仍用 `-&gt;`。
- HTML 成品放 `surveys/<topic>.html`，台账放 `data/<topic>.jsonl`；更新根目录 `index.html` 和 `README.md` 的索引。

## 论文台账（每个主题一份 JSONL）

每个主题一份 `data/<topic>.jsonl`，一行一篇，是**决策日志**——不只是「写了什么」，而是凡是你打开看过、读过的论文，无论最终进不进 HTML，都要 append 一行。

字段（一行一个 JSON 对象，`ensure_ascii=False`）：

| 字段 | 含义 |
|---|---|
| `topic` | 主题名（与 jsonl 文件名一致）|
| `id` | arXiv 号 / venue 号；没有就写标题 |
| `title` | 标题 |
| `url` | 链接（可空）|
| `status` | `in`（写进 HTML）或 `out`（看过但没写进 HTML）|
| `section` | 在 HTML 里的章节（`out` 可空）|
| `about` | 这篇讲了什么（问题 / 方法 / 核心）|
| `why` | 为什么这么处置：`in` 写为什么选进 HTML；`out` 写为什么没进 |
| `revisit` | 什么时候重新考虑：`out` 写「满足什么条件就挪回 HTML」；`in` 写「出现什么信号就挪出」|

核心用途是**重要性会随时间翻转**：

- 现在看起来不重要、没写进 HTML 的，`revisit` 记下「什么条件成立就值得挪回来」，以后翻这个 jsonl 就能想起它，而不是丢在历史里。
- 现在写进 HTML、看似重要的，`revisit` 记下「什么信号（无法复现 / 无法 scale / 被证伪）就该挪出去」，反过来也能及时降级。

流程约束：每读一篇（尤其交叉引用时顺手打开的那些），先判断进不进 HTML，再**不管进不进都 append 一行**；`out` 的一行必须写清「为什么没进」和「什么条件下回炉」，不能只写「不重要」这种空话。
