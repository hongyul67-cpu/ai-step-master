# -*- coding: utf-8 -*-
"""읽을거리·보기 목록이 '회색 안내문'으로만 있던 문제 수정
 1) 스텝에 '활동 자료(panel)' 칸을 새로 만들어 화면·인쇄물에 또렷이 보이게
 2) 기록칸 양식(1)2)3)…)을 버튼 한 번으로 입력칸에 넣을 수 있게
"""
import io, os, sys, json

REPO = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")

def patch(path, pairs, name):
    s = io.open(path, encoding="utf-8").read()
    for old, new, what in pairs:
        if old not in s:
            print("  !! [%s] 찾지 못함: %s" % (name, what)); sys.exit(1)
        s = s.replace(old, new, 1); print("  ✔ [%s] %s" % (name, what))
    io.open(path, "w", encoding="utf-8").write(s)

# ── 1) 스텝러너 : panel 렌더 + 양식 넣기 버튼 ───────────────────────
patch(os.path.join(REPO, "_템플릿", "스텝러너_템플릿.html"), [
 (".sample{white-space:pre-wrap;",
  """.panel{border:1.5px solid #c9d6ec;background:#fbfcff;border-radius:12px;padding:13px 15px;margin:0 0 14px;}
.panel h4{margin:0 0 8px;font-size:14px;letter-spacing:-.2px;color:var(--ink);}
.panel .ln{font-size:14.5px;line-height:1.9;color:#2c3a52;}
.fillform{border:1px solid var(--line);background:#fff;color:var(--sub);border-radius:8px;padding:5px 10px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit;margin-left:6px;}
.fillform:hover{background:#f5f8fd;}
.reclabel{display:flex;align-items:center;gap:4px;flex-wrap:wrap;margin:0 0 5px;}
.sample{white-space:pre-wrap;""",
  "활동 자료 스타일"),

 ('''  if(st.noai) h+='<div class="noai">🙅 이 스텝에서는 AI를 쓰지 않습니다. 내 머리와 내 손으로 합니다.</div>';''',
  '''  if(st.noai) h+='<div class="noai">🙅 이 스텝에서는 AI를 쓰지 않습니다. 내 머리와 내 손으로 합니다.</div>';
  if(st.panel && (st.panel.lines||[]).length){
    h+='<div class="panel">'+(st.panel.title?"<h4>"+esc(fill(st.panel.title))+"</h4>":"")
      +'<div class="ln">'+st.panel.lines.map(x=>esc(fill(x))).join("<br>")+"</div></div>";
  }''',
  "활동 자료 렌더"),

 ('''    h+='<label class="fl">'+esc(fill(st.record.label))+"</label>";''',
  '''    const hasForm=(st.record.ph||"").indexOf("\\n")>=0;
    h+='<div class="reclabel"><label class="fl" style="margin:0">'+esc(fill(st.record.label))+"</label>"
      +(hasForm?'<button class="fillform" id="fillBtn">✎ 양식 채워 넣기</button>':"")+"</div>";''',
  "양식 넣기 버튼"),

 ('''  const rb=card.querySelector("#recBox");''',
  '''  const fb=card.querySelector("#fillBtn");
  if(fb) fb.addEventListener("click",()=>{
    const box=card.querySelector("#recBox");
    if(box.value.trim() && !confirm("이미 쓴 내용이 있습니다. 양식으로 바꿀까요?")) return;
    box.value=fill(st.record.ph||"");
    box.dispatchEvent(new Event("input",{bubbles:true}));
    box.focus();
  });
  const rb=card.querySelector("#recBox");''',
  "양식 넣기 동작"),
], "스텝러너")

# ── 2) 워크북(워드) : panel 과 기록 양식 인쇄 ────────────────────────
patch(os.path.join(REPO, "_템플릿", "build_all.py"), [
 ('''        if st.get("mats"):
            table(doc, [["항목", "내가 적을 내용"]] + [[x["label"], ""] for x in m["mats"]],''',
  '''        if st.get("panel") and st["panel"].get("lines"):
            box(doc, ([lbl(m, st["panel"].get("title", ""))] if st["panel"].get("title") else [])
                     + [lbl(m, x) for x in st["panel"]["lines"]],
                fill="FBFCFF", border="C9D6EC", size=11, bold_first=bool(st["panel"].get("title")))
        if st.get("mats"):
            table(doc, [["항목", "내가 적을 내용"]] + [[x["label"], ""] for x in m["mats"]],''',
  "활동 자료 인쇄"),
 ('''            writebox(doc, h, "▷ 기록 — " + lbl(m, st["record"]["label"]))''',
  '''            writebox(doc, h, "▷ 기록 — " + lbl(m, st["record"]["label"]),
                     guide=lbl(m, st["record"].get("ph", "")))''',
  "기록 양식 인쇄"),
 ('''def writebox(doc, h_cm=3.0, label=None):
    if label: para(doc, label, size=9.5, bold=True, color="5B6675", sb=4, sa=2)''',
  '''def writebox(doc, h_cm=3.0, label=None, guide=""):
    if label: para(doc, label, size=9.5, bold=True, color="5B6675", sb=4, sa=2)
    if guide and "\\n" in guide:
        for ln in guide.split("\\n"):
            para(doc, ln if ln.strip() else " ", size=9, color="9AA4B2", sa=0, indent=0.3)
        h_cm = max(1.2, h_cm - 0.35 * len(guide.split("\\n")))''',
  "기록 양식 자리"),
], "build_all")

# ── 3) 편집기 : 활동 자료 편집 + 인쇄 ────────────────────────────────
patch(os.path.join(REPO, "_템플릿", "모듈편집기_템플릿.html"), [
 ('''  f+='<div class="card"><h3>AI에게 보낼 문장</h3>''',
  '''  const pn=st.panel||{};
  f+='<div class="card"><h3>활동 자료 <span style="font-weight:400;color:#9aa4b2;font-size:12px">— 학생이 보고 판단할 목록·읽을거리</span></h3>'
    +fld("제목",pn.title,"steps."+CUR+".panel.title","비워 두면 제목 없이 상자만 나옵니다")
    +'<label class="fl">내용 (한 줄에 하나)</label><textarea data-list="steps.'+CUR+'.panel.lines" style="min-height:90px">'
    +esc((pn.lines||[]).join("\\n"))+"</textarea></div>";

  f+='<div class="card"><h3>AI에게 보낼 문장</h3>''',
  "활동 자료 편집"),
 ('''    if(st.noai) h+='<div class="box warn"><b>※ 이 스텝에서는 AI를 쓰지 않습니다.</b>내 머리와 내 손으로 합니다.</div>';''',
  '''    if(st.noai) h+='<div class="box warn"><b>※ 이 스텝에서는 AI를 쓰지 않습니다.</b>내 머리와 내 손으로 합니다.</div>';
    if(st.panel&&(st.panel.lines||[]).length){
      h+='<div class="box">'+(st.panel.title?"<b>"+esc(lbl(st.panel.title))+"</b>":"")
        +st.panel.lines.map(x=>esc(lbl(x))).join("\\n")+"</div>";
    }''',
  "활동 자료 인쇄"),
], "모듈편집기")

# ── 4) 1단계 S1 에 실제 6가지 넣기 ───────────────────────────────────
p = os.path.join(REPO, "modules", "1단계-0_AI쓰기전약속.json")
m = json.load(io.open(p, encoding="utf-8"))
s1 = m["steps"][0]
s1["panel"] = {
  "title": "이 여섯 가지, AI 입력창에 넣어도 될까요?",
  "lines": ["1)  내 이름과 학번", "2)  우리 반 인원 수", "3)  친구 전화번호",
            "4)  교과서에 나온 공식", "5)  우리 집 주소", "6)  내가 쓴 글의 초안"],
}
s1["record"]["ph"] = ("1)\n2)\n3)\n4)\n5)\n6)\n\n✕ 를 준 것들의 공통점:")
io.open(p, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
print("  ✔ [1단계] S1에 여섯 가지를 화면에 보이는 자료로 옮김")

print("\n완료")
