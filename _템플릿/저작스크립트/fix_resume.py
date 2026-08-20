# -*- coding: utf-8 -*-
"""공용 PC 대비 — 앞사람 기록으로 그냥 이어지지 않도록 안내 띠를 넣는다."""
import io, os, sys

p = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code",
                 "ai-step-master", "_템플릿", "스텝러너_템플릿.html")
s = io.open(p, encoding="utf-8").read()

def rep(old, new, what):
    global s
    if old not in s:
        print("!! 찾지 못함:", what); sys.exit(1)
    s = s.replace(old, new, 1); print("  ✔", what)

rep(".savebadge{font-size:11px;",
    """.resume{background:#fff8e6;border:1px solid #f5dfa0;border-radius:12px;padding:11px 13px;margin-bottom:12px;font-size:13.5px;color:#7a5a00;display:flex;align-items:center;gap:9px;flex-wrap:wrap;}
.resume b{color:#9a6700;}
.resume .sp{flex:1;}
.resume button{border:0;border-radius:9px;padding:7px 12px;font-size:12.5px;font-weight:700;cursor:pointer;font-family:inherit;}
.resume .no{background:#e8730c;color:#fff;}
.resume .ok{background:#eef1f6;color:#1b2330;}
.savebadge{font-size:11px;""",
    "안내 띠 스타일")

rep('    <div class="progress"><i id="progBar"></i></div>',
    '    <div id="resumeBar"></div>\n    <div class="progress"><i id="progBar"></i></div>',
    "안내 띠 자리")

rep('''  if(resumed){ document.getElementById("startScreen").classList.add("hidden"); go(S.idx||0); toast("이어서 진행합니다 (자동 저장된 내용)"); }''',
    '''  if(resumed){ document.getElementById("startScreen").classList.add("hidden"); go(S.idx||0); showResumeBar(); }''',
    "이어하기 처리")

rep("/* ===================== 유틸 ===================== */",
    '''function showResumeBar(){
  const el=document.getElementById("resumeBar"); if(!el) return;
  const who=(S.student.studentName||"").trim();
  el.innerHTML='<div class="resume"><span><b>'+esc(who||"이전 사용자")+'</b> 학생이 쓰던 기록을 이어서 진행합니다.'
    +' 내가 아니라면 처음부터 시작하세요.</span><span class="sp"></span>'
    +'<button class="no" onclick="resetAll()">처음부터</button>'
    +'<button class="ok" onclick="this.parentNode.parentNode.innerHTML=\\'\\'">내가 맞아요</button></div>';
}

/* ===================== 유틸 ===================== */''',
    "안내 띠 함수")

io.open(p, "w", encoding="utf-8").write(s)
print("이어하기 안내 띠 적용 완료")
