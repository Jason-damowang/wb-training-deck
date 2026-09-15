#!/usr/bin/env python3
"""v3.1 → v3.2：删除「先记一个公式」页，改掉结尾页对它的引用，并加版本号到页脚。

新页序（22 页）：
  1 封面 / 2 WorkBuddy 是什么 / 3 岗位分身地图 / 4–6 销售·财务·老板分身
  / 7 11 项能力总览 / 8 四组归类 / 9–19 11 项能力逐项 / 20 场景演练 / 21 四动作 / 22 结尾

用法：python3 scripts/build-v3.2.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "workbuddy-training-v3.1.html")
OUT = os.path.join(ROOT, "workbuddy-training-v3.2.html")
VER = "v3.2"
TOTAL = 22
log = []

raw = open(SRC, encoding="utf-8").read()

# ---------- 1. 切块（prefix + 逐页块 + suffix），删掉第 2 页 ----------
sec_re = re.compile(r'<section[^>]*class="page"')
spans = []
for m in sec_re.finditer(raw):
    s = m.start()
    spans.append((s, raw.index('</section>', s) + len('</section>')))
assert len(spans) == 23, len(spans)

prefix = raw[:spans[0][0]]
blocks, cursor = [], spans[0][0]
for i, (s, e) in enumerate(spans):
    lead = raw[cursor:s]
    assert re.fullmatch(r'(?:\s|<!--.*?-->)*', lead, re.S), f"第 {i+1} 页前有非注释内容"
    blocks.append(lead + raw[s:e])
    cursor = e
suffix = raw[cursor:]
dropped = blocks.pop(1)          # 第 2 页 = 通用提问公式
assert 'data-title="通用提问公式"' in dropped, "第 2 页不是公式页"
assert "任务 = 目标 + 材料 + 约束 + 交付物" in dropped
raw = prefix + "".join(blocks) + suffix
log.append(("删除第 2 页「先记一个公式」（提问公式页）", f"{len(dropped)} 字符"))

# ---------- 2. 改掉结尾页对「那句公式」的引用 ----------
old_sent = "手上的活，用那句公式写一遍，发给它。"
new_sent = "手上的活，把要求一次说清，发给它。"
n = raw.count(old_sent)
assert n == 1, f"结尾句引用数：{n}"
raw = raw.replace(old_sent, new_sent)
assert "那句公式" not in raw, "仍有「那句公式」残留"
log.append(("结尾页改掉「用那句公式写一遍」→「把要求一次说清」（原引用已失效）", "1 处"))

# ---------- 3. PART 编号顺延（开场页被删，后面的依次前移一位）----------
for old, new in [("PART 02 · 它是什么", "PART 01 · 它是什么"),
                 ("PART 03 · 岗位分身", "PART 02 · 岗位分身"),
                 ("PART 04 · 能力全景", "PART 03 · 能力全景"),
                 ("PART 05 · 11 项能力逐项", "PART 04 · 11 项能力逐项"),
                 ("PART 06 · 真实任务演练", "PART 05 · 真实任务演练")]:
    cnt = raw.count(old)
    assert cnt, f"找不到 {old}"
    raw = raw.replace(old, new)
    log.append((f"PART 编号：{old} → {new}", f"{cnt} 处"))

# ---------- 4. 页脚重排 + 页数口径 ----------
spans2 = [(m.start(), raw.index('</section>', m.start()) + len('</section>')) for m in sec_re.finditer(raw)]
assert len(spans2) == TOTAL, len(spans2)
out, pg_seen = [raw[:spans2[0][0]]], 0
for i, (s, e) in enumerate(spans2):
    blk = raw[s:e] if i == 0 else raw[spans2[i - 1][1]:e]
    m = re.search(r'(<span[^>]*class="pg"[^>]*>(?:<!--pnid:[^>]*-->)?)([^<]*)(</span>)', blk)
    if m:
        pg_seen += 1
        blk = blk[:m.start()] + f"{m.group(1)}{i + 1:02d}{m.group(3)}" + blk[m.end():]
    out.append(blk)
raw = "".join(out) + raw[spans2[-1][1]:]
assert pg_seen == TOTAL - 2, f"页脚数应为 {TOTAL - 2}，实际 {pg_seen}"
log.append(("页脚序号重排", f"{pg_seen} 个 → 02..{TOTAL - 1}"))

n = raw.count("/ 23")
assert n == TOTAL - 1, f"「/ 23」应为 {TOTAL - 1} 处，实际 {n}"
raw = raw.replace("/ 23", f"/ {TOTAL}")
log.append(("页码口径", f"{n} 处「/ 23」→「/ {TOTAL}」"))

for pat, rep, name in [(r'23 页里，把 WorkBuddy', f'{TOTAL} 页里，把 WorkBuddy', "封面副标题页数"),
                       (r'(class="v">(?:<!--pnid:[^>]*-->)?)23(<span)', rf'\g<1>{TOTAL}\g<2>', "封面统计页数"),
                       (r'· 共 23 页', f'· 共 {TOTAL} 页', "结尾页脚注页数")]:
    c = len(re.findall(pat, raw))
    assert c == 1, f"{name}: 预期 1 处，实际 {c}"
    raw = re.sub(pat, rep, raw, count=1)
    log.append((name, "1 处"))

# ---------- 5. 页脚加版本号（便于一眼确认打开的是哪一版）----------
brand = "WorkBuddy 基础培训 · 第一阶段「会用」"
n_brand = raw.count(brand)
assert n_brand >= 18, n_brand
raw = raw.replace(brand, f"{brand} · {VER}")
log.append((f"页脚品牌行加版本号 · {VER}", f"{n_brand} 处"))
n_end = raw.count(f'第一阶段「会用」 · 共 {TOTAL} 页')
if n_end:
    raw = raw.replace(f'第一阶段「会用」 · 共 {TOTAL} 页', f'第一阶段「会用」 · {VER} · 共 {TOTAL} 页')
    log.append((f"结尾页脚注加版本号 · {VER}", f"{n_end} 处"))

open(OUT, "w", encoding="utf-8").write(raw)
print(f"产出 {os.path.basename(OUT)}  {os.path.getsize(OUT)} 字节\n")
for k, v in log:
    print(f"  - {k}：{v}")
