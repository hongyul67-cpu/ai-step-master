# -*- coding: utf-8 -*-
"""마무리 화면에 '제출 내용 복사'(구글 폼 붙여넣기용) 버튼을 추가한다."""
import io, os, sys

p = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code",
                 "ai-step-master", "_템플릿", "스텝러너_템플릿.html")
s = io.open(p, encoding="utf-8").read()

def rep(old, new, what):
    global s
    if old not in s:
        print("!! 찾지 못함:", what); sys.exit(1)
    s = s.replace(old, new, 1); print("  ✔", what)

# 버튼
rep('''      <button class="btn btn-ok" onclick="exportSubmission()">📤 제출 파일 저장 (.json)</button>
      <p class="muted" style="margin:9px 0 0;font-size:12.5px">선생님의 <b>과제 채점·피드백 도구</b>에서 바로 열립니다.</p>''',
'''      <button class="btn btn-ok" onclick="exportSubmission()">📤 제출 파일 저장 (.json)</button>
      <p class="muted" style="margin:9px 0 0;font-size:12.5px">선생님의 <b>과제 채점·피드백 도구</b>에서 바로 열립니다.</p>
      <button class="btn btn-ghost" style="margin-top:10px" id="copySubBtn">📋 제출 내용 복사 (구글 폼에 붙여넣기)</button>
      <p class="muted" style="margin:9px 0 0;font-size:12.5px">파일 올리기가 어려우면 이걸 눌러 복사한 뒤, 선생님이 안내한 <b>구글 폼</b>에 붙여넣으세요.</p>''',
    "제출 내용 복사 버튼")

# 텍스트 만들기 + 버튼 연결
rep('''function exportSubmission(){''',
'''function submitText(){
  const L=[];
  const head=(MOD.stage?(MOD.code&&MOD.code!=="0"?MOD.stage+" "+MOD.code+" · ":MOD.stage+" · "):"")+MOD.title;
  L.push("[제출] "+head+(S.mode==="short"?" (짧은 코스)":""));
  L.push((S.student.className||"")+" "+(S.student.studentId||"")+"번 "+(S.student.studentName||""));
  L.push("");
  if(MATS.length){
    L.push("■ 재료 카드");
    MATS.forEach(m=>L.push("· "+m.label+": "+((S.mats[m.k]||"").trim()||"—")));
    L.push("");
  }
  STEPS.forEach(st=>{
    if(!st.record) return;
    L.push("■ "+st.no+" "+st.title);
    L.push(((S.rec[st.no]||"").trim())||"(비어 있음)");
    L.push("");
  });
  L.push("■ 확인 목록");
  STEPS.forEach(st=>{
    const need=(st.checks||[]).length; if(!need) return;
    const got=((S.chk[st.no]||[]).filter(Boolean)).length;
    L.push(st.no+" "+st.title+" — "+got+"/"+need+(got>=need?" ✔":""));
  });
  return L.join("\\n");
}
function exportSubmission(){''',
    "제출 텍스트 만들기")

rep('''      <button class="btn btn-ghost" style="margin-top:10px" onclick="window.print()">🖨️ 인쇄 / PDF로 저장</button>''',
'''      <button class="btn btn-ghost" style="margin-top:8px" onclick="window.print()">🖨️ 인쇄 / PDF로 저장</button>''',
    "인쇄 버튼 간격")

# showDone 에서 버튼 연결
rep('''  document.getElementById("sumBox").innerHTML=h;
  window.scrollTo({top:0,behavior:"smooth"});''',
'''  document.getElementById("sumBox").innerHTML=h;
  const cb=document.getElementById("copySubBtn");
  if(cb && !cb.dataset.bound){
    cb.dataset.bound="1";
    cb.addEventListener("click",()=>copyText(submitText(),cb));
  }
  window.scrollTo({top:0,behavior:"smooth"});''',
    "복사 버튼 연결")

io.open(p, "w", encoding="utf-8").write(s)
print("완료")
