# -*- coding: utf-8 -*-
"""검토에서 나온 결함 수정
 1) 인쇄물(워크북)에 {{키}}가 그대로 나오는 문제 → [라벨]로 바꿔 인쇄
 2) 학생 화면에서 why·expect·기록칸·체크리스트의 {{키}}가 치환되지 않던 문제
 3) 공용 PC에서 앞사람 기록으로 그냥 이어지는 문제 → 이어하기 안내 띠
 4) A3·B1·B3 시작 전 약속에 개인정보 문장 보강
"""
import io, os, sys, json, glob

REPO = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")

def patch(path, pairs, name):
    s = io.open(path, encoding="utf-8").read()
    for old, new, what in pairs:
        if old not in s:
            print("  !! [%s] 찾지 못함: %s" % (name, what)); sys.exit(1)
        s = s.replace(old, new, 1)
        print("  ✔ [%s] %s" % (name, what))
    io.open(path, "w", encoding="utf-8").write(s)

# ── 1) build_all.py : 인쇄물 라벨 치환 ────────────────────────────────
p = os.path.join(REPO, "_템플릿", "build_all.py")
patch(p, [(
 "# ---------------- 학생용 워크북 ----------------",
 '''def lbl(m, text):
    """인쇄물에서는 {{키}}를 [보이는 이름]으로 바꿔 학생이 무엇을 채울지 알게 한다."""
    if not text: return text
    names = {x["k"]: x["label"] for x in m.get("mats", [])}
    return re.sub(r"\\{\\{(\\w+)\\}\\}", lambda mo: "[" + names.get(mo.group(1), mo.group(1)) + "]", text)

# ---------------- 학생용 워크북 ----------------''',
 "lbl() 추가"),
 ('        if st.get("why"): para(doc, st["why"], size=9.5, color="5B6675", sa=5)',
  '        if st.get("why"): para(doc, lbl(m, st["why"]), size=9.5, color="5B6675", sa=5)',
  "why 치환"),
 ('                box(doc, [p.get("label", "")] + p["text"].split("\\n"),',
  '                box(doc, [p.get("label", "")] + lbl(m, p["text"]).split("\\n"),',
  "프롬프트 치환"),
 ('            box(doc, st["expect"].split("\\n"), fill="FAFBFD", border="E2E6EC", size=9)',
  '            box(doc, lbl(m, st["expect"]).split("\\n"), fill="FAFBFD", border="E2E6EC", size=9)',
  "예시 치환"),
 ('                box(doc, ["[막혔을 때] " + t["when"]] + ["→ " + l for l in t["fix"].split("\\n")],',
  '                box(doc, ["[막혔을 때] " + t["when"]] + ["→ " + l for l in lbl(m, t["fix"]).split("\\n")],',
  "대처문 치환"),
 ('            writebox(doc, h, "▷ 기록 — " + st["record"]["label"])',
  '            writebox(doc, h, "▷ 기록 — " + lbl(m, st["record"]["label"]))',
  "기록칸 치환"),
 ('            for c in st["checks"]: para(doc, "☐  " + c, size=10, sa=1, indent=0.3)',
  '            for c in st["checks"]: para(doc, "☐  " + lbl(m, c), size=10, sa=1, indent=0.3)',
  "체크리스트 치환"),
], "build_all")

# ── 2) 스텝러너 : 화면에서도 why·expect·기록·체크 치환 + 이어하기 띠 ──
p = os.path.join(REPO, "_템플릿", "스텝러너_템플릿.html")
patch(p, [
 ('.savebadge{font-size:11px;',
  '''.resume{background:#fff8e6;border:1px solid #f5dfa0;border-radius:12px;padding:11px 13px;margin-bottom:12px;font-size:13.5px;color:#7a5a00;display:flex;align-items:center;gap:9px;flex-wrap:wrap;}
.resume b{color:#9a6700;}
.resume .sp{flex:1;}
.resume button{border:0;border-radius:9px;padding:7px 12px;font-size:12.5px;font-weight:700;cursor:pointer;font-family:inherit;}
.resume .no{background:#e8730c;color:#fff;}
.resume .ok{background:#eef1f6;color:#1b2330;}
.savebadge{font-size:11px;''',
  "이어하기 띠 스타일"),
 ('    <div class="progress"><i id="progBar"></i></div>',
  '    <div id="resumeBar"></div>\n    <div class="progress"><i id="progBar"></i></div>',
  "이어하기 띠 자리"),
 ('''  if(resumed){ document.getElementById("startScreen").classList.add("hidden"); go(S.idx||0); toast("이어서 진행합니다 (자동 저장된 내용)"); }''',
  '''  if(resumed){ document.getElementById("startScreen").classList.add("hidden"); go(S.idx||0); showResumeBar(); }''',
  "이어하기 처리"),
 ('/* ===================== 유틸 ===================== */',
  '''function showResumeBar(){
  const el=document.getElementById("resumeBar");
  const who=(S.student.studentName||"").trim();
  el.innerHTML='<div class="resume"><span><b>'+esc(who||"이전 사용자")+'</b> 학생이 쓰던 기록을 이어서 진행합니다.'
    +' 내가 아니라면 처음부터 시작하세요.</span><span class="sp"></span>'
    +'<button class="no" onclick="resetAll()">처음부터</button>'
    +'<button class="ok" onclick="document.getElementById(\\'resumeBar\\').innerHTML=\\'\\'">내가 맞아요</button></div>';
}

/* ===================== 유틸 ===================== */''',
  "이어하기 띠 함수"),
 ('''  h+='<p class="why'+(st.star?" star":"")+'">'+esc(st.why)+"</p>";''',
  '''  h+='<p class="why'+(st.star?" star":"")+'">'+esc(fill(st.why))+"</p>";''',
  "why 치환"),
 ('''<div class="sample">'+esc(st.expect)+"</div>''',
  '''<div class="sample">'+esc(fill(st.expect))+"</div>''',
  "예시 치환"),
 ('''    h+='<label class="fl">'+esc(st.record.label)+"</label>";''',
  '''    h+='<label class="fl">'+esc(fill(st.record.label))+"</label>";''',
  "기록칸 라벨 치환"),
 ('''placeholder="'+esc(st.record.ph||"")+'"''',
  '''placeholder="'+esc(fill(st.record.ph||""))+'"''',
  "기록칸 예시 치환"),
 ('''+(on?" checked":"")+"> <span>"+esc(c)+"</span></label></li>";''',
  '''+(on?" checked":"")+"> <span>"+esc(fill(c))+"</span></label></li>";''',
  "체크리스트 치환"),
], "스텝러너")

# ── 3) 편집기 인쇄물도 라벨 치환 ───────────────────────────────────────
p = os.path.join(REPO, "_템플릿", "모듈편집기_템플릿.html")
patch(p, [
 ("function printWorkbook(){",
  '''function lbl(t){
  if(!t) return t;
  const names={}; (M.mats||[]).forEach(x=>names[x.k]=x.label||x.k);
  return String(t).replace(/\\{\\{(\\w+)\\}\\}/g,(mo,k)=>"["+(names[k]||k)+"]");
}
function printWorkbook(){''',
  "lbl() 추가"),
 ('''    if(st.why) h+='<div class="why">'+esc(st.why)+"</div>";''',
  '''    if(st.why) h+='<div class="why">'+esc(lbl(st.why))+"</div>";''',
  "why 치환"),
 ('''(st.prompts||[]).forEach(p=>{ h+='<div class="box"><b>▶ '+esc(p.label||"")+"</b>"+esc(p.text||"")+"</div>"; });''',
  '''(st.prompts||[]).forEach(p=>{ h+='<div class="box"><b>▶ '+esc(p.label||"")+"</b>"+esc(lbl(p.text||""))+"</div>"; });''',
  "프롬프트 치환"),
 ('''if(st.expect) h+='<div class="box gray"><b>이런 답이 오면 정상입니다</b>'+esc(st.expect)+"</div>";''',
  '''if(st.expect) h+='<div class="box gray"><b>이런 답이 오면 정상입니다</b>'+esc(lbl(st.expect))+"</div>";''',
  "예시 치환"),
 ('''(st.troubles||[]).forEach(t=>{ h+='<div class="box warn"><b>[막혔을 때] '+esc(t.when)+"</b>→ "+esc(t.fix)+"</div>"; });''',
  '''(st.troubles||[]).forEach(t=>{ h+='<div class="box warn"><b>[막혔을 때] '+esc(t.when)+"</b>→ "+esc(lbl(t.fix))+"</div>"; });''',
  "대처문 치환"),
 ('''      h+="<h3>▷ 기록 — "+esc(st.record.label)+'</h3>''',
  '''      h+="<h3>▷ 기록 — "+esc(lbl(st.record.label))+'</h3>''',
  "기록칸 치환"),
 ('''(st.checks||[]).forEach(c=>{ h+='<div class="chk">☐ '+esc(c)+"</div>"; });''',
  '''(st.checks||[]).forEach(c=>{ h+='<div class="chk">☐ '+esc(lbl(c))+"</div>"; });''',
  "체크리스트 치환"),
], "모듈편집기")

# ── 4) A3·B1·B3 시작 전 약속에 개인정보 문장 보강 ──────────────────────
ADD = {
 "A3": "실제 이름 · 학번 · 연락처는 AI 입력창에 넣지 않습니다. 제출할 때 내가 직접 씁니다.",
 "B1": "실제 이름 · 학번 · 연락처는 AI 입력창에 넣지 않습니다. 슬라이드에는 마지막에 내가 직접 씁니다.",
 "B3": "실제 이름 · 학번 · 연락처는 AI 입력창에 넣지 않습니다.",
}
for f in glob.glob(os.path.join(REPO, "modules", "*.json")):
    m = json.load(io.open(f, encoding="utf-8"))
    if m["code"] in ADD:
        rules = m["intro"]["rules"]
        if not any("연락처" in r for r in rules):
            rules.insert(0, ADD[m["code"]])
            io.open(f, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
            print("  ✔ [약속] %s 개인정보 문장 추가" % m["code"])

print("\n수정 완료")
