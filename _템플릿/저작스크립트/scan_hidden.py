# -*- coding: utf-8 -*-
"""'학생이 실제로 보게 되는가' 관점에서 전 모듈을 훑는다.

보이는 곳   : why, panel, prompts(상자), record.label, checks
접혀 있는 곳: expect, troubles  (details 로 접힘 — 눌러야 보임)
사라지는 곳 : record.ph (회색 안내문 — 타이핑하면 사라짐)
"""
import json, io, os, glob, re

ROOT = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")
NUM = re.compile(r"^[\s]*([0-9]+[\).]|[·※\-]|\[|\()")

def is_scaffold(ph):
    """단순 서식(1) 2) 3), · 항목:) 인가, 아니면 진짜 내용인가"""
    lines = [l for l in ph.split("\n") if l.strip()]
    if not lines: return True
    meaty = [l for l in lines if len(l.strip()) > 14 and not l.strip().endswith(":")]
    return len(meaty) == 0

print("═" * 78)
print("① 기록칸 안내문(ph)에 '진짜 내용'이 들어가 사라질 위험이 있는 곳")
print("═" * 78)
hit1 = 0
for f in sorted(glob.glob(os.path.join(ROOT, "modules", "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    m = json.load(io.open(f, encoding="utf-8"))
    for s in m["steps"]:
        ph = (s.get("record") or {}).get("ph", "")
        if ph and not is_scaffold(ph):
            hit1 += 1
            print("  %s %s — %s" % (m["code"], s["no"], ph.replace("\n", " / ")[:88]))
if not hit1: print("  없음")

print()
print("═" * 78)
print("② AI 없이 하는 활동인데 'AI에게 보내세요 / 복사하기'로 보이는 프롬프트")
print("═" * 78)
hit2 = []
for f in sorted(glob.glob(os.path.join(ROOT, "modules", "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    m = json.load(io.open(f, encoding="utf-8"))
    for s in m["steps"]:
        for i, p in enumerate(s.get("prompts", [])):
            blob = p.get("label", "") + " " + p.get("text", "")
            if re.search(r"AI 없이|짝이 들|짝과 바꿔|판정 기준|평가표|짝이 질문|진행 방법", blob) and not p.get("noCopy"):
                hit2.append((m["code"], s["no"], i, p.get("label", "")[:40]))
                print("  %s %s prompt%d — %s" % (m["code"], s["no"], i, p.get("label", "")[:50]))
if not hit2: print("  없음")

print()
print("═" * 78)
print("③ 화면에 보이는 것이 설명(why)뿐인 스텝 — 활동 자료가 필요한지 점검")
print("═" * 78)
for f in sorted(glob.glob(os.path.join(ROOT, "modules", "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    m = json.load(io.open(f, encoding="utf-8"))
    for s in m["steps"]:
        if not s.get("prompts") and not s.get("panel") and not s.get("mats"):
            print("  %s %s %-22s (기록칸:%s 대처문:%d개)" % (
                m["code"], s["no"], s["title"][:20],
                "있음" if s.get("record") else "없음", len(s.get("troubles", []))))

print()
print("═" * 78)
print("④ 접힌 곳(예시·막혔을 때)에만 있는 핵심 안내 — 눌러야 보임")
print("═" * 78)
for f in sorted(glob.glob(os.path.join(ROOT, "modules", "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    m = json.load(io.open(f, encoding="utf-8"))
    for s in m["steps"]:
        for t in s.get("troubles", []):
            if t.get("noCopy") and not s.get("prompts"):
                print("  %s %s — [%s] %s" % (m["code"], s["no"], t["when"][:22], t["fix"][:60]))
print("\n※ ④는 'AI 없이 하는 스텝'에서 방법 안내가 접혀 있는 경우입니다.")
