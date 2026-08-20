# -*- coding: utf-8 -*-
"""1단계 자료(코드 0)가 제목·허브에서 자연스럽게 보이도록 손본다."""
import io, os, sys

REPO = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")

def patch(path, pairs, name):
    s = io.open(path, encoding="utf-8").read()
    for old, new, what in pairs:
        if old not in s:
            print("  !! [%s] 찾지 못함: %s" % (name, what)); sys.exit(1)
        s = s.replace(old, new, 1); print("  ✔ [%s] %s" % (name, what))
    io.open(path, "w", encoding="utf-8").write(s)

# 러너 제목 — 코드가 "0"이면 코드 표시를 뺀다
patch(os.path.join(REPO, "_템플릿", "스텝러너_템플릿.html"), [
 ('''  document.title=(m.stage?m.stage+" "+m.code+" · ":"")+m.title;''',
  '''  const headTxt=(m.stage? (m.code&&m.code!=="0" ? m.stage+" "+m.code+" · " : m.stage+" · ") : "")+m.title;
  document.title=headTxt;''',
  "제목 조립"),
 ('''  document.getElementById("barTitle").textContent=(m.stage?m.stage+" "+m.code+" · ":"")+m.title;''',
  '''  document.getElementById("barTitle").textContent=headTxt;''',
  "상단 제목"),
 ('''h+='<span class="phase">'+esc((MOD.stage||"")+" · 모듈 "+(MOD.code||""))+"</span>";''',
  '''h+='<span class="phase">'+esc((MOD.stage||"")+(MOD.code&&MOD.code!=="0"?" · 모듈 "+MOD.code:""))+"</span>";''',
  "시작 화면 배지"),
 ('''    assignmentTitle:(MOD.stage?MOD.stage+" "+MOD.code+" · ":"")+MOD.title+(S.mode==="short"?" (짧은 코스)":""),''',
  '''    assignmentTitle:(MOD.stage?(MOD.code&&MOD.code!=="0"?MOD.stage+" "+MOD.code+" · ":MOD.stage+" · "):"")+MOD.title+(S.mode==="short"?" (짧은 코스)":""),''',
  "제출 파일 제목"),
], "스텝러너")

# 허브 — 1단계 묶음을 맨 위에
patch(os.path.join(REPO, "_템플릿", "build_all.py"), [
 ('TRACKS = [("A", "A트랙 · 문서와 글쓰기"), ("B", "B트랙 · 발표")]',
  'TRACKS = [("0", "1단계 · 시작 전 약속 (10분)"),\n          ("A", "A트랙 · 문서와 글쓰기"), ("B", "B트랙 · 발표")]',
  "허브 트랙"),
 ('<h2>3단계 모듈</h2>%s',
  '<h2>모듈</h2>%s',
  "허브 제목"),
], "build_all")

# 모음 파일 화면의 트랙 목록에도
patch(os.path.join(REPO, "_템플릿", "스텝러너_템플릿.html"), [
 ('''  const tracks=[["A","A트랙 · 문서와 글쓰기"],["B","B트랙 · 발표"],["C","C트랙"],["D","D트랙"]];''',
  '''  const tracks=[["0","1단계 · 시작 전 약속 (10분)"],["A","A트랙 · 문서와 글쓰기"],["B","B트랙 · 발표"],["C","C트랙"],["D","D트랙"]];''',
  "모음 화면 트랙"),
], "스텝러너(모음)")

print("\n완료")
