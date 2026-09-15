# WorkBuddy 从「听说」到「会用」· 培训材料

WorkBuddy 基础培训（第一阶段「会用」）演示讲稿。单文件 HTML，可键盘翻页、可全屏，所有截图与数据包都已内嵌，打开即用。

- **在线预览（最新版 v2.0）**：https://jason-damowang.github.io/wb-training-deck/
- **当前版本**：v2.0 · `workbuddy-training-v2.0.html` · 19 页
- **历史版本**：v1.0 · `workbuddy-training-v1.0.html` · 20 页（原始版本，未做任何修改，git tag `v1.0`）

## 版本差异

| | v1.0 | v2.0 |
|---|---|---|
| 页数 | 20 页 | 19 页（删除「本周作业」页） |
| 页数口径 | 封面写 20 页 / 18 处页脚写 `/ 20` | 全部同步为 19 |
| 第 5 页 | 「后 10 页逐个展开」 | 「后 11 页逐个展开」（PART 03 实为 11 页） |
| 第 2 页提示 01 | 「不需要技术背景，不需要懂代码」 | 「不需要技术背景」（去掉重复语义） |
| 第 17 页 PPT 心得 | 「…是做出好 PPT 的唯一路径」 | 「…是做出好 PPT 最稳的路径」 |

逐条改动说明见 [CHANGELOG.md](CHANGELOG.md)。

## 仓库结构

```
wb-training-deck/
├── workbuddy-training-v2.0.html   # 当前版本（源）：6.9 MB，内嵌 29 张截图 + 1.1 MB 销售数据 zip
├── workbuddy-training-v1.0.html   # 历史版本 v1.0（原始素材，勿改）
├── index.html                     # 跳转到当前版本，供 Pages 根路径直接访问
├── docs/                          # 从当前版本派生的提取文本
│   ├── prompts.md                 # 14 条可照抄提示词（逐字提取自 data-pmt 属性）
│   ├── content-extract.md         # 提示词 + 逐页正文的合并提取版
│   └── full-text.txt              # 纯文本（去标签、去 base64）
├── scripts/
│   └── extract-docs.py            # 重新生成 docs/ 的脚本（改完 HTML 后跑一次即可）
├── CHANGELOG.md
└── .nojekyll
```

## 内容地图（v2.0，共 19 页）

| 部分 | 页 | 内容 |
|---|---|---|
| PART 01 开场 | 1–3 | 4 个可验收目标、提问公式：目标 + 材料 + 约束 + 交付物 |
| PART 02 能力全景 | 4–5 | 11 项核心能力按四组归类（能力扩展 / 记忆与上下文 / 自动化与连接 / 协作与资产） |
| PART 03 能力逐项 | 6–16 | 11 项能力，每项「解决什么问题 → 怎么用三步 → 可照抄提示词 + 截图」 |
| PART 04 场景演练 | 17–18 | PPT 制作 / 数据分析 / 会议纪要三类场景各四步；通用四动作：选能力 → 给材料 → 看中间结果 → 收口沉淀 |
| PART 05 收尾 | 19 | 结尾页（v2.0 已删除原第 19 页「本周作业」，收束由结尾页承担） |

## 改内容时的注意点

1. **只改当前版本的 HTML**（`workbuddy-training-v2.0.html`），`docs/` 下是从它派生的产物 —— 改完跑 `python3 scripts/extract-docs.py` 同步。
2. **提示词不在 `.txt` 容器里**。页面上的提示词由 `data-pmt` 属性提供、JS 打字机动画渲染，`<div class="txt">` 是空的。改提示词要搜 `data-pmt="`，不要搜页面文字。
3. **截图是内嵌 base64**，共 29 处 `data:image/...;base64,`；换图后体积会变化，注意 GitHub 单文件 100 MB 上限（当前 6.9 MB，安全）。
4. **删/加页面要同步三处数字**：封面统计（`class="v"` 里的页数）与副标题「N 页里」、各页脚 `NN` 与 `/ N`、结尾页「共 N 页」；顶部页码控件 `#pgnum` 是 JS 动态渲染的，无需改逻辑。
5. **销售数据包**是内嵌的 base64 zip，页面上的下载按钮在本地和 Pages 下都走 Blob 下载；删掉内嵌数据后按钮会退化成跳转外链（脚本里的 `DL_URL`）。
6. 版本升级请**另存新文件**（`workbuddy-training-v2.1.html`）并更新 `index.html` 的跳转目标，历史版本保留在根目录便于对比。

## 本地预览与推送

```bash
open workbuddy-training-v2.0.html    # 直接打开，无外部依赖
git-push-github                      # 本机网络下用这个推送（自动走本地代理/候选 IP）
```
