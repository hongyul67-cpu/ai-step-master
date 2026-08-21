# -*- coding: utf-8 -*-
"""모듈 JSON 내용 점검."""
import json, io, os, glob, re, collections

ROOT = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")
issues = collections.defaultdict(list)

def add(code, level, msg):
    issues[code].append((level, msg))

def walk_text(m):
    """모듈 안의 모든 사람이 읽는 문자열을 (위치, 글) 로 뽑는다."""
    out = []
    it = m.get("intro", {})
    out.append(("intro.lead", it.get("lead", "")))
    for i, x in enumerate(it.get("outcomeItems", [])): out.append(("intro.outcome%d" % i, x))
    for i, x in enumerate(it.get("rules", [])): out.append(("intro.rule%d" % i, x))
    for s in m["steps"]:
        no = s["no"]
        out.append((no + ".title", s.get("title", "")))
        out.append((no + ".why", s.get("why", "")))
        for i, p in enumerate(s.get("prompts", [])):
            out.append((no + ".prompt%d.label" % i, p.get("label", "")))
            out.append((no + ".prompt%d" % i, p.get("text", "")))
        out.append((no + ".expect", s.get("expect", "")))
        for i, t in enumerate(s.get("troubles", [])):
            out.append((no + ".trouble%d.when" % i, t.get("when", "")))
            out.append((no + ".trouble%d.fix" % i, t.get("fix", "")))
        if s.get("record"):
            out.append((no + ".record.label", s["record"].get("label", "")))
            out.append((no + ".record.ph", s["record"].get("ph", "")))
        for i, c in enumerate(s.get("checks", [])): out.append((no + ".check%d" % i, c))
        te = s.get("teach", {})
        for k in ("point", "fail", "fix"): out.append((no + ".teach." + k, te.get(k, "")))
    g = m.get("guide", {})
    out.append(("guide.intent", g.get("intent", "")))
    for i, x in enumerate(g.get("intentBox", [])): out.append(("guide.box%d" % i, x))
    for i, row in enumerate(g.get("stuck", [])):
        for j, c in enumerate(row): out.append(("guide.stuck%d.%d" % (i, j), c))
    ev = g.get("eval", {})
    for i, row in enumerate(ev.get("elements", [])):
        for j, c in enumerate(row): out.append(("eval.el%d.%d" % (i, j), c))
    for i, row in enumerate(ev.get("feedback", [])):
        for j, c in enumerate(row): out.append(("eval.fb%d.%d" % (i, j), c))
    for i, x in enumerate(ev.get("records", [])): out.append(("eval.rec%d" % i, x))
    return out

MODS = []
for f in sorted(glob.glob(os.path.join(ROOT, "modules", "*.json"))):
    if os.path.basename(f).startswith("_"): continue   # 묶음 파일 제외
    m = json.load(io.open(f, encoding="utf-8"))
    m["_f"] = os.path.basename(f)
    MODS.append(m)

codes = [m["code"] for m in MODS]
dup = [c for c, n in collections.Counter(codes).items() if n > 1]
if dup: add("전체", "치명", "모듈 코드 중복 %s — 저장 공간(localStorage)이 겹칩니다" % dup)

for m in MODS:
    c = m["code"]
    st = m["steps"]

    # 1) 스텝 번호 연속성
    want = ["S%d" % (i + 1) for i in range(len(st))]
    got = [s["no"] for s in st]
    if got != want: add(c, "높음", "스텝 번호가 S1~S%d 순서가 아님: %s" % (len(st), got))

    FULL = len(st) >= 13   # 14스텝 정규 모듈에만 적용하는 규칙들

    # 2) 뼈대 규칙
    if not any(s.get("star") for s in st): add(c, "높음", "★ 강조 스텝이 없음")
    if FULL and not any(s.get("noai") for s in st): add(c, "높음", "‘AI 없이’ 스텝이 없음")
    s3 = st[2] if len(st) > 2 else {}
    if FULL and not s3.get("star"): add(c, "보통", "S3이 ★가 아님 (모듈 간 리듬이 흔들림)")
    s12 = st[11] if len(st) > 11 else {}
    if FULL and not s12.get("noai"): add(c, "보통", "S12가 ‘AI 없이’가 아님")
    if FULL and st[0].get("mats") is not True: add(c, "높음", "S1에 재료 카드가 없음")

    # 3) 규칙 3원칙
    rules = " ".join(m["intro"].get("rules", []))
    if FULL and "기록표" not in rules: add(c, "보통", "시작 전 약속에 ‘사용 기록’ 항목이 없음")
    if not re.search(r"이름|연락처|개인정보|실명", rules): add(c, "보통", "시작 전 약속에 개인정보 항목이 없음")

    # 4) 평가 5요소 · 채점표
    ev = m.get("guide", {}).get("eval", {})
    if len(ev.get("elements", [])) != 5: add(c, "보통", "평가 요소가 5개가 아님")
    if len(ev.get("rubric", [])) != 5: add(c, "보통", "채점 기준표가 5줄이 아님")
    if len(ev.get("feedback", [])) < 4: add(c, "낮음", "피드백 문구가 4개 미만")

    # 5) 교사 메모
    miss = [s["no"] for s in st if not (s.get("teach") or {}).get("point")]
    if miss: add(c, "보통", "교사 메모 없음: %s" % ",".join(miss))

    # 6) 글 품질
    for where, txt in walk_text(m):
        if not txt: continue
        if "  " in txt.replace("\n", ""): add(c, "낮음", "이중 공백 — %s" % where)
        if txt != txt.rstrip(): add(c, "낮음", "줄 끝 공백 — %s" % where)
        if "�" in txt or "?" in txt.replace("?", ""): add(c, "높음", "깨진 문자 — %s" % where)
        if re.search(r"[가-힣]{25,}", txt.replace(" ", "")) and where.endswith(tuple("0123456789")) is False:
            pass
        for bad in ("됫", "됬", "뭬"):
            if bad in txt: add(c, "보통", "맞춤법 의심(%s) — %s" % (bad, where))
        if re.search(r"\bTODO\b|여기에 채우기|샘플텍스트", txt): add(c, "높음", "미완성 표시 — %s" % where)

    # 7) 체크 항목 길이·중복
    for s in st:
        ck = s.get("checks", [])
        if len(ck) != len(set(ck)): add(c, "보통", "%s 확인 항목 중복" % s["no"])
        for x in ck:
            if len(x) > 40: add(c, "낮음", "%s 확인 항목이 김(%d자): %s" % (s["no"], len(x), x[:30]))

    # 8) 재료 키가 프롬프트에서 실제로 쓰이는지
    keys = set(x["k"] for x in m["mats"])
    used = set()
    for s in st:
        for p in s.get("prompts", []): used |= set(re.findall(r"\{\{(\w+)\}\}", p["text"]))
        for t in s.get("troubles", []): used |= set(re.findall(r"\{\{(\w+)\}\}", t["fix"]))
    if used - keys: add(c, "치명", "정의되지 않은 재료 키 %s" % (used - keys))
    unused = keys - used
    if unused: add(c, "낮음", "프롬프트에서 한 번도 안 쓰인 재료 칸: %s" % ", ".join(sorted(unused)))

    # 9) 기록 칸 없는 스텝
    norec = [s["no"] for s in st if not s.get("record")]
    if FULL and len(norec) > 1: add(c, "보통", "기록 칸 없는 스텝이 둘 이상: %s" % ",".join(norec))

    # 10) 1단계 자료 의존 (1단계 모듈이 실제로 있으면 문제 없음)
    HAS_S1 = any(x.get("stage") == "1단계" for x in MODS)
    if not HAS_S1 and "1단계" in " ".join([s.get("why", "") for s in st]) + rules:
        add(c, "운영", "‘1단계에서 정한 약속’을 전제로 하는데 1단계 자료가 없음")

print("=" * 78)
tot = 0
for c in ["전체"] + codes:
    if c not in issues: continue
    print("\n■", c)
    for lv, msg in sorted(issues[c], key=lambda x: ["치명", "높음", "보통", "운영", "낮음"].index(x[0])):
        print("   [%s] %s" % (lv, msg)); tot += 1
print("\n총 %d건" % tot)
