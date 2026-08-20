# -*- coding: utf-8 -*-
"""스텝러너에 '짧게(1차시) / 전체(3차시)' 선택을 넣는다."""
import io, os, sys

p = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code",
                 "ai-step-master", "_템플릿", "스텝러너_템플릿.html")
s = io.open(p, encoding="utf-8").read()

def rep(old, new, what):
    global s
    if old not in s:
        print("!! 찾지 못함:", what); sys.exit(1)
    s = s.replace(old, new, 1); print("  ✔", what)

# 스타일
rep(".flow{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 4px;}",
""".modepick{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:6px;}
@media(max-width:520px){.modepick{grid-template-columns:1fr;}}
.modebtn{border:2px solid var(--line);border-radius:12px;padding:13px;background:#fff;cursor:pointer;text-align:left;font-family:inherit;}
.modebtn:hover{border-color:#bcd0f0;}
.modebtn.on{border-color:var(--brand);background:var(--soft);}
.modebtn b{display:block;font-size:14.5px;margin-bottom:3px;color:var(--ink);}
.modebtn.on b{color:var(--brand-d);}
.modebtn span{font-size:12.5px;color:var(--sub);line-height:1.5;}
.modetag{font-size:11px;font-weight:800;padding:3px 9px;border-radius:20px;background:#fff1e6;color:#b3590a;white-space:nowrap;}
.flow{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 4px;}""",
 "코스 선택 스타일")

# 상단에 코스 표시
rep('<span class="savebadge" id="saveBadge">자동 저장</span>',
    '<span class="modetag hidden" id="modeTag">짧은 코스</span>\n    <span class="savebadge" id="saveBadge">자동 저장</span>',
    "상단 코스 표시")

# 전역 + 스텝 목록 적용
rep("let MOD=null, MATS=[], STEPS=[], TOTAL=0, LSKEY=\"\";",
    "let MOD=null, MATS=[], STEPS=[], TOTAL=0, LSKEY=\"\";\nlet ALLSTEPS=[];   /* 원본 14스텝 */",
    "원본 스텝 보관")

rep("  MOD=m; MATS=m.mats||[]; STEPS=m.steps||[]; TOTAL=STEPS.length;",
    "  MOD=m; MATS=m.mats||[]; ALLSTEPS=m.steps||[];\n  applyMode();",
    "setModule에서 코스 적용")

# applyMode 함수
rep("/* ===================== 유틸 ===================== */",
"""function applyMode(){
  const sh=MOD&&MOD.short;
  if(S.mode==="short" && sh && sh.steps && sh.steps.length){
    const ov=sh.override||{};
    STEPS=sh.steps.map(no=>{
      const base=ALLSTEPS.find(x=>x.no===no);
      return base ? Object.assign({}, base, ov[no]||{}) : null;
    }).filter(Boolean);
  } else {
    STEPS=ALLSTEPS.slice();
  }
  TOTAL=STEPS.length;
  const tag=document.getElementById("modeTag");
  if(tag) tag.classList.toggle("hidden", S.mode!=="short");
}
function setMode(mode){
  S.mode=mode; applyMode(); save();
  document.querySelectorAll("[data-mode]").forEach(b=>b.classList.toggle("on", b.dataset.mode===mode));
}

/* ===================== 유틸 ===================== */""",
 "applyMode 함수")

# 시작 화면에 선택 UI
rep("""  h+='<div class="card"><h3 class="sub" style="margin-top:0">✍️ 내 정보</h3><div class="info-grid">'""",
"""  if(MOD.short&&MOD.short.steps&&MOD.short.steps.length){
    h+='<div class="card"><h3 class="sub" style="margin-top:0">⏱️ 오늘 얼마나 할까요?</h3><div class="modepick">'
      +'<button class="modebtn'+(S.mode==="short"?" on":"")+'" data-mode="short"><b>짧게 · 1차시</b>'
      +'<span>'+MOD.short.steps.length+'스텝만 합니다. 결과물까지 나오고, 뼈대 고치기·부분 수정·짝 비교는 건너뜁니다.</span></button>'
      +'<button class="modebtn'+(S.mode!=="short"?" on":"")+'" data-mode="full"><b>전체 · 3차시</b>'
      +'<span>'+ALLSTEPS.length+'스텝을 모두 합니다. 고치는 연습과 상대 입장에서 점검까지 들어갑니다.</span></button>'
      +'</div></div>';
  }
  h+='<div class="card"><h3 class="sub" style="margin-top:0">✍️ 내 정보</h3><div class="info-grid">'""",
 "시작 화면 코스 선택")

# 선택 버튼 이벤트
rep("""  ["className","studentId","studentName"].forEach(k=>{
    const el=document.getElementById("s_"+k); if(el) el.value=S.student[k]||"";
  });""",
"""  ["className","studentId","studentName"].forEach(k=>{
    const el=document.getElementById("s_"+k); if(el) el.value=S.student[k]||"";
  });
  document.querySelectorAll("[data-mode]").forEach(b=>{
    b.addEventListener("click",()=>setMode(b.dataset.mode));
  });""",
 "코스 선택 이벤트")

# 상태 초기화에 mode 포함
rep("""  S={student:Object.assign({className:"",studentId:"",studentName:""}, keepStudent()),
     mats:{}, rec:{}, chk:{}, idx:0, started:false};""",
"""  S={student:Object.assign({className:"",studentId:"",studentName:""}, keepStudent()),
     mats:{}, rec:{}, chk:{}, idx:0, started:false, mode:"full"};""",
 "상태에 코스 포함")

rep("""let S={student:{className:"",studentId:"",studentName:""}, mats:{}, rec:{}, chk:{}, idx:0, started:false};""",
    """let S={student:{className:"",studentId:"",studentName:""}, mats:{}, rec:{}, chk:{}, idx:0, started:false, mode:"full"};""",
 "초기 상태에 코스 포함")

# 이어할 때도 코스 반영
rep("  const resumed=load();",
    "  const resumed=load();\n  if(resumed) applyMode();",
 "이어하기 시 코스 반영")

# 제출 파일에 코스 표시
rep("""    assignmentTitle:(MOD.stage?MOD.stage+" "+MOD.code+" · ":"")+MOD.title,""",
    """    assignmentTitle:(MOD.stage?MOD.stage+" "+MOD.code+" · ":"")+MOD.title+(S.mode==="short"?" (짧은 코스)":""),""",
 "제출 파일에 코스 표시")

io.open(p, "w", encoding="utf-8").write(s)
print("짧은 코스 선택 적용 완료")
