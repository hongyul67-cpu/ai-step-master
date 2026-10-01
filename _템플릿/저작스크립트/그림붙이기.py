# -*- coding: utf-8 -*-
"""modules/*.json 의 스텝에 그림 키(fig)를 붙인다 — 그림은 figs.js 에 있다 (2026-10-01 · 보조06).
다시 돌려도 결과가 같다. 붙인 뒤에는 build_all.py 로 학생용 HTML 을 다시 굽는다.
그림을 빼고 싶으면 아래 표에서 그 칸을 지우고 다시 돌린다."""
import io, json, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 3단계 공통 14스텝 — 모듈마다 다른 칸은 아래 EXTRA 로 덮어쓴다 (None = 그림 없음)
COMMON = {"S2": "rc", "S3": "askme", "S5": "skeleton", "S6": "fix1", "S8": "fix2", "S9": "fix3",
          "S10": "check", "S11": "roleflip", "S12": "myhand", "S13": "mine"}
EXTRA = {
    "A1": {"S7": "compare", "S10": "compare"},
    "A2": {"S5": "mail", "S7": "mail"},
    "A3": {"S10": "blank"},
    "A4": {"S11": None},
    "A6": {"S10": "compare"},
    "B1": {"S12": "slide5s", "S14": "slide5s"},
    "B2": {"S5": "timebar", "S11": "rehearsal", "S12": "rehearsal"},
    "B3": {"S5": None, "S12": None},
    "C1": {"S5": "pseudo", "S10": "errloop", "S11": None},
    "D1": {"S10": "leading", "S11": None, "S12": "factvs"},
    "D2": {"S5": None, "S6": "criteria", "S11": "bias", "S12": None},
}
OTHER = {
    "0": {"intro": "promise3", "S1": "dataflow", "S2": "confident", "S3": "mine", "S4": "promise3"},
    "R": {"S2": "samediff", "S3": "vague", "S4": "rcif", "S7": "mine"},
    "P1": {"S2": "flow14", "S3": "rc", "S4": "askme", "S5": "skeleton", "S6": "fixall", "S7": "check", "S8": "myhand", "S9": "mine"},
    "P2": {"S2": "mine"},
}

def plan(code):
    if code in OTHER:
        return dict(OTHER[code])
    p = dict(COMMON); p["intro"] = "flow14"
    p.update(EXTRA.get(code, {}))
    return p

total = withfig = 0
for f in sorted(glob.glob(os.path.join(ROOT, "modules", "*.json"))):
    if os.path.basename(f).startswith("_"):
        continue
    raw = io.open(f, encoding="utf-8", newline="").read()
    m = json.loads(raw)
    p = plan(m["code"])
    if p.get("intro"):
        m.setdefault("intro", {})["fig"] = p["intro"]
    else:
        m.get("intro", {}).pop("fig", None)
    for st in m["steps"]:
        total += 1
        k = p.get(st["no"])
        if k:
            st["fig"] = k; withfig += 1
        else:
            st.pop("fig", None)
    out = json.dumps(m, ensure_ascii=False, indent=1)
    if raw.endswith("\n"):
        out += "\n"
    io.open(f, "w", encoding="utf-8", newline="").write(out)
    print(m["code"], sum(1 for s in m["steps"] if s.get("fig")), "/", len(m["steps"]))
print("스텝", total, "· 그림 붙은 스텝", withfig)
