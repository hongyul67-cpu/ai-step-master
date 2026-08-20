# -*- coding: utf-8 -*-
"""전 모듈 점검 후속 수정
 ② AI 없이 하는 활동인데 'AI에게 보내세요 / 복사하기'로 보이던 것 (9곳)
 ④ AI 없이 하는 스텝에서 '어떻게 하는지'가 접혀 있던 것 → 기본으로 펼침
 ① 양식 채워 넣기 버튼 안내 문구 보강
"""
import io, os, sys, json, glob, re

REPO = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")

def patch(path, pairs, name):
    s = io.open(path, encoding="utf-8").read()
    for old, new, what in pairs:
        if old not in s:
            print("  !! [%s] 찾지 못함: %s" % (name, what)); sys.exit(1)
        s = s.replace(old, new, 1); print("  ✔ [%s] %s" % (name, what))
    io.open(path, "w", encoding="utf-8").write(s)

# ── 러너 ───────────────────────────────────────────────────────────
patch(os.path.join(REPO, "_템플릿", "스텝러너_템플릿.html"), [
 # 프롬프트 블록: AI용인지 아닌지에 따라 제목과 복사 버튼을 달리
 ('''    h+='<div class="blockhead"><span class="n">'+(++n)+'</span>AI에게 이렇게 보내세요'
      +(st.prompts.length>1?' <span style="font-weight:600;color:#b3590a">— 한 번에 하나씩</span>':"")+"</div>";
    st.prompts.forEach((p,pi)=>{
      h+='<div class="promptbox"><div class="plabel">'+esc(p.label||"")+'</div><pre>'+esc(fill(p.text))+'</pre>'
        +'<button class="copy" data-copy="'+pi+'">📋 복사하기</button></div>';
    });''',
  '''    const allNoCopy=st.prompts.every(p=>p.noCopy);
    h+='<div class="blockhead"><span class="n">'+(++n)+'</span>'
      +(allNoCopy?"이렇게 하세요":"AI에게 이렇게 보내세요")
      +((!allNoCopy&&st.prompts.length>1)?' <span style="font-weight:600;color:#b3590a">— 한 번에 하나씩</span>':"")+"</div>";
    st.prompts.forEach((p,pi)=>{
      h+='<div class="promptbox"'+(p.noCopy?' style="border-color:#dfe4ec;background:#fafbfd"':"")
        +'><div class="plabel"'+(p.noCopy?' style="color:#5b6675"':"")+'>'+esc(p.label||"")+'</div><pre>'+esc(fill(p.text))+'</pre>'
        +(p.noCopy?"":'<button class="copy" data-copy="'+pi+'">📋 복사하기</button>')+"</div>";
    });''',
  "AI 없는 활동은 복사 버튼 없이"),

 # 대처문: 프롬프트가 없거나 AI 없이 하는 스텝이면 기본으로 펼침
 ('''    h+='<details class="fold"><summary>이렇게 나왔다면? — 막혔을 때 보낼 문장</summary><div class="body">';''',
  '''    const openIt=(!st.prompts||!st.prompts.length||st.noai);
    h+='<details class="fold"'+(openIt?" open":"")+'><summary>'
      +(openIt?"이렇게 하면 됩니다":"이렇게 나왔다면? — 막혔을 때 보낼 문장")+'</summary><div class="body">';''',
  "AI 없는 스텝은 안내를 펼쳐서"),

 # 양식 버튼 문구
 ('''hasForm?'<button class="fillform" id="fillBtn">✎ 양식 채워 넣기</button>':""''',
  '''hasForm?'<button class="fillform" id="fillBtn">✎ 양식·예시 넣기</button>':""''',
  "버튼 문구"),
 ('''    box.dispatchEvent(new Event("input",{bubbles:true}));
    box.focus();''',
  '''    box.dispatchEvent(new Event("input",{bubbles:true}));
    box.focus();
    toast("예시는 지우고 내 내용으로 바꿔 쓰세요");''',
  "버튼 안내"),
], "스텝러너")

# ── 워크북(워드) ───────────────────────────────────────────────────
patch(os.path.join(REPO, "_템플릿", "build_all.py"), [
 ('''            t = "▶ AI에게 이렇게 보내세요"
            if len(st["prompts"]) > 1: t += "   (반드시 한 번에 하나씩)"''',
  '''            all_nocopy = all(p.get("noCopy") for p in st["prompts"])
            t = "▶ 이렇게 하세요" if all_nocopy else "▶ AI에게 이렇게 보내세요"
            if len(st["prompts"]) > 1 and not all_nocopy: t += "   (반드시 한 번에 하나씩)"''',
  "인쇄물 제목"),
], "build_all")

# ── 편집기 ─────────────────────────────────────────────────────────
patch(os.path.join(REPO, "_템플릿", "모듈편집기_템플릿.html"), [
 ('''      +fld("라벨",x.label,"steps."+CUR+".prompts."+i+".label")''',
  '''      +'<label class="flag"><input type="checkbox" data-nocopy="'+i+'" '+(x.noCopy?"checked":"")+'> AI에게 보내는 것이 아님 (복사 버튼 없음)</label>'
      +fld("라벨",x.label,"steps."+CUR+".prompts."+i+".label")''',
  "프롬프트 noCopy 체크"),
 ('''  const bindChk=(id,fn)=>{''',
  '''  document.querySelectorAll("[data-nocopy]").forEach(cb=>{
    cb.addEventListener("change",()=>{
      const i=+cb.dataset.nocopy;
      if(cb.checked) M.steps[CUR].prompts[i].noCopy=true; else delete M.steps[CUR].prompts[i].noCopy;
    });
  });
  const bindChk=(id,fn)=>{''',
  "noCopy 저장"),
 ('''(st.prompts||[]).forEach(p=>{ h+='<div class="box"><b>▶ '+esc(p.label||"")+"</b>"+esc(lbl(p.text||""))+"</div>"; });''',
  '''(st.prompts||[]).forEach(p=>{ h+='<div class="box'+(p.noCopy?" gray":"")+'"><b>▶ '+esc(p.label||"")+"</b>"+esc(lbl(p.text||""))+"</div>"; });''',
  "인쇄 구분"),
], "모듈편집기")

# ── 데이터: AI 없이 하는 프롬프트에 표시 ────────────────────────────
PAT = re.compile(r"AI 없이|짝이 들|짝과 바꿔|판정 기준|평가표|짝이 질문|진행 방법")
n = 0
for f in sorted(glob.glob(os.path.join(REPO, "modules", "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    m = json.load(io.open(f, encoding="utf-8")); ch = False
    for s in m["steps"]:
        for p in s.get("prompts", []):
            if p.get("noCopy"): continue
            if PAT.search((p.get("label", "") + " " + p.get("text", ""))):
                p["noCopy"] = True; ch = True; n += 1
                print("  ✔ [%s %s] %s" % (m["code"], s["no"], p.get("label", "")[:40]))
    if ch:
        io.open(f, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
print("\n프롬프트 %d곳 표시 완료" % n)
