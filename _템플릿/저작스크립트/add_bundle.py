# -*- coding: utf-8 -*-
"""build_all.py 에 모음 파일 · 묶음 JSON · 전체 관리표(워드) 생성을 추가한다."""
import io, os, sys

p = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code",
                 "ai-step-master", "_템플릿", "build_all.py")
s = io.open(p, encoding="utf-8").read()

def rep(old, new, what):
    global s
    if old not in s:
        print("!! 찾지 못함:", what); sys.exit(1)
    s = s.replace(old, new, 1); print("  ✔", what)

# 1) 개별 HTML에 로컬 경로(__file)가 박히지 않게
rep('''def build_html(m, path, tpl):
    payload = json.dumps(m, ensure_ascii=False).replace("</", "<\\\\/")''',
    '''def clean(m):
    """저장할 때는 내부용 키(__file)를 뺀다."""
    return {k: v for k, v in m.items() if not k.startswith("__")}

def build_html(m, path, tpl):
    payload = json.dumps(clean(m), ensure_ascii=False).replace("</", "<\\\\/")''',
    "__file 제거")

# 2) 모음 파일 · 묶음 JSON · 관리표
rep("# ---------------- 모듈 편집기 ----------------",
    '''# ---------------- 모음 파일 · 묶음 JSON ----------------
BUNDLE_HTML = "단계별AI수업_전체모음.html"
BUNDLE_JSON = "_전체모듈.json"

def build_bundle(mods, tpl):
    payload = json.dumps([clean(m) for m in mods], ensure_ascii=False).replace("</", "<\\\\/")
    out = tpl.replace('<script id="moduleData" type="application/json">null</script>',
                      '<script id="moduleData" type="application/json">' + payload + '</script>')
    p1 = os.path.join(ROOT, BUNDLE_HTML)
    io.open(p1, "w", encoding="utf-8").write(out)
    p2 = os.path.join(MODDIR, BUNDLE_JSON)
    io.open(p2, "w", encoding="utf-8").write(
        json.dumps([clean(m) for m in mods], ensure_ascii=False, indent=1))
    return p1, p2

# ---------------- 전체 관리표 (교사용 워드) ----------------
def ov(m, key, default="—"):
    for row in m.get("guide", {}).get("overview", []):
        if row[0] == key: return row[1]
    return default

def build_admin(mods, path):
    doc = new_doc()
    head(doc, "단계별 AI 수업", "전체 모듈 관리표",
         "3단계 공통 과제 모듈 %d개  |  교사용 한 장 정리" % len(mods))

    para(doc, "이 수업의 전체 흐름", size=13, bold=True, sb=6, sa=3)
    table(doc, [["단계", "내용", "자료"],
                ["1단계", "AI 윤리 — 넣지 말 것 · 믿지 말 것 · 숨기지 말 것", "미제작"],
                ["2단계", "다양한 AI 맛보기 + RCIF 프롬프트", "미제작"],
                ["3단계", "공통 과제 모듈 — 같이 한 스텝씩", "모듈 %d개 (아래)" % len(mods)],
                ["4단계", "각자 주제로 다시 해 보기", "미제작"]],
          [2.0, 10.5, 4.5], size=10)

    para(doc, "모듈 목록", size=13, bold=True, sb=10, sa=3)
    rows = [["코드", "모듈", "차시", "산출물"]]
    for m in mods:
        rows.append([m["code"], m["title"], ov(m, "차시"), ov(m, "산출물")])
    table(doc, rows, [1.5, 4.2, 2.6, 8.7], size=9)

    para(doc, "모듈마다 다른 ‘장치’", size=13, bold=True, sb=10, sa=3)
    para(doc, "14스텝은 모두 같습니다. 모듈을 가르는 것은 아래 한 가지 조건입니다.",
         size=9.5, color="5B6675", sa=4)
    rows = [["코드", "이 모듈만의 장치"]]
    for m in mods:
        box_ = m.get("guide", {}).get("intentBox", [])
        rows.append([m["code"] + " " + m["title"], box_[0] if box_ else "—"])
    table(doc, rows, [3.6, 13.4], size=9)

    doc.add_page_break()
    para(doc, "모든 모듈이 쓰는 14스텝", size=13, bold=True, sa=3)
    table(doc, [["차시", "스텝", "하는 일"],
                ["1차시", "S1~S2", "재료 정리 → 역할과 상황만 알려주기 (결과물은 아직 요구하지 않음)"],
                ["", "★S3~S4", "AI가 나에게 질문하게 하고, 그 질문에 답하기"],
                ["", "S5~S6", "뼈대만 뽑고 한 번에 하나씩 고쳐 확정"],
                ["2차시", "S7", "1차 초안 — 조건을 촘촘히 걸어서"],
                ["", "S8~S9", "전체 손보기 → 부분만 고치기"],
                ["", "S10", "사실 확인 — 지어낸 곳 찾기"],
                ["3차시", "S11", "상대 입장에서 비판받기"],
                ["", "★S12", "AI 없이 내 손으로 마무리"],
                ["", "S13~S14", "사용 기록표 → 제출하고 짝과 비교"]],
          [1.6, 2.4, 13.0], size=9.5)
    para(doc, "★ S3(AI가 먼저 질문하게)과 S12(AI 없이 내 손으로)가 이 수업의 승부처입니다.",
         size=9.5, color="5B6675")

    para(doc, "권장 운영 순서", size=13, bold=True, sb=10, sa=3)
    box(doc, ["A트랙(문서) — A1 회의록 → A2 선생님께 메일 → A3 학교에 건의 → A4 체험학습 보고서 → A5 근로계약서",
              "B트랙(발표) — B1 발표자료 → B2 대본과 리허설 → B3 예상 질문",
              "낱개로 떼어 써도 됩니다. 처음이라면 A1(회의록)이 가장 쉽습니다.",
              "세 번째 모듈부터는 스텝 설명이 거의 필요 없어집니다."],
        fill="F7F9FC", border="C9D6EC", size=10)

    para(doc, "평가 공통 원칙", size=13, bold=True, sb=10, sa=3)
    box(doc, ["모든 모듈이 5개 요소 × 20점 = 100점 (상 20 · 중 14 · 하 8)입니다.",
              "기준은 ‘AI를 썼는가’가 아니라 ‘기록하고 검증했는가’입니다.",
              "AI 사용은 감점이 아니며, 기록하지 않았거나 확인 없이 제출한 것이 감점입니다.",
              "요소별 세부 기준·채점표·피드백 문구는 모듈별 교사용 운영 가이드에 있습니다."],
        fill="FFF8E6", border="F5DFA0", size=10)

    doc.add_page_break()
    para(doc, "파일과 배포", size=13, bold=True, sa=3)
    table(doc, [["무엇을", "누구에게", "어떻게"],
                ["A○·B○_*.html", "학생", "파일 하나만 주면 됩니다. 인터넷 없이 열리고 자동 저장됩니다."],
                [BUNDLE_HTML, "학생·교사", "모듈 전부가 들어 있는 파일 하나. USB 하나로 여러 모듈 수업이 가능합니다."],
                ["워드/○○_학생용_워크북.docx", "학생", "인쇄해서 나눠 줍니다. 손으로 쓰는 칸이 있습니다."],
                ["워드/○○_교사용_운영가이드.docx", "교사", "차시 운영·지도 포인트·평가 자료"],
                ["모듈편집기.html", "교사", "내용 수정과 새 모듈 만들기, 학생 배포 파일 생성"],
                ["modules/*.json", "교사", "모듈 원본. 편집기로 열어 고칩니다."],
                ["제출 .json", "교사", "‘과제 채점·피드백 도구’에서 열어 채점합니다."]],
          [4.6, 2.4, 10.0], size=9)

    para(doc, "수업 전 점검표", size=13, bold=True, sb=10, sa=3)
    for x in ["학생 기기에서 모듈 파일이 열리는지 한 대로 미리 확인했다",
              "학생들이 쓸 AI(학교 계정)에 접속되는지 확인했다",
              "복사 버튼이 동작하는지 확인했다 (안 되면 드래그 복사 안내)",
              "제출 파일 저장 위치를 학생에게 안내할 준비가 되었다",
              "제출 .json을 채점 도구에서 한 번 열어 봤다",
              "공용 PC라면 이전 학생 기록이 남아 있을 수 있음을 안내한다 (‘처음부터’ 버튼)",
              "워크북을 인쇄했다 (또는 화면으로만 진행하기로 정했다)",
              "이번 시간에 할 모듈과 차시 범위를 정했다"]:
        para(doc, "☐  " + x, size=10, sa=1, indent=0.3)

    doc.save(path); return path

# ---------------- 모듈 편집기 ----------------''',
    "모음·묶음·관리표 함수")

# 3) 허브에 모아보기 구역
rep('''<h2>교사용 도구</h2>''',
    '''<h2>모아 보기 · 관리</h2>
<div class="tool">
  <a href="단계별AI수업_전체모음.html"><b>📚 전체 모음 (파일 하나)</b><span>모듈 전부가 들어 있는 단일 파일. USB 하나로 수업할 수 있고, 진행 상황이 모듈마다 표시됩니다.</span></a>
  <a href="워드/00_전체모듈_관리표.docx"><b>📋 전체 모듈 관리표</b><span>모듈 목록·차시·산출물·장치·평가 원칙·수업 전 점검표 한 장 정리</span></a>
  <a href="modules/_전체모듈.json"><b>{ } 모듈 묶음 파일</b><span>전체 모듈 원본을 한 파일로. 백업과 일괄 편집에 씁니다.</span></a>
</div>

<h2>교사용 도구</h2>''',
    "허브 모아보기 구역")

# 4) 실행부
rep("print(build_editor(tpl))",
    '''b1, b2 = build_bundle(mods, tpl)
print(b1); print(b2)
print(build_admin(mods, os.path.join(DOCDIR, "00_전체모듈_관리표.docx")))
print(build_editor(tpl))''',
    "실행부")

io.open(p, "w", encoding="utf-8").write(s)
print("build_all.py 확장 완료")
