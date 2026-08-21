# -*- coding: utf-8 -*-
"""기본 3가지 묶음 처리
 1) A6·A7 짧은 코스 정의 추가
 2) 러너: 모듈이 정한 기본 코스(defaultMode)를 처음 선택으로
 3) 허브·모음 화면: '기본 · 먼저 하는 3가지'를 맨 앞에 (다른 트랙에서는 제외)
"""
import json, io, os, sys, glob

REPO = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")
MODDIR = os.path.join(REPO, "modules")

def P(label, text): return {"label": label, "text": text}

SHORT = {
"A6": {"steps": ["S1","S2","S3","S4","S7","S10","S12","S13"],
 "override": {"S7": {"prompts": [P("이렇게 보내세요 (아래 [자료] 자리에 필기·유인물 내용을 붙여넣기)",
"""아래는 내 수업 자료야. 이걸로 정리 노트를 만들어 줘. 조건은 이래.

- 내가 준 자료에 있는 내용만 사용해. 자료에 없는 내용은 절대 추가하지 마.
- 네가 아는 지식으로 빈칸을 채우지 마. 자료에 없으면 [수업에서 확인]이라고 비워 둬.
- 항목은 이 순서로: 한눈에 보기 / 핵심 개념 / 용어 정리 / 헷갈리는 것 비교 / 확인 문제
- '용어 정리'와 '헷갈리는 것 비교'는 표로.
- 내가 헷갈린 것({{hard}})을 비교 표의 중심에 놓아 줘.
- 꼭 들어가야 할 말({{keyword}})이 빠지지 않게 해 줘.
- 내 수준은 {{level}}이야. 어려운 말은 쉬운 말로.
- 분량은 {{form}}.

[자료]
""")]}}},

"A7": {"steps": ["S1","S2","S3","S4","S7","S10","S12","S13"],
 "override": {"S7": {"prompts": [P("이렇게 보내세요",
"""이제 보고서를 써 줘. 조건은 이래.

- 항목은 이 순서로: 목적 / 방법 / 결과 / 해석 / 한계 / 제안
  (선생님이 요구한 항목 {{must}} 이 빠지지 않게 해 줘)
- '결과'에는 사실과 숫자만, '해석'에는 내 생각만. 둘을 섞지 마.
- '결과'는 표로 만들어 줘.
- 내가 알려준 자료에 있는 내용만 사용해. 없는 숫자·사실은 절대 지어내지 마.
- 자료가 없는 자리는 [내가 채울 것: 무엇을]이라고 비워 둬.
- 단정하는 표현(반드시, 절대)은 쓰지 마.
- 문체는 '~하였다'로 끝나는 보고서체. 분량은 {{form}}.
- 학교 이름과 내 이름은 [학교명], [이름]으로 비워 둬.""")]}}},
}

n = 0
for f in sorted(glob.glob(os.path.join(MODDIR, "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    m = json.load(io.open(f, encoding="utf-8"))
    sh = SHORT.get(m["code"])
    if not sh: continue
    m["short"] = {"label": "짧은 코스 (1차시 · %d스텝)" % len(sh["steps"]),
                  "steps": sh["steps"], "override": sh["override"]}
    io.open(f, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
    print("  ✔ %s 짧은 코스 %d스텝" % (m["code"], len(sh["steps"]))); n += 1

def patch(path, pairs, name):
    s = io.open(path, encoding="utf-8").read()
    for old, new, what in pairs:
        if old not in s:
            print("  !! [%s] 찾지 못함: %s" % (name, what)); sys.exit(1)
        s = s.replace(old, new, 1); print("  ✔ [%s] %s" % (name, what))
    io.open(path, "w", encoding="utf-8").write(s)

# 러너 — 모듈이 정한 기본 코스를 처음 선택으로
patch(os.path.join(REPO, "_템플릿", "스텝러너_템플릿.html"), [
 ("""     mats:{}, rec:{}, chk:{}, idx:0, started:false, mode:"full"};""",
  """     mats:{}, rec:{}, chk:{}, idx:0, started:false, mode:(m.defaultMode==="short"?"short":"full")};""",
  "기본 코스 적용"),
 ("""  const tracks=[["0","1단계 · 시작 전 약속 (10분)"],["A","A트랙 · 문서와 글쓰기"],["B","B트랙 · 발표"],["C","C트랙"],["D","D트랙"]];""",
  """  const basics=LIB.filter(m=>m.basic).sort((a,b)=>a.basic-b.basic);
  const tracks=[["0","1단계 · 시작 전 약속 (10분)"],["A","A트랙 · 문서와 글쓰기"],["B","B트랙 · 발표"],["C","C트랙"],["D","D트랙"]];""",
  "모음 화면 기본 묶음 준비"),
 ("""  const used=[];
  tracks.forEach(t=>{
    const g=LIB.filter(m=>String(m.code||"").startsWith(t[0]));""",
  """  const used=[];
  if(basics.length){
    basics.forEach(m=>used.push(m));
    h+='<div class="trackhd">기본 · 먼저 하는 '+basics.length+'가지</div><div class="libgrid">'+basics.map(cardHTML).join("")+"</div>";
  }
  tracks.forEach(t=>{
    const g=LIB.filter(m=>String(m.code||"").startsWith(t[0])&&used.indexOf(m)<0);""",
  "모음 화면 기본 묶음 표시"),
], "스텝러너")

# 허브 — 기본 묶음을 맨 앞에
patch(os.path.join(REPO, "_템플릿", "build_all.py"), [
 ('''def build_index(mods):
    cards = ""
    for letter, label in TRACKS:
        group = [m for m in mods if m["code"].startswith(letter)]''',
  '''def build_index(mods):
    cards = ""
    basics = sorted([m for m in mods if m.get("basic")], key=lambda x: x["basic"])
    if basics:
        cards += '\\n    <h3 class="track">기본 · 먼저 하는 %d가지</h3>' % len(basics)
        cards += _cards(basics)
    for letter, label in TRACKS:
        group = [m for m in mods if m["code"].startswith(letter) and not m.get("basic")]''',
  "허브 기본 묶음"),
 ('    rest = [m for m in mods if not any(m["code"].startswith(l) for l, _ in TRACKS)]',
  '    rest = [m for m in mods if not any(m["code"].startswith(l) for l, _ in TRACKS) and not m.get("basic")]',
  "나머지 묶음 제외"),
 ('''      <div class="mhead"><span class="code">%s</span><h3>%s</h3></div>''',
  '''      <div class="mhead"><span class="code">%s</span><h3>%s</h3>%s</div>''',
  "카드에 기본 배지 자리"),
 ('''    </div>""" % (m["code"], m["title"], m.get("desc", ""), base, m["code"], m["code"],''',
  '''    </div>""" % (m["code"], m["title"],
                 ('<span class="basic">기본 %d</span>' % m["basic"]) if m.get("basic") else "",
                 m.get("desc", ""), base, m["code"], m["code"],''',
  "카드 기본 배지 값"),
 ('.mhead h3{font-size:17px;margin:0;letter-spacing:-.3px;}',
  '.mhead h3{font-size:17px;margin:0;letter-spacing:-.3px;}\n.basic{font-size:11px;font-weight:800;background:#eaf7ec;color:#2c7a44;border:1px solid #bcdcc4;border-radius:20px;padding:2px 9px;margin-left:6px;}',
  "기본 배지 스타일"),
], "build_all")

print("\n완료 — 짧은 코스 %d개 추가" % n)
