#!/usr/bin/env python3
"""把 scripts/v3-pages.html 里的 5 个新增页装配进 v2.0，产出 v3.0。

做四件事：
  1. 把 CEO 版 08–12 页改写成的 5 个新页插入到位（「是什么」放在开场后；岗位地图 + 销售/财务/老板放在能力归类后）
  2. 页脚编号按新顺序 02..23 重排，所有「/ 24」口径统一
  3. 原有 PART 编号顺延（能力全景 02→03、逐项能力 03→05、演练 04→06）
  4. 新组件样式注入主 <style>

用法：python3 scripts/build-v3.0.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "workbuddy-training-v2.0.html")
FRAG = os.path.join(ROOT, "scripts", "v3-pages.html")
OUT = os.path.join(ROOT, "workbuddy-training-v3.0.html")
TOTAL = 24

log = []
raw = open(SRC, encoding="utf-8").read()
frag = open(FRAG, encoding="utf-8").read()

# ---------- 0. 从素材文件里切出 5 个新页 + 新 CSS ----------
frag_pages = re.findall(r'<!-- ============ NEW:.*?-->\s*(<section.*?</section>)', frag, re.S)
assert len(frag_pages) == 5, f"素材页数不对：{len(frag_pages)}"
new_css = re.search(r'<!-- ============ NEW CSS ============ -->\s*<style>(.*?)</style>', frag, re.S).group(1).strip()
log.append(("从素材文件切出新页", f"{len(frag_pages)} 页 + {len(new_css)} 字符 CSS"))

# ---------- 1. 原有 PART 编号顺延（先做，避免与新页的 PART 号撞车）----------
for old, new, name in [("PART 04 · 真实任务演练", "PART 06 · 真实任务演练", "演练页 04→06"),
                       ("PART 03 · 11 项能力逐项", "PART 05 · 11 项能力逐项", "逐项能力 03→05"),
                       ("PART 02 · 能力全景", "PART 03 · 能力全景", "能力全景 02→03")]:
    n = raw.count(old)
    assert n > 0, f"{name}: 找不到 {old}"
    raw = raw.replace(old, new)
    log.append((f"PART 编号顺延：{name}", f"{n} 处"))

# 四组归类页里那句「后 11 页逐个展开」——新增 4 页后它不再准确
old_tip = "后 11 页逐个展开。"
n_tip = raw.count(old_tip)
assert n_tip == 1, f"导语标记数不对：{n_tip}"
raw = raw.replace(old_tip, "11 项能力逐个展开。")
log.append(("修正四组归类页的导语（新增页插在中间后原说法不再准确）", "1 处"))

# ---------- 2. 插入新页 ----------
def section_starts(s):
    return [m.start() for m in re.finditer(r'<section[^>]*class="page"', s)]

starts = section_starts(raw)
assert len(starts) == 19, f"v2.0 应为 19 页，实际 {len(starts)}"

# 插入点 1：在旧第 4 页（能力总览）之前 → 新页「是什么」成为第 4 页
# 插入点 2：在旧第 6 页（FEATURE 01）之前 → 岗位地图/销售/财务/老板 成为 07–10
# 两个位置都按 v2.0 的原始坐标算，然后从后往前插，避免坐标失效
pos1 = raw.rfind('<!--', 0, starts[3])
pos2 = raw.rfind('<!--', 0, starts[5])
assert 0 < pos1 < pos2, (pos1, pos2)

block1 = "<!-- ============ 04 它是什么（CEO 08 改写）============ -->\n" + frag_pages[0] + "\n\n"
block2 = ""
for i, title in zip(range(1, 5), ["07 岗位分身地图", "08 销售分身", "09 财务分身", "10 老板分身"]):
    block2 += f"<!-- ============ {title}（CEO 09/10/11/12 改写）============ -->\n" + frag_pages[i] + "\n\n"

raw = raw[:pos2] + block2 + raw[pos2:]
raw = raw[:pos1] + block1 + raw[pos1:]
log.append(("插入新页", "1 页（是什么）→ 开场后；4 页（岗位地图/销售/财务/老板）→ 能力归类后"))

# ---------- 3. 页脚编号重排 + 页数口径统一 ----------
starts = section_starts(raw)
assert len(starts) == TOTAL, f"插入后应为 {TOTAL} 页，实际 {len(starts)}"
out, pg_seen = [raw[:starts[0]]], 0   # 第一段之前是文档头（CSS/topbar/页码控件），必须先保留
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else len(raw)
    blk = raw[s:e]
    m = re.search(r'(<span[^>]*class="pg"[^>]*>(?:<!--pnid:[^>]*-->)?)([^<]*)(</span>)', blk)
    if m:
        pg_seen += 1
        blk = blk[:m.start()] + f"{m.group(1)}{i + 1:02d}{m.group(3)}" + blk[m.end():]
    out.append(blk)
raw = "".join(out)
log.append(("页脚编号重排", f"{pg_seen} 个页脚 → 02..{TOTAL - 1}（封面/结尾无页脚）"))
assert pg_seen == TOTAL - 2, pg_seen

n = raw.count("/ 19")
assert n == 18, f"v2.0 遗留「/ 19」应为 18 处（17 页脚 + 页码控件），实际 {n}"
raw = raw.replace("/ 19", f"/ {TOTAL}")
assert raw.count(f"/ {TOTAL}") == TOTAL - 1, raw.count(f"/ {TOTAL}")
log.append(("页码口径", f"18 处「/ 19」→「/ {TOTAL}」（新页素材本身已是 / {TOTAL}）"))

# ---------- 4. 封面 / 结尾的数字 ----------
sub_once = [
    (r'19 页里，把 WorkBuddy 的 11 项核心能力', f'{TOTAL} 页里，把 WorkBuddy 的 11 项核心能力', "封面副标题页数"),
    (r'(class="v">(?:<!--pnid:[^>]*-->)?)19(<span)', rf'\g<1>{TOTAL}\g<2>', "封面统计页数"),
    (r'· 共 19 页', f'· 共 {TOTAL} 页', "结尾页脚注页数"),
]
for pat, rep, name in sub_once:
    c = len(re.findall(pat, raw))
    assert c == 1, f"{name}: 预期 1 处，实际 {c}"
    raw = re.sub(pat, rep, raw, count=1)
    log.append((name, "1 处"))

# ---------- 5. 注入新组件 CSS ----------
i = raw.find("</style>")
assert i > 0
raw = raw[:i] + "\n" + new_css + "\n" + raw[i:]
log.append(("注入新组件 CSS", f"{len(new_css)} 字符"))

open(OUT, "w", encoding="utf-8").write(raw)
print(f"产出 {os.path.basename(OUT)}  {os.path.getsize(OUT)} 字节\n")
for k, v in log:
    print(f"  - {k}：{v}")
