# AGENTS.md

新开的 agent 在做「论文速览」之前，必须先读完这份文件。这里的规范是用户在多轮迭代里逐条敲定并纠正出来的，照做就能一次到位，不照做会被反复打回。

## 任务是什么

用户会给出「帮我梳理 <某领域> 从 <某年> 到现在的文章」，要的是一份**单文件 HTML 速览**：把论文按主题/年代系统归类，每篇用「配方（伪代码）+ 一句话」讲清楚，面向**没读过原文的初学者**，全程中文。

这是一份会**多轮迭代**的活：用户会不断要求「再多来点」「这个没覆盖到」「去核实一遍」。所以第一版就要把格式定对，后面只做增量。

## 每篇论文的固定写法

每篇论文只写两样东西，HTML 结构如下（照抄，别改）：

```html
<p class="paper"><b>论文名（作者 年份）</b>（<a href="链接">arXiv 号 / 出处</a>）<br>
<code class="recipe">flow(patch + noise) -&gt; x-pred + v-loss</code><br>
<span class="idea"><span class="p">问题</span> ……；<span class="p">方法</span> ……；<span class="p">核心</span> ……。</span></p>
```

### 配方（`<code class="recipe">`）

格式统一为 `<输入管线> -> <预测目标> + <损失/目标>`。**不写完整公式**，只写「预测什么 + 用什么损失」。

- 生成/扩散类：`flow(patch + noise) -> x-pred + v-loss`、`diffuse(vae(patch) + noise) -> ε-pred + ε-loss`、`ar(vq(patch)) -> next-token-loss`
- 句法/NLP 类：`pcfg(sentence) -> 成分树 + MLE`、`dmv(pos-seq) -> 依存树 + EM`、`spectral(sentence) -> 文法 + SVD`、`diora(sentence) -> 成分树 + 重建`
- 预测目标词汇：`ε-pred / v-pred / x-pred / consistency / next-token / score / 成分树 / 依存树 / 文法`
- 损失/目标词汇：`ε-loss / v-loss / x-loss / consistency-loss / next-token-loss / MLE / EM / ELBO / 重建 / SVD / 通信`
- 有 VAE 就写 `vae(patch)`，没有 VAE 直接写 `patch`（这是核心信息，别省略）。

### 一句话（`<span class="idea">`）

固定三段，顺序是 **问题 → 方法 → 核心**，每段都要**有信息量**：

- **问题**：它要解决什么具体问题（不是「研究了这个领域」）。
- **方法**：怎么解决的，写清关键机制（不是「提出了一个模型」）。
- **核心**：它最关键的贡献/insight 是什么（一句话能让人记住的点）。

反面教材（用户明确否掉过的空壳）：「系统梳理了 XX」「验证了可行性」「做了系统比较」——这些等于什么都没说。

## 结构记法（share / 独立）

统一/多模态模型要用记法说清「哪部分共享、哪部分独立」，让用户一眼看懂：

- `X_shared` —— X 由理解 + 生成共享
- `X_und + X_gen` —— 理解与生成各一套 X
- `X (Y_und + Y_gen)` —— X 共享，其内部 Y 拆成 und / gen 两份

例：`transformer_shared (head_lm + head_diffuse)`、`transformer (moe_und + moe_gen)`。

## 归类与趋势段

- 用 `<h3>` 分大类（按主题或年代），每个大类开头先写一段 `<p class="trend">` 的**发展趋势**：这一代/这一类在解决什么、从哪到哪、代表是什么。然后再逐篇列论文。
- 时间窗口**之前**的关键「源头 / 地基」论文也要收，单独成一节并标成「源头」，别硬塞进时间窗口。
- 文末写一节「共识与分歧」：几条共识 + 几条分歧/开放难点。

## 质量底线（用户反复纠正过的点，别踩）

1. **pred 和 loss 都要写**。只写 `v-pred` 不写是什么 loss 会被打回。
2. **一句话三段都要有**，且不能是空壳（见上）。
3. **抽象概括要落到具体条件**。像「Rosetta Stone 这样写根本看不懂」——必须写出「浅层重建 + 深层语义对齐、CLIP/DINOv2/SAM 监督」这种具体机制。
4. 面向初学者：能说人话就说人话，不堆公式、不甩术语。
5. 全文中文，配方记法里的英文记号除外。

## 检索与核实流程（用户最看重，不要只列标题）

1. **去读原文**：打开摘要 + 参考文献列表，不是只看标题。
2. **交叉引用找缺口**：拉几篇「hub 论文」的参考文献列表（arXiv 的 ar5iv HTML、Semantic Scholar Graph API 都可以），跟已有清单 diff，找出漏掉的关键论文。地基性论文（范式源头）最容易被漏。
3. **查 follow-up**：顺着被引方向找续作（漏过 R2D2 → Fast-R2D2 这种，用户会点名）。
4. **核实再写**：每个 arXiv 号 / venue / 作者都要回原文或搜索引擎核对过，不许编。近期论文用 arXiv，经典论文用 aclanthology / JMLR / DOI。
5. 拿不准元数据的论文，在文末 `<p class="note">` 里说明，别硬给一个可能错的链接。

## 交付

- **直接手写 HTML**（不要 Markdown 转 HTML），内联 CSS，单文件自包含，风格对齐 `pixel-diffusion.html` / `grammar-induction.html`。
- 成品放到本仓库根目录，更新 `index.html` 和 `README.md` 的索引。
