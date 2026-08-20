# -*- coding: utf-8 -*-
"""fix_review.py 의 나머지 (스텝러너 화면 치환 · 편집기 인쇄 치환 · 약속 문장)"""
import io, os, sys, json, glob

REPO = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code", "ai-step-master")

def patch(path, pairs, name):
    s = io.open(path, encoding="utf-8").read()
    for old, new, what in pairs:
        if old not in s:
            print("  !! [%s] 찾지 못함: %s" % (name, what)); sys.exit(1)
        s = s.replace(old, new, 1)
        print("  ✔ [%s] %s" % (name, what))
    io.open(path, "w", encoding="utf-8").write(s)

# ── 스텝러너 : 화면에서도 {{키}} 치환 ───────────────────────────────
p = os.path.join(REPO, "_템플릿", "스텝러너_템플릿.html")
patch(p, [
 ("""h+='<p class="why'+(st.star?" star":"")+'">'+esc(st.why)+"</p>";""",
  """h+='<p class="why'+(st.star?" star":"")+'">'+esc(fill(st.why))+"</p>";""",
  "why 치환"),
 ("""<div class="sample">'+esc(st.expect)+"</div>""",
  """<div class="sample">'+esc(fill(st.expect))+"</div>""",
  "예시 치환"),
 ("""h+='<label class="fl">'+esc(st.record.label)+"</label>";""",
  """h+='<label class="fl">'+esc(fill(st.record.label))+"</label>";""",
  "기록칸 라벨 치환"),
 ("""placeholder="'+esc(st.record.ph||"")+'\"""",
  """placeholder="'+esc(fill(st.record.ph||""))+'\"""",
  "기록칸 예시 치환"),
 ("""+(on?" checked":"")+"> <span>"+esc(c)+"</span></label></li>";""",
  """+(on?" checked":"")+"> <span>"+esc(fill(c))+"</span></label></li>";""",
  "체크리스트 치환"),
], "스텝러너")

# ── 편집기 인쇄물 라벨 치환 ─────────────────────────────────────────
p = os.path.join(REPO, "_템플릿", "모듈편집기_템플릿.html")
patch(p, [
 ("function printWorkbook(){",
  '''function lbl(t){
  if(!t) return t;
  const names={}; (M.mats||[]).forEach(x=>names[x.k]=x.label||x.k);
  return String(t).replace(/\\{\\{(\\w+)\\}\\}/g,(mo,k)=>"["+(names[k]||k)+"]");
}
function printWorkbook(){''',
  "lbl() 추가"),
 ("""if(st.why) h+='<div class="why">'+esc(st.why)+"</div>";""",
  """if(st.why) h+='<div class="why">'+esc(lbl(st.why))+"</div>";""",
  "why 치환"),
 ("""'<div class="box"><b>▶ '+esc(p.label||"")+"</b>"+esc(p.text||"")+"</div>";""",
  """'<div class="box"><b>▶ '+esc(p.label||"")+"</b>"+esc(lbl(p.text||""))+"</div>";""",
  "프롬프트 치환"),
 ("""<b>이런 답이 오면 정상입니다</b>'+esc(st.expect)+"</div>";""",
  """<b>이런 답이 오면 정상입니다</b>'+esc(lbl(st.expect))+"</div>";""",
  "예시 치환"),
 ("""'<div class="box warn"><b>[막혔을 때] '+esc(t.when)+"</b>→ "+esc(t.fix)+"</div>";""",
  """'<div class="box warn"><b>[막혔을 때] '+esc(t.when)+"</b>→ "+esc(lbl(t.fix))+"</div>";""",
  "대처문 치환"),
 ("""h+="<h3>▷ 기록 — "+esc(st.record.label)+'</h3>""",
  """h+="<h3>▷ 기록 — "+esc(lbl(st.record.label))+'</h3>""",
  "기록칸 치환"),
 ("""'<div class="chk">☐ '+esc(c)+"</div>";""",
  """'<div class="chk">☐ '+esc(lbl(c))+"</div>";""",
  "체크리스트 치환"),
], "모듈편집기")

# ── 약속 문장 보강 ─────────────────────────────────────────────────
ADD = {
 "A3": "실제 이름 · 학번 · 연락처는 AI 입력창에 넣지 않습니다. 제출할 때 내가 직접 씁니다.",
 "B1": "실제 이름 · 학번 · 연락처는 AI 입력창에 넣지 않습니다. 슬라이드에는 마지막에 내가 직접 씁니다.",
 "B3": "실제 이름 · 학번 · 연락처는 AI 입력창에 넣지 않습니다.",
}
for f in glob.glob(os.path.join(REPO, "modules", "*.json")):
    m = json.load(io.open(f, encoding="utf-8"))
    if m["code"] in ADD:
        rules = m["intro"]["rules"]
        if not any("연락처" in r for r in rules):
            rules.insert(0, ADD[m["code"]])
            io.open(f, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
            print("  ✔ [약속] %s 개인정보 문장 추가" % m["code"])

print("\n나머지 수정 완료")
