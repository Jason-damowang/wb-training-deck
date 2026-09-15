#!/usr/bin/env python3
"""v3.0 → v3.1：删第 2 页（培训目标）、把「能力全景」两页挪到「老板分身」之后、去掉案例里的客户名。

新页序（23 页）：
  1 封面 / 2 提问公式 / 3 WorkBuddy 是什么 / 4 岗位分身地图 / 5 销售分身 / 6 财务分身 / 7 老板分身
  / 8 11 项能力总览 / 9 四组归类 / 10–20 11 项能力逐项 / 21 场景演练 / 22 四动作 / 23 结尾

用法：python3 scripts/build-v3.1.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "workbuddy-training-v3.0.html")
OUT = os.path.join(ROOT, "workbuddy-training-v3.1.html")
TOTAL = 23
log = []

raw = open(SRC, encoding="utf-8").read()

# ---------- 1. 切成 prefix + 逐页块（含各页前面的注释）+ suffix ----------
sec_re = re.compile(r'<section[^>]*class="page"')
spans = []
for m in sec_re.finditer(raw):
    s = m.start()
    e = raw.index('</section>', s) + len('</section>')
    spans.append((s, e))
assert len(spans) == 24, len(spans)

prefix = raw[:spans[0][0]]
blocks, cursor = [], spans[0][0]   # 第 1 页之前是文档头，已单独取出
for i, (s, e) in enumerate(spans):
    lead = raw[cursor:s]
    assert re.fullmatch(r'(?:\s|<!--.*?-->)*', lead, re.S), f"第 {i+1} 页前有非注释内容"
    blocks.append(lead + raw[s:e])
    cursor = e
suffix = raw[cursor:]
log.append(("切分文档", f"prefix {len(prefix)}B / 24 页块 / suffix {len(suffix)}B"))

# ---------- 2. 删第 2 页，按新顺序重排 ----------
order = [1, 3, 4, 7, 8, 9, 10, 5, 6] + list(range(11, 22)) + [22, 23, 24]  # 1-based 原页号
assert len(order) == TOTAL and 2 not in order, order
new_blocks = [blocks[i - 1] for i in order]
log.append(("删除第 2 页「这次培训要达成什么」", "1 页"))
log.append(("重排：原 5/6（能力总览·四组归类）→ 移到原 10（老板分身）之后", "2 页"))
raw = prefix + "".join(new_blocks) + suffix

# ---------- 3. 去掉案例里的客户名 ----------
for old, new, label in [("罗莱生活 · 一次报价的真实对比", "某家纺客户 · 一次报价的真实对比", "案例标题去客户名"),
                        ("罗莱生活", "某家纺客户", "正文残留客户名")]:
    n = raw.count(old)
    if n:
        raw = raw.replace(old, new)
        log.append((label, f"{n} 处"))
assert "罗莱" not in raw, "仍有「罗莱」残留"

# ---------- 4. PART 编号按新顺序重排 ----------
for old, new in [("PART 04 · 岗位分身", "PART 03 · 岗位分身"),
                 ("PART 03 · 能力全景", "PART 04 · 能力全景")]:
    n = raw.count(old)
    assert n, old
    raw = raw.replace(old, new)
    log.append((f"PART 编号：{old} → {new}", f"{n} 处"))

# ---------- 5. 页脚重排 + 页数口径 ----------
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
raw = "".join(out) + raw[spans2[-1][1]:]   # 末页 </section> 之后还有数据包 script + 灯箱脚本，必须接回
assert pg_seen == TOTAL - 2, f"页脚数应为 {TOTAL - 2}，实际 {pg_seen}"
log.append(("页脚序号重排", f"{pg_seen} 个 → 02..{TOTAL - 1}"))

n = raw.count("/ 24")
assert n == TOTAL - 1, f"「/ 24」应为 {TOTAL - 1} 处（21 页脚 + 页码控件），实际 {n}"
raw = raw.replace("/ 24", f"/ {TOTAL}")
assert raw.count(f"/ {TOTAL}") == TOTAL - 1
log.append(("页码口径", f"{n} 处「/ 24」→「/ {TOTAL}」"))

for pat, rep, name in [(r'24 页里，把 WorkBuddy', f'{TOTAL} 页里，把 WorkBuddy', "封面副标题页数"),
                       (r'(class="v">(?:<!--pnid:[^>]*-->)?)24(<span)', rf'\g<1>{TOTAL}\g<2>', "封面统计页数"),
                       (r'· 共 24 页', f'· 共 {TOTAL} 页', "结尾页脚注页数")]:
    c = len(re.findall(pat, raw))
    assert c == 1, f"{name}: 预期 1 处，实际 {c}"
    raw = re.sub(pat, rep, raw, count=1)
    log.append((name, "1 处"))

open(OUT, "w", encoding="utf-8").write(raw)
print(f"产出 {os.path.basename(OUT)}  {os.path.getsize(OUT)} 字节\n")
for k, v in log:
    print(f"  - {k}：{v}")
