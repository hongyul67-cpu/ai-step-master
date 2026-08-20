# -*- coding: utf-8 -*-
"""A트랙 모듈 저작 공통 도구."""
import json, io, os

MODDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "modules")
SUBJECT = "인공지능(AI)과 직업생활"
TEACHER = "윤홍열 선생님"

def S(no, phase, title, why, **kw):
    d = {"no": no, "phase": phase, "title": title, "why": why}
    d.update(kw)
    return d

def P(label, text):
    return {"label": label, "text": text}

def T(when, fix, noCopy=False):
    d = {"when": when, "fix": fix}
    if noCopy: d["noCopy"] = True
    return d

def R(label, ph="", big=False):
    d = {"label": label, "ph": ph}
    if big: d["big"] = True
    return d

# ---------- 모든 모듈이 공유하는 마지막 두 스텝 ----------
def std_S13(extra_note=""):
    return S("S13", 3, "AI 사용 기록표 쓰기",
      "AI를 썼다는 사실은 숨기는 게 아니라 밝히는 것입니다. 1단계에서 정한 약속이고, 평가의 근거가 됩니다." + (" " + extra_note if extra_note else ""),
      record=R("사용 기록을 채우세요",
               "· 사용한 AI:\n· 주고받은 횟수: 약    회\n· AI가 가장 도움이 된 부분:\n"
               "· AI 결과 중 내가 고친 부분:\n· 사실 확인한 내용과 방법:\n· AI에게 맡기지 않고 내가 한 일:", big=True),
      checks=["사용한 AI 이름을 적었다", "내가 고친 부분을 적었다", "확인한 사실과 방법을 적었다"],
      teach={"point": "모든 모듈에서 같은 양식을 반복해 습관으로 만든다.",
             "fail": "지난 모듈에 쓴 내용을 그대로 복사한다.",
             "fix": "이번 모듈에서 새로 한 일을 한 줄이라도 넣게 한다. 4단계 포트폴리오의 재료가 된다."})

def std_S14(title, why, criteria, record_label, record_ph, checks, teach):
    return S("S14", 3, title, why,
      prompts=[P("짝과 바꿔 읽고 판정하기 (AI 없이)", criteria)],
      record=R(record_label, record_ph, big=True),
      checks=checks, teach=teach)

# ---------- 평가 묶음 ----------
def eval_block(elements, rubric, feedback, records, note, materials):
    return {
      "outline": [
        ["평가 유형", "과정 중심 수행평가 — 결과물 40%, 과정 기록 60%"],
        ["평가 시기", "마지막 차시 종료 직후 (스텝 러너 제출 파일 기준)"],
        ["평가 자료", materials],
        ["배점", "5개 요소 × 20점 = 100점 (상 20 · 중 14 · 하 8 · 미제출 0)"],
        ["채점 도구", "‘과제 채점·피드백 도구(교사용)’에서 제출 .json을 열어 항목별로 확인"],
        ["유의 사항", note],
      ],
      "elements": elements, "rubric": rubric,
      "sheetCols": ["번호", "이름", "①", "②", "③", "④", "⑤", "합계", "피드백"],
      "sheetRows": 12, "feedback": feedback, "records": records,
    }

# ---------- 공통 규칙 ----------
BASE_RULES = [
  "실제 이름 · 학번 · 연락처 · 주소는 AI 입력창에 넣지 않습니다. 필요한 곳은 마지막에 내가 직접 씁니다.",
  "AI가 말한 숫자 · 규정 · 사실은 그대로 믿지 않고 S10에서 확인합니다.",
  "어떤 AI를 어떻게 썼는지 S13 사용 기록표에 남깁니다.",
]

PHASE_NAMES = {"1": "1차시 · 준비와 뼈대", "2": "2차시 · 초안과 고치기", "3": "3차시 · 검증과 마무리"}

def module(code, title, desc, lead, outcome_title, outcome_items, rules, mats, steps, guide,
           phases=None, phase_names=None, finish="끝까지 만들었습니다", next_note="", optional=False):
    m = {
      "formatVersion": "stepRunner-1.0",
      "code": code, "stage": "3단계", "title": title,
      "subject": SUBJECT, "teacher": TEACHER, "desc": desc,
      "intro": {
        "lead": lead,
        "phases": phases or ["1차시 · S1~S6 준비와 뼈대", "2차시 · S7~S10 초안과 확인", "3차시 · S11~S14 검증과 마무리"],
        "outcomeTitle": outcome_title, "outcomeItems": outcome_items, "rules": rules,
        "finishTitle": finish, "nextNote": next_note,
      },
      "phaseNames": phase_names or PHASE_NAMES,
      "mats": mats, "steps": steps, "guide": guide,
    }
    if optional: m["optional"] = True
    return m

def write(m, fname):
    p = os.path.join(MODDIR, fname)
    io.open(p, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
    print(fname, round(os.path.getsize(p) / 1024, 1), "KB", "| steps", len(m["steps"]))
