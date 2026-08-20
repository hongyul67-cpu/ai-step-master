# -*- coding: utf-8 -*-
"""핸드폰에서 손가락으로 누르기 작은 버튼 두 개를 키운다."""
import io, os, sys

p = os.path.join(os.environ["USERPROFILE"], "Desktop", "claude code",
                 "ai-step-master", "_템플릿", "스텝러너_템플릿.html")
s = io.open(p, encoding="utf-8").read()

anchor = "@media print{"
if anchor not in s:
    print("!! 인쇄 스타일 자리를 찾지 못함"); sys.exit(1)

add = """/* 핸드폰 — 손가락으로 누르는 것들을 키운다 */
@media (max-width:560px){
  .promptbox .copy{width:100%;padding:13px 14px;font-size:14px;}
  .trouble .copy{width:100%;padding:11px 12px;font-size:13px;}
  .map{gap:6px;}
  .map button{width:38px;height:38px;font-size:12.5px;}
  .iconbtn{padding:7px 10px;font-size:12px;}
}
@media print{"""

s = s.replace(anchor, add, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("  ✔ 모바일 터치 크기 보정")
