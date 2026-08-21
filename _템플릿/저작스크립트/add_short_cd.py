# -*- coding: utf-8 -*-
"""C·D 트랙 모듈에 1차시용 '짧은 코스(8스텝)'를 추가한다."""
import json, io, os, glob

MODDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "modules")

def P(label, text): return {"label": label, "text": text}

SHORT = {
"C1": {
 "steps": ["S1","S2","S3","S4","S5","S7","S10","S13"],
 "override": {"S7": {"prompts": [P("이렇게 보내세요",
"""방금 정리한 순서대로 웹앱을 만들어 줘. 조건은 이래.

- 파일 하나로 끝나게 만들어 줘. 따로 설치하거나 준비할 것 없이 바로 열리게.
- 화면의 글자는 모두 한국어로.
- {{limit}}
- 버튼은 손가락으로 누르기 쉽게 크게.
- 아무것도 입력하지 않고 눌렀을 때 안내 문구가 뜨게.
- 잘못 눌렀을 때 되돌릴 수 있게.
- 설명은 짧게. 코드를 먼저 보여 줘.""")]}}},

"D1": {
 "steps": ["S1","S2","S3","S4","S5","S7","S10","S13"],
 "override": {"S7": {"prompts": [P("이렇게 보내세요",
"""방금 정리한 구성대로 실제 설문 문항을 만들어 줘. 조건은 이래.

- 특정 답을 유도하는 표현을 쓰지 마. ("~이 좋다고 생각하지 않나요?" 금지)
- 한 문항에 두 가지를 묻지 마. ("재미있고 안전한가요?" 금지)
- 이름 · 학번 · 연락처는 묻지 마.
- {{who}}가 읽고 바로 이해할 수 있는 쉬운 말로.
- 고르는 문항은 보기도 함께. 보기에는 ‘잘 모르겠다’를 꼭 넣어 줘.
- 맨 앞에 두 줄짜리 안내문(왜 걷는지, 익명인지, 몇 분 걸리는지)도 만들어 줘.
- 형식: {{form}}""")]}}},

"D2": {
 "steps": ["S1","S2","S3","S5","S6","S7","S10","S13"],
 "override": {
   "S5": {"prompts": [P("이렇게 보내세요 (네 질문에 대한 답을 한 줄씩 채워서)",
"""네 질문에 짧게 답할게.
1)
2)
3)
4)
5)

이제 표는 만들지 말고, 이 선택에서 비교해 볼 만한 기준을 10개만 목록으로 줘.
- 각 줄에 [기준 이름] — [왜 중요한지 한 줄]
- 내가 말하지 않은 기준도 넣어 줘. 내가 놓친 게 있을 수 있으니까.
- 숫자로 확인할 수 있는 기준과, 느낌으로 판단하는 기준을 나눠서 표시해 줘.""")]},
   "S7": {"prompts": [P("이렇게 보내세요",
"""내가 고른 기준 3개로 비교표를 만들어 줘. 조건은 이래.

- 세로줄: 후보 ({{cand}})
- 가로줄: 내가 고른 기준 3개
- 확실하지 않은 값은 절대 지어내지 마. 모르면 반드시 "확인 필요"라고 써.
- 값 옆에 어디서 확인해야 하는지 한 단어로 표시해 줘.
- 표 아래에 ‘내가 직접 확인해야 할 것’ 목록을 따로 만들어 줘.
- 아직 결론은 내리지 마.
- 형식: {{form}}""")]},
 }},
}

for f in sorted(glob.glob(os.path.join(MODDIR, "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    m = json.load(io.open(f, encoding="utf-8"))
    sh = SHORT.get(m["code"])
    if not sh: continue
    nos = [s["no"] for s in m["steps"]]
    miss = [x for x in sh["steps"] if x not in nos]
    if miss:
        print("  ! %s 없는 스텝 지정: %s" % (m["code"], miss)); continue
    m["short"] = {
      "label": "짧은 코스 (1차시 · %d스텝)" % len(sh["steps"]),
      "steps": sh["steps"],
      "override": sh.get("override", {}),
    }
    io.open(f, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
    print("  [OK] %s 짧은 코스 %d스텝 (%s)" % (m["code"], len(sh["steps"]), " ".join(sh["steps"])))
print("완료")
