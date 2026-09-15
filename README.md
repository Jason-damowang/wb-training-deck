# WorkBuddy 从「听说」到「会用」· 培训材料

WorkBuddy 基础培训（第一阶段「会用」）演示讲稿。单文件 HTML，20 页，可键盘翻页、可全屏，所有截图与数据包都已内嵌，打开即用。

- **在线预览**：https://jason-damowang.github.io/wb-training-deck/
- **当前版本**：v1.0（`workbuddy-training-v1.0.html`）
- **源文件 SHA-256**：`e7cba9491b8cd860e94f8c8c63e530c4bdffb59647a15cf409e69e9258536e8a`

## 仓库结构

```
wb-training-deck/
├── workbuddy-training-v1.0.html   # 唯一的交付文件（源）：6.9 MB，内嵌 30 张截图 + 1.1 MB 销售数据 zip
├── index.html                     # 跳转到当前版本，供 Pages 根路径直接访问
├── docs/
│   ├── prompts.md                 # 14 条可照抄提示词（逐字提取自 data-pmt 属性）
│   ├── content-extract.md         # 提示词 + 逐页正文的合并提取版
│   └── full-text.txt              # 20 页纯文本（去标签、去 base64）
├── CHANGELOG.md
└── .nojekyll
```

## 内容地图

| 部分 | 页 | 内容 |
|---|---|---|
| PART 01 开场 | 1–3 | 4 个可验收目标、提问公式：目标 + 材料 + 约束 + 交付物 |
| PART 02 能力全景 | 4–5 | 11 项核心能力按四组归类（能力扩展 / 记忆与上下文 / 自动化与连接 / 协作与资产） |
| PART 03 能力逐项 | 6–16 | 11 项能力，每项「解决什么问题 → 怎么用三步 → 可照抄提示词 + 截图」 |
| PART 04 场景演练 | 17–18 | PPT 制作 / 数据分析 / 会议纪要三类场景各四步；通用四动作：选能力 → 给材料 → 看中间结果 → 收口沉淀 |
| PART 05 收尾 | 19–20 | 三项本周作业、结束页 |

## 改内容时的注意点

1. **`workbuddy-training-v1.0.html` 是唯一源文件**，`docs/` 下的提取文本是从它派生的产物 —— 改内容只改 HTML，然后重新跑提取脚本同步 `docs/`。
2. **提示词不在 `.txt` 容器里**。页面上的提示词由 `data-pmt` 属性提供、JS 打字机动画渲染，`<div class="txt">` 是空的。改提示词要搜 `data-pmt="`，不要搜页面文字。
3. **截图是内嵌 base64**，共 30 处 `data:image/...;base64,`；换图后文件体积会变化，注意 GitHub 单文件 100 MB 上限（当前 6.9 MB，安全）。
4. **销售数据包**是内嵌的 base64 zip（`Stores.csv` 等），页面上的下载按钮在本地 `file://` 和 Pages 下都走 Blob 下载；若删掉内嵌数据，按钮会退化成跳转外链（脚本里的 `DL_URL`）。
5. 版本升级请**另存新文件**（`workbuddy-training-v1.1.html`）并更新 `index.html` 的跳转目标，保留历史版本便于对比。

## 本地预览

```bash
open workbuddy-training-v1.0.html      # 直接打开即可，无外部依赖
```
