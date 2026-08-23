# 论文速览

多份研究速览，每篇论文用「配方（伪代码 + 损失）+ 一句话（问题 / 方法 / 核心）」的形式整理，按主题归类，面向没读过原论文的读者。

- [Pixel Diffusion 速览](surveys/pixel-diffusion.html) — 像素空间扩散 / flow，2025-08 ~ 2026-08，72 篇
- [统一多模态模型速览](surveys/unified-multimodal.html) — 理解 + 生成统一模型，Tuna 家族深读，18 篇
- [Grammar Induction / Unsupervised Parsing 速览](surveys/grammar-induction.html) — 无监督句法分析，2010 ~ 2026，81 篇
- [长上下文（Long Context）速览](surveys/long-context.html) — 稀疏/硬件高效注意力、attention sink、KV 驱逐与压缩、位置外推、训练与 benchmark，2020 ~ 2026，65 篇
- [线性注意力速览](surveys/linear-attention.html) — kernel 线性 / SSM / delta / TTT / Titans + Qwen3-Next、Kimi K3 混合旗舰，2020 ~ 2026，33 篇
- [稀疏注意力速览](surveys/sparse-attention.html) — 选 block 还是选 token + DeepSeek NSA/DSA/CSA/HCA，2019 ~ 2026，18 篇
- [递归自我改进速览](surveys/recursive-self-improvement.html) — 自训练 / 自奖励 / 自博弈 / 自纠正 / 弱到强 + AI Scientist、AlphaEvolve，2003 ~ 2026，27 篇
- [LLM 强化学习速览](surveys/llm-rl.html) — GRPO → GSPO/GEPO → DAPO + credit assignment + OPD/OPSD/MOPD，2017 ~ 2026，20 篇

> 新增论文/续写速览前，先读 [AGENTS.md](AGENTS.md)，里面是这套「配方 + 一句话」格式的完整规范。

## 目录结构

```
├── index.html          # 入口 / 导航页
├── surveys/            # 各主题速览（单文件 HTML）
├── data/               # 各主题论文台账（JSONL）
├── AGENTS.md           # 格式与流程规范
└── README.md
```

在线预览见 GitHub Pages：<https://speedcell4.github.io/ai-surveys/>
