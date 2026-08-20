# -*- coding: utf-8 -*-
"""자동 저장이 막힌 환경(일부 브라우저·파일 직접 열기)에서 학생이 모르고 작업을 잃지 않도록 경고."""
import io, os, sys

p = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code",
                 "ai-step-master", "_템플릿", "스텝러너_템플릿.html")
s = io.open(p, encoding="utf-8").read()

def rep(old, new, what):
    global s
    if old not in s:
        print("!! 찾지 못함:", what); sys.exit(1)
    s = s.replace(old, new, 1); print("  ✔", what)

# 저장 가능 여부 판정
rep("let MOD=null, MATS=[], STEPS=[], TOTAL=0, LSKEY=\"\";",
    """const CAN_SAVE=(function(){ try{ localStorage.setItem("__t","1"); localStorage.removeItem("__t"); return true; }catch(e){ return false; } })();
let MOD=null, MATS=[], STEPS=[], TOTAL=0, LSKEY="";""",
    "저장 가능 여부 판정")

# 저장 배지에 표시
rep('''  const b=document.getElementById("saveBadge");
  b.textContent="저장됨"; b.classList.add("saving");''',
    '''  const b=document.getElementById("saveBadge");
  if(!CAN_SAVE){ b.textContent="저장 안 됨"; b.style.color="#b3590a"; b.style.background="#fff1e6"; return; }
  b.textContent="저장됨"; b.classList.add("saving");''',
    "저장 배지 표시")

# 시작 화면에 경고
rep('''  if(it.rules&&it.rules.length){''',
    '''  if(!CAN_SAVE){
    h+='<div class="card"><div class="rule" style="background:#fff1e6;border-color:#f2cfc9;color:#a5433a">'
      +'<b>⚠ 이 환경에서는 자동 저장이 되지 않습니다.</b><br>'
      +'창을 닫거나 새로 고치면 쓴 내용이 사라집니다. 중간중간 위쪽 <b>💾 임시저장</b>으로 파일을 저장해 두세요.<br>'
      +'(선생님께: 링크로 열면 자동 저장이 됩니다.)</div></div>';
  }
  if(it.rules&&it.rules.length){''',
    "시작 화면 경고")

io.open(p, "w", encoding="utf-8").write(s)
print("자동 저장 불가 경고 적용 완료")
