# -*- coding: utf-8 -*-
"""스텝러너 템플릿에 '여러 모듈 묶음(모음 파일)' 지원을 추가한다."""
import io, os, sys

p = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code",
                 "ai-step-master", "_템플릿", "스텝러너_템플릿.html")
s = io.open(p, encoding="utf-8").read()
orig = s

def rep(old, new, what):
    global s
    if old not in s:
        print("!! 찾지 못함:", what); sys.exit(1)
    s = s.replace(old, new, 1)
    print("  ✔", what)

# 1) 라이브러리 화면 스타일
rep(".flow{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 4px;}",
    """.libgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
@media(max-width:640px){.libgrid{grid-template-columns:1fr;}}
.libcard{border:1.5px solid var(--line);border-radius:13px;padding:14px;background:#fff;cursor:pointer;text-align:left;font-family:inherit;transition:.14s;}
.libcard:hover{border-color:#bcd0f0;box-shadow:0 4px 14px rgba(40,60,100,.07);}
.libcard .lc{display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.libcard .code{background:linear-gradient(135deg,var(--brand),#7aa2ff);color:#fff;font-weight:900;font-size:11.5px;padding:3px 9px;border-radius:7px;}
.libcard h4{margin:0;font-size:15.5px;letter-spacing:-.3px;flex:1;}
.libcard p{margin:0 0 10px;font-size:12.5px;color:var(--sub);line-height:1.55;}
.libcard .bar{height:6px;background:#e7ebf2;border-radius:99px;overflow:hidden;}
.libcard .bar>i{display:block;height:100%;background:linear-gradient(90deg,var(--brand),#7aa2ff);width:0;}
.libcard .st{font-size:11.5px;color:#9aa4b2;margin-top:5px;display:flex;justify-content:space-between;}
.libcard .st b{color:var(--ok);}
.trackhd{font-size:12.5px;font-weight:800;color:var(--brand-d);background:var(--soft);border:1px solid #c8d8f7;border-radius:8px;padding:5px 10px;display:inline-block;margin:16px 0 9px;}
.flow{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 4px;}""",
    "라이브러리 스타일")

# 2) 전역 변수
rep("let MOD=null, MATS=[], STEPS=[], TOTAL=0, LSKEY=\"\";",
    "let MOD=null, MATS=[], STEPS=[], TOTAL=0, LSKEY=\"\";\nlet LIB=null;   /* 모음 파일일 때 모듈 배열 */",
    "전역 LIB")

# 3) 상단 버튼
rep('<button class="iconbtn" onclick="saveWork()" title="지금까지 쓴 내용을 파일로 저장">💾 임시저장</button>',
    '<button class="iconbtn hidden" id="libBtn" onclick="showLib()" title="다른 모듈 고르기">☰ 모듈</button>\n'
    '    <button class="iconbtn" onclick="saveWork()" title="지금까지 쓴 내용을 파일로 저장">💾 임시저장</button>',
    "모듈 버튼")

# 4) 라이브러리 화면 자리
rep('  <!-- 시작 화면 -->\n  <section id="startScreen" class="hidden"></section>',
    '  <!-- 모듈 고르기 (모음 파일일 때) -->\n  <section id="libScreen" class="hidden"></section>\n\n'
    '  <!-- 시작 화면 -->\n  <section id="startScreen" class="hidden"></section>',
    "라이브러리 화면 자리")

# 5) setModule — 상태 초기화 + 학생 정보 유지
rep("""function setModule(m){
  MOD=m; MATS=m.mats||[]; STEPS=m.steps||[]; TOTAL=STEPS.length;""",
    """function keepStudent(){
  try{ return JSON.parse(localStorage.getItem("stepRunner_student")||"null") || {}; }catch(e){ return {}; }
}
function setModule(m){
  S={student:Object.assign({className:"",studentId:"",studentName:""}, keepStudent()),
     mats:{}, rec:{}, chk:{}, idx:0, started:false};
  MOD=m; MATS=m.mats||[]; STEPS=m.steps||[]; TOTAL=STEPS.length;""",
    "setModule 상태 초기화")

# 6) setModule 안에서 화면 전환할 때 라이브러리 화면도 감추기
rep('  document.getElementById("pickScreen").classList.add("hidden");\n  renderStart();',
    '  document.getElementById("pickScreen").classList.add("hidden");\n'
    '  document.getElementById("libScreen").classList.add("hidden");\n'
    '  document.getElementById("libBtn").classList.toggle("hidden", !LIB);\n'
    '  renderStart();',
    "setModule 화면 전환")

# 7) 학생 정보 기억
rep('  if(!S.student.studentName){ toast("이름을 입력해 주세요."); return; }',
    '  if(!S.student.studentName){ toast("이름을 입력해 주세요."); return; }\n'
    '  try{ localStorage.setItem("stepRunner_student", JSON.stringify(S.student)); }catch(e){}',
    "학생 정보 기억")

# 8) 라이브러리 함수 추가 (부팅 직전에 삽입)
rep("/* ===================== 부팅 ===================== */",
    """/* ===================== 모듈 묶음(모음 파일) ===================== */
function libProgress(m){
  let st=null;
  try{ st=JSON.parse(localStorage.getItem("stepRunner_"+(m.code||"MOD")+"_v1")||"null"); }catch(e){}
  const total=(m.steps||[]).length;
  if(!st || !st.started) return {started:false, idx:0, done:0, total:total};
  let done=0;
  (m.steps||[]).forEach(s=>{
    const need=(s.checks||[]).length;
    const got=(((st.chk||{})[s.no])||[]).filter(Boolean).length;
    const recOk=s.record ? (((st.rec||{})[s.no]||"").trim().length>0) : true;
    const matOk=s.mats ? (m.mats||[]).every(x=>((st.mats||{})[x.k]||"").trim()) : true;
    if(got>=need && recOk && matOk) done++;
  });
  return {started:true, idx:st.idx||0, done:done, total:total};
}
function setLibrary(arr){
  LIB=arr;
  document.getElementById("pickScreen").classList.add("hidden");
  showLib();
}
function showLib(){
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("stepScreen").classList.add("hidden");
  document.getElementById("doneScreen").classList.add("hidden");
  document.getElementById("actionbar").classList.add("hidden");
  document.getElementById("libScreen").classList.remove("hidden");
  document.getElementById("barDot").textContent="≡";
  document.getElementById("barTitle").textContent="단계별 AI 수업 — 모듈 고르기";
  document.title="단계별 AI 수업 — 모듈 모음";
  renderLib();
  window.scrollTo({top:0,behavior:"smooth"});
}
function renderLib(){
  const tracks=[["A","A트랙 · 문서와 글쓰기"],["B","B트랙 · 발표"],["C","C트랙"],["D","D트랙"]];
  let h='<div class="card"><h2 class="sec">어떤 모듈을 할까요?</h2>'
      +'<p class="muted">이 파일 하나에 모든 모듈이 들어 있습니다. 고른 모듈부터 시작하면 되고, '
      +'하던 것이 있으면 이어서 진행됩니다.</p></div>';
  const used=[];
  tracks.forEach(t=>{
    const g=LIB.filter(m=>String(m.code||"").startsWith(t[0]));
    if(!g.length) return;
    g.forEach(m=>used.push(m));
    h+='<div class="trackhd">'+esc(t[1])+'</div><div class="libgrid">'+g.map(cardHTML).join("")+"</div>";
  });
  const rest=LIB.filter(m=>used.indexOf(m)<0);
  if(rest.length) h+='<div class="trackhd">그 밖의 모듈</div><div class="libgrid">'+rest.map(cardHTML).join("")+"</div>";
  document.getElementById("libScreen").innerHTML=h;
  document.getElementById("libScreen").querySelectorAll("[data-pick]").forEach(b=>{
    b.addEventListener("click",()=>setModule(LIB[+b.dataset.pick]));
  });
  function cardHTML(m){
    const i=LIB.indexOf(m), p=libProgress(m);
    const pct=p.total? Math.round(p.done/p.total*100) : 0;
    const state=p.started ? ("이어하기 · S"+(p.idx+1)+"부터") : "시작하기";
    return '<button class="libcard" data-pick="'+i+'">'
      +'<div class="lc"><span class="code">'+esc(m.code||"")+'</span><h4>'+esc(m.title||"")+"</h4></div>"
      +"<p>"+esc(m.desc||"")+"</p>"
      +'<div class="bar"><i style="width:'+pct+'%"></i></div>'
      +'<div class="st"><span>'+esc(state)+"</span><span>"
      +(p.done? "<b>완료 "+p.done+"/"+p.total+"</b>" : "완료 0/"+p.total)+"</span></div></button>";
  }
}

/* ===================== 부팅 ===================== */""",
    "라이브러리 함수")

# 9) 부팅 — 배열이면 라이브러리
rep("""    if(raw && raw!=="null") m=JSON.parse(raw);
  }catch(e){}
  if(m){ setModule(m); return; }""",
    """    if(raw && raw!=="null") m=JSON.parse(raw);
  }catch(e){}
  if(Array.isArray(m)){ setLibrary(m); return; }
  if(m){ setModule(m); return; }""",
    "부팅 분기")

# 10) 모듈 파일 불러오기도 배열 허용
rep("""      const j=JSON.parse(r.result);
      if(!j.steps||!j.steps.length) throw 0;
      setModule(j);""",
    """      const j=JSON.parse(r.result);
      if(Array.isArray(j) && j.length && j[0].steps){ setLibrary(j); return; }
      if(!j.steps||!j.steps.length) throw 0;
      setModule(j);""",
    "불러오기 배열 허용")

io.open(p, "w", encoding="utf-8").write(s)
print("완료 —", len(orig), "→", len(s), "자")
