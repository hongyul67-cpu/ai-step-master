# -*- coding: utf-8 -*-
"""무료 제미나이로 이 수업을 할 때의 교사용 안내 — 워드 + 한 장 HTML 생성.

내용(CONTENT)과 렌더링만 여기에 두고, 워드 도구는 build_all 것을 그대로 쓴다.
build_all.py 실행 시 함께 만들어진다.
"""
import io, os

CONFIRMED = "2026-08-22"   # 아래 ‘확인한 것’ 항목을 마지막으로 대조한 날

TITLE = "무료 제미나이로 수업하기"
SUB = "학생이 무료 Gemini를 쓴다고 보고, 이 수업 자료가 실제로 어떻게 돌아가는지 정리한 것"

# ── 왜 숫자를 안 적었는가 ─────────────────────────────────────────
WHY = [
 "이 수업 자료의 프롬프트는 특정 AI에 맞춰 쓰지 않았습니다. 어떤 도구로도 돌아갑니다.",
 "다만 학생이 무료 제미나이를 쓴다면 몇 군데에서 다르게 흘러갑니다. 그 자리를 모아 둔 것이 이 문서입니다.",
 "무료 정책과 한도 숫자는 자주 바뀝니다. 그래서 이 문서에는 ‘몇 회’, ‘몇 MB’ 같은 숫자를 적지 않았습니다.",
 "대신 수업 전에 10분이면 끝나는 점검표를 넣었습니다. 숫자는 그때 선생님 눈으로 확인하는 것이 가장 정확합니다.",
]

# ── 1. 수업 전 10분 점검 ─────────────────────────────────────────
CHECK_INTRO = ("반드시 ‘학생과 같은 조건’에서 하세요. 선생님 개인 계정으로 되는 것이 "
               "학생 학교 계정에서는 안 되는 경우가 가장 흔한 사고입니다.")
CHECK = [
 ["", "확인할 것", "하는 법", "안 되면"],
 ["①", "학생이 쓸 계정으로 로그인이 되는가",
  "학생 학교 계정(또는 학생이 실제로 쓸 계정)으로 gemini.google.com 에 들어가 본다",
  "개인 계정으로 통일하거나, 정보부에 문의. 계정이 갈리면 반마다 다른 사고가 납니다"],
 ["②", "만 18세 미만 계정에서 기능이 줄어드는가",
  "학생 계정으로 들어가 파일 올리기·캔버스 버튼이 보이는지 확인",
  "보이는 기능만으로 수업 설계. 4번 표의 ‘안 될 때’ 칸대로 우회"],
 ["③", "학교 와이파이에서 열리는가",
  "교실 와이파이로 접속. 교내망 필터에 막히는 학교가 있다",
  "정보부에 도메인 허용 요청. 그동안은 워크북(종이)으로 진행 가능"],
 ["④", "사진·PDF를 올릴 수 있는가",
  "아무 사진이나 하나 올려 본다 (A5·A6에서 필요)",
  "학생이 손으로 옮겨 적기. 개인정보를 지우게 되니 오히려 낫습니다"],
 ["⑤", "캔버스(Canvas)가 있는가",
  "입력창 주변에서 캔버스 버튼을 찾아본다 (C1에서 필요)",
  "코드만 받아 다른 실행 도구로. 없으면 C1은 S1~S6만 해도 평가 가능"],
 ["⑥", "한도에 걸리면 어떤 화면이 뜨는가",
  "한 계정으로 길고 복잡한 대화를 몰아서 해 본다",
  "그 화면을 캡처해 두었다가 수업 때 미리 보여 주면 학생이 당황하지 않습니다"],
]

# ── 2. 무료에서 바뀌지 않는 것 ───────────────────────────────────
FIXED = [
 ["같은 질문에도 답이 매번 다르다",
  "2단계 R 모듈이 바로 이것을 이용합니다. ‘틀린 게 아니라 원래 그렇다’를 먼저 겪게 합니다."],
 ["사용량 한도가 있고, 길고 복잡한 대화일수록 빨리 닳는다",
  "우리 자료가 ‘한 스텝에 한 번’으로 잘게 나뉜 이유이기도 합니다. 몰아서 길게 시키지 않게 하세요."],
 ["대화가 길어지면 앞에 정한 것을 잊는다",
  "S6의 ‘③ 최종 고정’ 프롬프트가 그래서 있습니다. 건너뛰면 뒤에서 뼈대가 흔들립니다."],
 ["파일 업로드는 되더라도 따로 한도가 있다",
  "꼭 필요한 모듈(A5·A6)에서만 쓰고, 나머지는 붙여넣기로 하게 하세요."],
 ["확실하지 않은 것도 확신 있게 말한다",
  "S10(사실 확인)이 그래서 있습니다. 무료라서 그런 것이 아니라 원래 그렇습니다."],
 ["학교 계정과 개인 계정은 다르게 동작한다",
  "학교(Workspace for Education) 계정은 관리자가 켜고 끌 수 있고, 만 18세 미만은 일부 기능이 제한될 수 있습니다."],
]

# ── 3. 한도를 아끼는 운영 ────────────────────────────────────────
SAVE = [
 "한 스텝에 한 번만 보냅니다. 우리 자료가 이미 그렇게 설계되어 있습니다.",
 "새 모듈은 새 대화로 시작합니다. 앞 대화를 끌고 가면 한도가 빨리 닳고 답도 흐려집니다.",
 "파일 업로드는 A5·A6에서만. 나머지는 붙여넣기로 합니다.",
 "이 수업에서는 이미지 생성을 쓰지 않습니다. B1의 그림 자리는 [사진: 무엇] 표시로 남깁니다.",
 "한도에 걸린 학생은 짝의 화면을 함께 봅니다. 단, 스텝 러너 기록은 각자 자기 기기에 씁니다.",
 "짧은 코스(8스텝)로 하면 AI에 보내는 횟수가 절반 이하로 줄어듭니다. 한도가 걱정되면 짧은 코스부터.",
]

# ── 4. 모듈별 ────────────────────────────────────────────────────
MOD_HEAD = ["모듈", "무료로 되나", "이것만 주의", "안 될 때"]
MODS = [
 ["0 · AI 쓰기 전 약속", "그대로 됩니다",
  "S2에서 법령을 물으면 확신 있게 틀린 답이 나오는 것이 정상입니다. 그게 이 스텝의 재료입니다.",
  "—"],
 ["R · AI 고르기와 프롬프트", "그대로 됩니다",
  "‘같은 질문 두 번’은 반드시 새 대화 두 개로 하게 하세요. 같은 대화에서 두 번 물으면 앞 답에 끌려갑니다.",
  "—"],
 ["A1 · 회의록 정리", "그대로 됩니다", "메모를 붙여넣기만 하므로 한도 부담이 적습니다.", "—"],
 ["A2 · 선생님께 메일", "그대로 됩니다", "실명·학번은 [이름]으로 비우게 되어 있습니다. 그대로 지키게 하세요.", "—"],
 ["A3 · 학교에 건의하기", "그대로 됩니다",
  "숫자를 지어내는 일이 가장 잦은 모듈입니다. [조사 필요]로 비우는 규칙을 꼭 지키게 하세요.", "—"],
 ["A4 · 체험학습 보고서", "그대로 됩니다", "‘너는 그날 그곳에 가지 않았다’를 빼면 관광 안내문이 나옵니다.", "—"],
 ["A5 · 근로계약서 읽기", "사진 업로드가 필요",
  "계약서에는 이름·주소·연락처·사업자번호가 있습니다. 올리기 전에 반드시 가리게 하세요.",
  "업로드가 막히면 학생이 손으로 옮겨 적습니다. 개인정보를 스스로 지우게 되니 오히려 낫습니다."],
 ["A6 · 수업 자료 정리", "붙여넣기 권장",
  "파일을 올리기보다 필기를 붙여넣는 편이 한도도 아끼고 결과도 낫습니다.",
  "사진밖에 없으면 그때만 업로드. 안 되면 눈으로 보고 옮겨 적습니다."],
 ["A7 · 보고서 쓰기", "그대로 됩니다", "‘결과(사실)와 해석(생각)을 섞지 않기’가 핵심입니다.", "—"],
 ["B1 · 발표자료 만들기", "그대로 됩니다",
  "슬라이드는 글로만 받습니다. 이미지 생성은 쓰지 않고 [사진: 무엇] 자리만 남깁니다.",
  "만든 내용은 학생이 직접 슬라이드 도구에 옮겨 적습니다."],
 ["B2 · 발표 대본과 리허설", "그대로 됩니다",
  "녹음 파일은 절대 올리지 않습니다. 자기가 받아쓴 글만 넣습니다. (자료에도 적혀 있습니다)",
  "받아쓰기가 부담되면 [나] 짝이 들어 주는 방법으로 진행하면 됩니다."],
 ["B3 · 예상 질문 대비", "그대로 됩니다", "‘답변은 만들지 말고 질문만’ 조건을 빼면 학생이 생각할 일이 없어집니다.", "—"],
 ["C1 · 간단한 앱 만들기", "캔버스가 있으면 가장 좋음",
  "코드를 이해시키려 하지 마세요. 눌러서 되는지만 봅니다. 오류 메시지는 그대로 옮겨 붙이게 합니다.",
  "캔버스가 없으면 코드만 받아 다른 실행 도구로. 그것도 어려우면 S1~S6(순서 설계)까지만 해도 평가가 됩니다."],
 ["D1 · 설문 만들고 결과 정리", "그대로 됩니다",
  "설문을 실제로 걷는 것은 구글 폼(또는 종이)으로 따로 합니다. 제미나이와 무관합니다.",
  "결과를 못 걷으면 가상 숫자로 연습해도 됩니다. ‘가상 자료’라고 표시하게 하세요."],
 ["D2 · 비교해서 고르기", "그대로 됩니다",
  "값을 그럴듯하게 지어내는 일이 가장 잦습니다. ‘모르면 확인 필요’ 조건이 방어선입니다.",
  "검색 결과를 보여 주더라도 그대로 믿지 말고 S10에서 학생이 직접 확인하게 하세요."],
 ["P1 · 내 주제로 해보기", "그대로 됩니다", "복사할 프롬프트가 없는 모듈입니다. 학생이 직접 씁니다.", "—"],
 ["P2 · 포트폴리오", "AI를 거의 안 씁니다", "S3 한 번만 AI를 씁니다. 한도 부담이 가장 적습니다.", "—"],
]

# ── 5. 수업 중 이 말이 나오면 ────────────────────────────────────
SAY = [
 ["“한도를 다 썼대요”",
  "“지금은 짝 화면으로 같이 보고, 기록은 네 기기에 써.” 한도는 시간이 지나면 풀립니다. "
  "다음 시간에는 짧은 코스로 돌리면 됩니다."],
 ["“답이 이상해요”",
  "“무엇을 눌렀는데 무엇이 나와야 하는데 무엇이 나왔는지 세 칸으로 말해 봐.” "
  "그 문형이 C1 S8에 그대로 있습니다."],
 ["“친구랑 답이 달라요”",
  "“원래 그래. 그걸 확인하는 게 오늘 배운 거야.” 2단계 R 모듈의 결론이 바로 이것입니다."],
 ["“로그인이 안 돼요”",
  "학교 계정인지 개인 계정인지부터 확인합니다. 반마다 계정이 섞이면 사고가 커집니다."],
 ["“캔버스가 없어요”",
  "“코드만 받아 두자. 실행은 선생님 화면에서 같이 보자.” C1은 실행 없이도 절반은 평가됩니다."],
 ["“파일이 안 올라가요”",
  "“그럼 눈으로 보고 옮겨 적자.” 옮겨 적는 동안 개인정보를 스스로 지우게 됩니다."],
 ["“AI가 다 해 줬는데 왜 점수가 낮아요?”",
  "평가표를 보여 주세요. 이 수업은 결과물 40%, 과정 기록 60%입니다. "
  "S12(AI 없이 내 손으로)와 S13(사용 기록)이 점수의 중심입니다."],
]

# ── 6. 개인정보 ─────────────────────────────────────────────────
PRIV = [
 "무료 계정의 대화는 서비스 개선에 쓰일 수 있습니다. 지운다고 없던 일이 되지 않습니다.",
 "그래서 1단계 약속이 ‘넣지 말 것’으로 시작합니다 — 실명 · 학번 · 연락처 · 주소 · 계약서 원본.",
 "A5에서 계약서를 올릴 때는 이름·주소·연락처·사업자번호를 가리고 올리게 하세요.",
 "B2에서 녹음 파일은 올리지 않습니다. 자기가 받아쓴 글만 넣습니다.",
 "C1에서 만든 앱에 친구 실명을 넣지 않게 하세요. 시험용 이름은 [학생1]입니다.",
 "학생이 스스로 지운 뒤 올리는 그 과정 자체가 이 수업의 학습 내용입니다. 대신 해 주지 마세요.",
]

# ── 7. 학생에게 그대로 읽어 주는 안내 ────────────────────────────
READ = [
 "① 오늘 쓰는 AI는 무료입니다. 많이 쓰면 잠깐 막힐 수 있어요. 막히면 손 들지 말고 짝 화면을 같이 보세요.",
 "② 같은 질문을 해도 친구와 답이 다릅니다. 고장이 아닙니다.",
 "③ 이름·학번·연락처·주소는 절대 넣지 않습니다. 필요한 자리는 마지막에 여러분이 직접 씁니다.",
 "④ AI가 말한 숫자와 규정은 믿지 말고 확인합니다. 확인하는 스텝이 따로 있습니다.",
 "⑤ AI를 썼다는 건 숨기는 게 아니라 적는 겁니다. 마지막에 사용 기록표를 씁니다.",
]

# ── 8. 확인한 것 / 확인하지 않은 것 ─────────────────────────────
SOURCE_CONFIRMED = [
 "학교(Workspace for Education) 계정에서 Gemini 앱은 관리자가 조직 단위별로 켜고 끌 수 있습니다.",
 "만 18세 미만 사용자에게는 일부 기능이 제한될 수 있습니다.",
 "파일 업로드에는 별도의 사용량 한도가 있고, 그 한도는 고정된 값이 아니라 시간이 지나면 다시 풀립니다.",
 "사용량은 ‘몇 번 물었나’보다 프롬프트의 복잡도·기능·대화 길이에 따라 다르게 깎입니다.",
]
SOURCE_LINKS = [
 ["직장 또는 학교 Google 계정으로 Gemini 앱 사용하기 (Education)",
  "https://support.google.com/gemini/answer/14620100?hl=ko&co=DASHER._Family%3DEducation"],
 ["모든 연령대의 사용자를 위해 Gemini 앱 액세스 관리하기 (관리자)",
  "https://support.google.com/a/answer/16309563?hl=ko"],
 ["Gemini 앱에서 파일 업로드하고 분석하기",
  "https://support.google.com/gemini/answer/14903178?hl=ko&co=GENIE.Platform%3DDesktop"],
 ["Google AI 구독자의 Gemini 앱 한도 및 업그레이드",
  "https://support.google.com/gemini/answer/16275805?hl=ko"],
]
SOURCE_UNCONFIRMED = [
 "무료로 쓸 수 있는 정확한 횟수·용량 — 공식 문서도 ‘변동적’이라고만 밝힙니다. 1번 점검표로 직접 보세요.",
 "지금 무료에서 캔버스가 되는지 — 제공 범위가 자주 바뀝니다. 1번 점검표 ⑤번으로 확인하세요.",
 "학교 계정에서 무엇이 켜져 있는지 — 학교마다 다릅니다. 정보부에 물어보는 편이 가장 빠릅니다.",
]


# ══════════════════════════════ 워드 ══════════════════════════════
def build_docx(path):
    import build_all as B
    doc = B.new_doc()
    B.head(doc, "단계별 AI 수업 · 교사용", TITLE, SUB + "   |   대조 확인일 " + CONFIRMED)

    B.para(doc, "이 문서에 한도 숫자를 적지 않은 이유", size=12, bold=True, sb=2, sa=3)
    B.box(doc, WHY, fill="FFF8E6", border="F5DFA0", size=10)

    B.h2(doc, "1. 수업 전 10분 점검")
    B.para(doc, CHECK_INTRO, size=10, color="5B6675", sa=5)
    B.table(doc, CHECK, [1.0, 4.6, 6.2, 5.2], size=9.5, rowheight=1.0)

    B.h2(doc, "2. 무료에서 바뀌지 않는 것 6가지")
    B.table(doc, [["이런 일이 생깁니다", "그래서 이 자료는 이렇게 되어 있습니다"]] + FIXED,
            [6.0, 11.0], size=9.5)

    B.h2(doc, "3. 한도를 아끼는 수업 운영")
    B.box(doc, ["· " + s for s in SAVE], size=10)

    B.h2(doc, "4. 모듈별 — 무료 제미나이로 하면")
    B.table(doc, [MOD_HEAD] + MODS, [4.2, 2.8, 5.4, 4.6], size=9, rowheight=0.9)

    doc.add_page_break()
    B.h2(doc, "5. 수업 중 이 말이 나오면")
    B.table(doc, [["학생이 하는 말", "선생님 한 마디"]] + SAY, [4.6, 12.4], size=9.5)

    B.h2(doc, "6. 개인정보 — 무료라서 더 중요한 것")
    B.box(doc, ["· " + s for s in PRIV], fill="FFF4F4", border="F2C7C7", size=10)

    B.h2(doc, "7. 학생에게 그대로 읽어 주세요")
    B.box(doc, READ, fill="EEF7EE", border="C3E0C8", size=10.5)

    B.h2(doc, "8. 확인한 것과 확인하지 못한 것")
    B.para(doc, "공식 문서로 확인한 것", size=11, bold=True, sb=2, sa=2)
    B.box(doc, ["· " + s for s in SOURCE_CONFIRMED], size=9.5)
    B.para(doc, "확인하지 못한 것 (직접 보셔야 합니다)", size=11, bold=True, sb=4, sa=2)
    B.box(doc, ["· " + s for s in SOURCE_UNCONFIRMED], fill="FFF8E6", border="F5DFA0", size=9.5)
    B.para(doc, "참고한 문서", size=11, bold=True, sb=4, sa=2)
    B.box(doc, ["· %s\n  %s" % (t, u) for t, u in SOURCE_LINKS], size=9)

    doc.save(path)
    return path


# ══════════════════════════════ HTML ══════════════════════════════
def _rows(head, rows):
    h = "<tr>" + "".join("<th>%s</th>" % c for c in head) + "</tr>"
    for r in rows:
        h += "<tr>" + "".join("<td>%s</td>" % str(c).replace("\n", "<br>") for c in r) + "</tr>"
    return h

def build_html(path):
    check = _rows(CHECK[0], CHECK[1:])
    fixed = _rows(["이런 일이 생깁니다", "그래서 이 자료는 이렇게 되어 있습니다"], FIXED)
    mods = _rows(MOD_HEAD, MODS)
    say = _rows(["학생이 하는 말", "선생님 한 마디"], SAY)
    ul = lambda xs: "".join("<li>%s</li>" % x for x in xs)
    links = "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, t)
                    for t, u in SOURCE_LINKS)

    html = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s · 단계별 AI 수업</title>
<style>
:root{--ink:#1b2330;--sub:#5b6675;--line:#e2e6ec;--bg:#f4f6fa;--brand:#2f6df0;--brand-d:#1f53c4;--paper:#fff;--soft:#eef3ff;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Apple SD Gothic Neo","Malgun Gothic","맑은 고딕",system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.65;}
.wrap{max-width:900px;margin:0 auto;padding:32px 18px 64px;}
.kicker{font-size:12px;font-weight:800;color:var(--brand);letter-spacing:.2px;}
h1{font-size:26px;margin:4px 0 6px;letter-spacing:-.5px;}
p.lead{color:var(--sub);margin:0 0 4px;font-size:14px;}
.stamp{font-size:12px;color:var(--sub);margin:0 0 20px;}
h2{font-size:17px;margin:30px 0 10px;letter-spacing:-.3px;border-bottom:1px solid var(--line);padding-bottom:7px;}
.card{background:var(--paper);border:1px solid var(--line);border-radius:13px;padding:15px 17px;margin-bottom:12px;}
.warn{background:#fff8e6;border-color:#f5dfa0;}
.danger{background:#fff4f4;border-color:#f2c7c7;}
.good{background:#eef7ee;border-color:#c3e0c8;}
ul{margin:0;padding-left:20px;} li{font-size:13.5px;margin:4px 0;}
.tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;background:var(--paper);border:1px solid var(--line);border-radius:13px;}
table{border-collapse:collapse;width:100%%;min-width:560px;}
th,td{border-bottom:1px solid var(--line);padding:9px 11px;font-size:13px;text-align:left;vertical-align:top;}
th{background:var(--soft);color:var(--brand-d);font-size:12.5px;font-weight:800;white-space:nowrap;}
tr:last-child td{border-bottom:0;}
td:first-child{font-weight:700;}
.small{font-size:12.5px;color:var(--sub);}
.back{display:inline-block;margin-bottom:18px;font-size:13px;text-decoration:none;color:var(--sub);border:1px solid var(--line);background:var(--paper);border-radius:9px;padding:7px 12px;}
.print{float:right;font-size:13px;border:1px solid var(--brand);background:var(--brand);color:#fff;border-radius:9px;padding:7px 13px;cursor:pointer;font-family:inherit;}
@media print{.back,.print{display:none;} body{background:#fff;} .tblwrap{overflow:visible;} table{min-width:0;}}
</style></head><body><div class="wrap">
<a class="back" href="index.html">← 수업 첫 화면</a>
<button class="print" onclick="window.print()">🖨 인쇄</button>
<div class="kicker">단계별 AI 수업 · 교사용</div>
<h1>%(title)s</h1>
<p class="lead">%(sub)s</p>
<p class="stamp">대조 확인일 %(confirmed)s · 무료 정책은 자주 바뀌므로 1번 점검표로 직접 확인하세요</p>

<div class="card warn"><b>이 문서에 한도 숫자를 적지 않은 이유</b><ul>%(why)s</ul></div>

<h2>1. 수업 전 10분 점검</h2>
<p class="small">%(checkintro)s</p>
<div class="tblwrap"><table>%(check)s</table></div>

<h2>2. 무료에서 바뀌지 않는 것 6가지</h2>
<div class="tblwrap"><table>%(fixed)s</table></div>

<h2>3. 한도를 아끼는 수업 운영</h2>
<div class="card"><ul>%(save)s</ul></div>

<h2>4. 모듈별 — 무료 제미나이로 하면</h2>
<div class="tblwrap"><table>%(mods)s</table></div>

<h2>5. 수업 중 이 말이 나오면</h2>
<div class="tblwrap"><table>%(say)s</table></div>

<h2>6. 개인정보 — 무료라서 더 중요한 것</h2>
<div class="card danger"><ul>%(priv)s</ul></div>

<h2>7. 학생에게 그대로 읽어 주세요</h2>
<div class="card good"><ul>%(read)s</ul></div>

<h2>8. 확인한 것과 확인하지 못한 것</h2>
<div class="card"><b>공식 문서로 확인한 것</b><ul>%(conf)s</ul></div>
<div class="card warn"><b>확인하지 못한 것 — 직접 보셔야 합니다</b><ul>%(unconf)s</ul></div>
<div class="card"><b>참고한 문서</b><ul>%(links)s</ul></div>
</div></body></html>""" % dict(
        title=TITLE, sub=SUB, confirmed=CONFIRMED,
        why=ul(WHY), checkintro=CHECK_INTRO, check=check, fixed=fixed,
        save=ul(SAVE), mods=mods, say=say, priv=ul(PRIV), read=ul(READ),
        conf=ul(SOURCE_CONFIRMED), unconf=ul(SOURCE_UNCONFIRMED), links=links)

    io.open(path, "w", encoding="utf-8").write(html)
    return path
