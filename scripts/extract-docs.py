#!/usr/bin/env python3
"""从当前版本的 HTML 重新生成 docs/ 下的提取文件。

用法：
    python3 scripts/extract-docs.py [HTML 文件路径]
默认处理仓库根目录的 workbuddy-training-v2.0.html。

产出：
    docs/prompts.md         逐字提取的提示词（来自 data-pmt 属性 —— 页面上是 JS 打字机渲染的，
                            源码里的 <div class="txt"> 是空的，所以只能从属性取）
    docs/full-text.txt      去标签 / 去 base64 之后的纯文本
    docs/content-extract.md 提示词 + 逐页正文的合并版
"""
import html as H
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_HTML = "workbuddy-training-v3.2.html"

# 提示词与所在页的对应关系（顺序即 data-pmt 在文档中的出现顺序）
LABELS = [
    "01 Skill 市场 · 电子签合同审查", "02 自建 Skill · 周报生成", "03 专家团 · 销售数据分析",
    "04 记忆 · 记住我的要求", "05 工作空间 · 拜访材料整理", "06 自动化 · 每周一 9 点简报",
    "07 连接器 · 企业微信导出汇总", "08 腾讯生态 · 会议纪要入库", "09 资料库 · 目录页整理",
    "10 移动端 · 合同到期日查询", "11 项目协作 · 共享工作空间", "12 场景演练 · PPT 制作",
    "13 场景演练 · 数据分析（同 03）", "14 场景演练 · 会议纪要（企微/钉钉/飞书）",
]


def prompts(raw):
    seen, out = set(), []
    for m in re.finditer(r'data-pmt="([^"]*)"', raw):
        v = H.unescape(m.group(1))
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def plain_text(raw):
    t = re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=\s]+', '[IMG]', raw)
    t = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<(br|/p|/div|/h[1-6]|/li|/tr|/section|/td|/th|/table)\b[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = H.unescape(t)
    t = re.sub(r'[ \t\u00a0]+', ' ', t)
    return re.sub(r'\n\s*\n+', '\n', t).strip()


def main():
    html_path = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HTML)
    raw = open(html_path, encoding="utf-8", errors="replace").read()
    ver = re.search(r'v(\d+\.\d+)\.html$', html_path)
    ver = ver.group(1) if ver else "?"
    docs = os.path.join(ROOT, "docs")
    os.makedirs(docs, exist_ok=True)

    ps = prompts(raw)
    md = f"# 可照抄提示词清单（{len(ps)} 条，提取自 data-pmt 属性，版本 v{ver}）\n\n"
    md += "> 页面上这些提示词以打字机动画显示、点「复制」按钮复制；源码里的 `.txt` 容器是空的，原文存在 `data-pmt` 属性中，此清单为逐字提取。\n\n"
    for i, x in enumerate(ps):
        md += f"## {i + 1:02d} · {LABELS[i] if i < len(LABELS) else ''}\n\n```\n{x}\n```\n\n"
    open(os.path.join(docs, "prompts.md"), "w", encoding="utf-8").write(md)

    txt = plain_text(raw)
    open(os.path.join(docs, "full-text.txt"), "w", encoding="utf-8").write(txt)

    ce = f"# WorkBuddy 从「听说」到「会用」培训材料 · 内容提取（v{ver}）\n\n"
    ce += f"> 源文件：`{os.path.basename(html_path)}`；页面数：{raw.count(chr(60) + 'section')} 段；截图：{raw.count('<img')} 张\n\n"
    ce += f"## 一、可照抄提示词（共 {len(ps)} 条）\n\n"
    for i, x in enumerate(ps, 1):
        ce += f"{i}. {x}\n\n"
    ce += "## 二、逐页正文\n\n```\n" + txt + "\n```\n"
    open(os.path.join(docs, "content-extract.md"), "w", encoding="utf-8").write(ce)

    print(f"已从 {os.path.basename(html_path)} 生成 docs/：提示词 {len(ps)} 条，正文 {len(txt)} 字符")


if __name__ == "__main__":
    main()
