/* ══════════════════════════════════════════════════════════════
   단계별 AI 수업 — 그림 모음 (보조06 · 2026-10-01)
   공용 그리기 도우미 links/fig.js 를 쓴다. 학생용 스텝 러너(A1_….html 등)가 부른다.

   붙이는 법 — modules/*.json 의 스텝에 "fig": "키" (여러 장이면 ["키","키"]),
               시작 화면은 intro.fig. 스텝 러너가 「왜 하나」 설명 바로 아래에 그린다.
   학생용 파일은 인터넷 없이도 열린다 — 그때는 그림만 빠지고 글은 그대로 나온다.

   그림 내용은 모듈의 설명(why) · 안내판(panel) · 프롬프트에 적힌 것만 옮겼다.
   예시 숫자를 쓴 그림은 캡션에 (예시)라고 적었다.
   ══════════════════════════════════════════════════════════════ */
var FIGS = (function () {
  var F = window.FIG;
  if (!F) return {};
  var C = F.C;
  var t = F.t, box = F.box, line = F.line, arrow = F.arrow, circle = F.circle;

  /* ── 작은 도우미 ── */
  /* 사람 — (x,y) = 발밑 가운데 */
  function person(x, y, s, c, fill) {
    s = s || 1; c = c || C.blue; fill = fill || C.blueL;
    return '<circle cx="' + x + '" cy="' + (y - 34 * s) + '" r="' + (7 * s) + '" fill="' + fill + '" stroke="' + c + '" stroke-width="1.8"/>' +
      F.path('M' + (x - 11 * s) + ',' + y + ' L' + (x - 11 * s) + ',' + (y - 15 * s) + ' Q' + (x - 11 * s) + ',' + (y - 25 * s) + ' ' + x + ',' + (y - 25 * s) +
        ' Q' + (x + 11 * s) + ',' + (y - 25 * s) + ' ' + (x + 11 * s) + ',' + (y - 15 * s) + ' L' + (x + 11 * s) + ',' + y + ' Z', { fill: fill, c: c, w: 1.8 });
  }
  /* AI — (x,y) = 가운데. 네모 얼굴에 눈 두 개 */
  function ai(x, y, s, c, fill) {
    s = s || 1; c = c || C.purple; fill = fill || C.purpleL;
    return line(x, y - 17 * s, x, y - 24 * s, { c: c, w: 1.8 }) + '<circle cx="' + x + '" cy="' + (y - 26 * s) + '" r="' + (3 * s) + '" fill="' + c + '"/>' +
      box(x - 18 * s, y - 17 * s, 36 * s, 32 * s, { fill: fill, c: c, r: 8 * s, w: 1.8 }) +
      '<circle cx="' + (x - 7 * s) + '" cy="' + (y - 3 * s) + '" r="' + (3 * s) + '" fill="' + c + '"/>' +
      '<circle cx="' + (x + 7 * s) + '" cy="' + (y - 3 * s) + '" r="' + (3 * s) + '" fill="' + c + '"/>' +
      line(x - 6 * s, y + 7 * s, x + 6 * s, y + 7 * s, { c: c, w: 1.6 });
  }
  /* 종이 — 줄 n 개. o.heads = 굵은 제목 줄(뼈대) 위치들, o.hi = 강조할 줄 */
  function doc(x, y, w, h, o) {
    o = o || {};
    var s = box(x, y, w, h, { fill: o.fill || '#fff', c: o.c || C.ink, r: 5, w: 1.6 });
    var n = o.n == null ? Math.floor((h - 16) / 12) : o.n, gap = (h - 20) / Math.max(1, n);
    for (var i = 0; i < n; i++) {
      var yy = y + 14 + i * gap, head = o.heads && o.heads.indexOf(i) >= 0, hi = o.hi && o.hi.indexOf(i) >= 0;
      var len = head ? (w - 20) * 0.5 : (w - 20) * (i % 3 === 2 ? 0.7 : 1);
      if (o.bones && !head) continue;
      s += line(x + 10, yy, x + 10 + len, yy, { c: hi ? (o.hc || C.orange) : (head ? (o.headc || C.blue) : C.grayM), w: head ? 4 : (hi ? 4 : 2.4) });
    }
    return s;
  }
  function bubble(x, y, w, h, txt, o) {
    o = o || {};
    var c = o.c || C.grayM, tail = o.tail === 'r' ? [[x + w - 22, y + h], [x + w - 12, y + h + 10], [x + w - 34, y + h]] : [[x + 22, y + h], [x + 12, y + h + 10], [x + 34, y + h]];
    return box(x, y, w, h, { fill: o.fill || '#fff', c: c, r: 10, w: 1.6 }) + (o.notail ? '' : F.poly(tail, { fill: o.fill || '#fff', c: c, w: 1.6 }) +
      line(tail[0][0], tail[0][1], tail[2][0], tail[2][1], { c: o.fill || '#fff', w: 2.4 })) +
      t(x + w / 2, y + h / 2, txt, { a: 'm', size: o.size || 13, b: o.b, c: o.tc || C.ink, halo: false });
  }
  function check(x, y, c, s) { s = s || 1; return F.poly([[x - 7 * s, y], [x - 2 * s, y + 6 * s], [x + 8 * s, y - 7 * s]], { c: c || C.green, w: 3 }); }
  function cross(x, y, c, r) {
    r = r || 7;
    return line(x - r, y - r, x + r, y + r, { c: c || C.red, w: 3 }) + line(x + r, y - r, x - r, y + r, { c: c || C.red, w: 3 });
  }
  function tag(x, y, w, txt, c, cl) {
    return box(x, y - 13, w, 26, { fill: cl, c: c, r: 13, w: 1.4 }) + t(x + w / 2, y, txt, { a: 'm', size: 13, b: 1, c: c, halo: false });
  }
  function pencil(x, y, c) {
    c = c || C.orange;
    return F.g(F.poly([[0, 0], [5, -14], [11, -12], [6, 2]], { close: 1, fill: C.orangeL, c: c, w: 1.4 }) +
      F.poly([[5, -14], [16, -44], [22, -42], [11, -12]], { close: 1, fill: '#fff', c: c, w: 1.4 }), { x: x, y: y });
  }

  /* 수정 요청 세 번 — hi: 1·2·3 = 지금 스텝, 0 = 셋 다 */
  function fixFig(hi) {
    return function () {
      var d = [['① 뼈대', '항목 · 순서를 고친다'], ['② 전체', '문체 · 분량을 고친다'], ['③ 부분', '한 곳만 고친다']], s = '';
      d.forEach(function (it, i) {
        var x = 20 + i * 154, on = hi === 0 || hi === i + 1;
        s += box(x, 18, 132, 196, { fill: on ? C.orangeL : '#fff', c: on ? C.orange : C.grayM, r: 12, w: on ? 2.4 : 1.4 });
        if (hi && on) s += tag(x + 86, 18, 44, '지금', C.orange, '#fff');
        if (i === 0) s += doc(x + 30, 36, 72, 100, { n: 7, heads: [0, 3, 5], headc: C.orange });
        if (i === 1) s += doc(x + 30, 36, 72, 100, { n: 7, heads: [0, 3, 5], fill: C.yellowL, hi: [1, 2, 4, 6] });
        if (i === 2) s += doc(x + 30, 36, 72, 100, { n: 7, heads: [0, 3, 5], hi: [4] }) +
          box(x + 34, 86, 64, 16, { fill: 'none', c: C.orange, r: 4, w: 1.6, dash: '4 3' });
        s += t(x + 66, 160, it[0], { a: 'm', b: 1, size: 17, c: on ? C.orange : C.sub });
        s += t(x + 66, 188, it[1], { a: 'm', size: 13, c: on ? C.ink : C.sub });
        if (i < 2) s += arrow(x + 134, 116, x + 152, 116, { c: C.grayM, w: 1.8, head: 8 });
      });
      s += t(240, 236, '한 번에 하나씩 · “다시 써 줘” 대신 무엇을 어떻게 바꿀지 말한다', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 254, s);
    };
  }
  var FIXCAP = '수정 요청은 세 번 — 큰 것(뼈대)부터 작은 것(부분)으로 좁혀 간다';

  return {

  /* ─────────── 전체 흐름 ─────────── */
  flow14: {
    cap: '14스텝 지도 — 준비 → 초안과 수정 → 점검과 마무리 (★ 두 곳이 승부처 · 이름은 모듈마다 조금 다르다)',
    draw: function () {
      var n = ['재료', '역할·상황', 'AI가 질문', '답하기', '뼈대만', '수정 ①', '1차 초안', '수정 ②', '수정 ③', '사실 확인', '상대 입장', '내 손으로', '사용 기록', '제출·비교'];
      var ph = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2], col = [C.blue, C.orange, C.green], cl = [C.blueL, C.orangeL, C.greenL], s = '';
      n.forEach(function (name, i) {
        var r = i < 7 ? 0 : 1, k = i % 7, x = 38 + k * 67, y = 56 + r * 96, star = i === 2 || i === 11, p = ph[i];
        if (k < 6) s += line(x + 18, y, x + 49, y, { c: C.grayM, w: 1.6 });
        s += circle(x, y, 18, { fill: star ? col[p] : cl[p], c: col[p], w: 2 }) +
          t(x, y + 1, String(i + 1), { a: 'm', b: 1, size: 15, c: star ? '#fff' : col[p], halo: false });
        if (star) s += t(x + 20, y - 20, '★', { a: 'm', size: 16, c: C.red });
        s += t(x, y + 34, name, { a: 'm', size: 13, b: star, c: star ? C.red : C.ink });
      });
      s += F.route([[458, 56], [470, 56], [470, 104], [14, 104], [14, 152], [20, 152]], { c: C.grayM, w: 1.6, head: 8 });
      s += tag(20, 222, 132, '1차시 · 준비와 뼈대', C.blue, C.blueL) + tag(166, 222, 132, '2차시 · 초안과 확인', C.orange, C.orangeL) +
        tag(312, 222, 148, '3차시 · 점검과 마무리', C.green, C.greenL);
      return F.svg(480, 248, s);
    } },

  /* ─────────── 3단계 공통 스텝 ─────────── */
  rc: {
    cap: '처음에는 역할(R)과 상황(C)만 준다 — 결과물은 아직 달라고 하지 않는다',
    draw: function () {
      var rows = [['R', '역할', '누구처럼 답할지', 1], ['C', '맥락', '어떤 상황인지', 1], ['I', '지시', '무엇을 해 달라는지', 0], ['F', '형식', '어떤 모양으로', 0]], s = '';
      rows.forEach(function (r, i) {
        var y = 20 + i * 48, on = r[3];
        s += box(20, y, 280, 40, { fill: on ? C.blueL : '#fff', c: on ? C.blue : C.grayM, r: 8, w: on ? 2 : 1.4, dash: on ? '' : '5 4' });
        s += box(26, y + 5, 30, 30, { fill: on ? C.blue : C.grayM, c: on ? C.blue : C.grayM, r: 6 }) +
          t(41, y + 21, r[0], { a: 'm', b: 1, size: 17, c: '#fff', halo: false });
        s += t(68, y + 20, r[1], { a: 's', b: 1, size: 16, c: on ? C.ink : C.sub }) + t(118, y + 20, r[2], { a: 's', size: 13, c: C.sub });
      });
      s += F.path('M308,24 Q320,24 320,40 L320,90 Q320,106 308,106', { c: C.blue, w: 1.8 }) + t(330, 56, '지금', { a: 's', b: 1, size: 16, c: C.blue }) +
        t(330, 78, '보낸다', { a: 's', b: 1, size: 16, c: C.blue });
      s += F.path('M308,120 Q320,120 320,136 L320,186 Q320,202 308,202', { c: C.grayM, w: 1.8 }) + t(330, 152, '아직', { a: 's', b: 1, size: 16, c: C.sub }) +
        t(330, 174, '나중에', { a: 's', size: 13, c: C.sub });
      s += ai(430, 96, 1) + bubble(376, 124, 92, 30, '이해했습니다', { c: C.purple, notail: 1 });
      return F.svg(480, 222, s);
    } },

  askme: {
    cap: 'AI가 먼저 나에게 질문하게 한다 — 묻는 방향을 뒤집으면 빠진 정보가 채워진다',
    draw: function () {
      var s = t(20, 26, '보통은', { a: 's', b: 1, size: 15, c: C.sub });
      s += person(60, 96, 0.95, C.sub, C.grayL) + ai(420, 76, 0.95, C.sub, C.grayL);
      s += arrow(90, 66, 388, 66, { c: C.grayM, w: 2 }) + t(240, 52, '내가 묻는다 “써 줘”', { a: 'm', size: 13, c: C.sub });
      s += arrow(388, 88, 90, 88, { c: C.grayM, w: 2 }) + t(240, 102, 'AI가 답한다 (빠진 건 지어낸다)', { a: 'm', size: 13, c: C.sub });
      s += line(16, 122, 464, 122, { c: C.edge, w: 1.4 });
      s += t(20, 146, '이 스텝에서는', { a: 's', b: 1, size: 15, c: C.orange });
      s += person(60, 222, 0.95) + ai(420, 202, 0.95);
      s += arrow(388, 190, 90, 190, { c: C.orange, w: 2.6 }) + t(240, 174, 'AI가 묻는다 “질문 5개”', { a: 'm', size: 15, b: 1, c: C.orange });
      s += arrow(90, 214, 388, 214, { c: C.blue, w: 2.6 }) + t(240, 230, '내가 답한다', { a: 'm', size: 15, b: 1, c: C.blue });
      s += t(240, 258, '→ 내 답이 결과물의 알맹이가 된다', { a: 'm', size: 13 });
      return F.svg(480, 274, s);
    } },

  skeleton: {
    cap: '본문보다 뼈대(항목)를 먼저 받는다 — 뼈대에서 고치는 것이 훨씬 빠르다',
    draw: function () {
      var s = t(110, 26, '한 번에 전부 받으면', { a: 'm', b: 1, size: 15, c: C.sub });
      s += doc(60, 42, 100, 140, { n: 11 }) + t(110, 200, '길어서 고치기 어렵다', { a: 'm', size: 13, c: C.red });
      s += line(222, 16, 222, 214, { c: C.grayM, w: 1.4, dash: '6 5' });
      s += t(350, 26, '뼈대부터 받으면', { a: 'm', b: 1, size: 15, c: C.blue });
      s += doc(244, 42, 86, 140, { n: 11, heads: [0, 3, 6, 9], bones: 1 }) + t(287, 200, '① 항목만', { a: 'm', size: 13, b: 1, c: C.blue });
      s += arrow(336, 112, 366, 112, { c: C.blue, w: 2 });
      s += doc(372, 42, 86, 140, { n: 11, heads: [0, 3, 6, 9] }) + t(415, 200, '② 살 붙이기', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 220, s);
    } },

  fix1: { cap: FIXCAP, draw: fixFig(1) },
  fix2: { cap: FIXCAP, draw: fixFig(2) },
  fix3: { cap: FIXCAP, draw: fixFig(3) },
  fixall: { cap: FIXCAP, draw: fixFig(0) },

  check: {
    cap: '사실 확인 — AI에게 확실·추측·모름을 표시하게 하고, 추측·모름은 내가 직접 확인한다',
    draw: function () {
      var s = t(86, 26, 'AI가 쓴 글', { a: 'm', b: 1, size: 15 });
      s += doc(36, 40, 100, 130, { n: 9 });
      s += arrow(142, 104, 176, 104, { c: C.purple, w: 2 }) + t(159, 86, '①', { a: 'm', size: 15, b: 1, c: C.purple });
      s += t(240, 26, '표시하게 한다', { a: 'm', b: 1, size: 15, c: C.purple });
      [['확실', C.green, C.greenL], ['추측', C.orange, C.orangeL], ['모름', C.red, C.redL]].forEach(function (d, i) {
        s += tag(196, 64 + i * 40, 88, d[0], d[1], d[2]);
      });
      s += F.route([[288, 104], [300, 104], [300, 124], [318, 124]], { c: C.orange, w: 1.8, head: 8 }) +
        F.route([[288, 144], [318, 144]], { c: C.red, w: 1.8, head: 8 });
      s += t(396, 26, '내가 직접 확인', { a: 'm', b: 1, size: 15, c: C.blue });
      s += box(322, 96, 148, 74, { fill: C.blueL, c: C.blue, r: 10 }) + person(350, 158, 0.8) +
        t(418, 122, '공식 자료', { a: 'm', size: 13, b: 1 }) + t(418, 144, '원래 자료', { a: 'm', size: 13, b: 1 });
      s += t(304, 86, '②', { a: 'm', size: 15, b: 1, c: C.blue });
      s += check(206, 198) + t(222, 198, '맞으면 그대로', { a: 's', size: 13 }) + cross(336, 198, C.red, 6) + t(350, 198, '틀리면 고친다', { a: 's', size: 13 });
      s += t(240, 226, 'AI는 모르는 것도 자신 있게 말한다 — 확인은 내 몫', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 244, s);
    } },

  compare: {
    cap: '원래 자료와 대조 — 내가 준 자료에 없던 문장을 찾아낸다',
    draw: function () {
      var s = t(100, 26, '내가 준 자료', { a: 'm', b: 1, size: 15, c: C.blue }) + t(380, 26, 'AI가 정리한 글', { a: 'm', b: 1, size: 15, c: C.purple });
      s += box(30, 42, 140, 150, { fill: '#fff', c: C.blue, r: 6 }) + box(310, 42, 140, 186, { fill: '#fff', c: C.purple, r: 6 });
      [0, 1, 2].forEach(function (i) {
        var y = 70 + i * 44;
        s += line(44, y, 156, y, { c: C.blue, w: 3 }) + line(324, y, 436, y, { c: C.blue, w: 3 });
        s += line(172, y, 308, y, { c: C.grayM, w: 1.4, dash: '4 4' }) + t(240, y - 12, '있음', { a: 'm', size: 13, c: C.green });
      });
      s += line(324, 202, 436, 202, { c: C.red, w: 4 }) + t(240, 202, '자료에 없음 →', { a: 'm', size: 13, b: 1, c: C.red });
      s += t(100, 214, '?', { a: 'm', size: 22, b: 1, c: C.red });
      s += t(240, 250, '없던 문장은 지우거나 (확인 필요)로 표시한다', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 268, s);
    } },

  roleflip: {
    cap: 'AI를 상대편 자리에 세운다 — 읽는 사람의 눈으로 부족한 점을 듣는다',
    draw: function () {
      var s = person(54, 150, 1) + t(54, 170, '나', { a: 'm', size: 13, b: 1 });
      s += doc(112, 76, 78, 96, { n: 7, heads: [0, 3] }) + t(151, 190, '내 결과물', { a: 'm', size: 13 });
      s += arrow(196, 124, 250, 124, { w: 2 });
      s += ai(300, 128, 1.2) + t(300, 170, 'AI', { a: 'm', size: 13, b: 1, c: C.purple });
      s += box(248, 38, 104, 28, { fill: C.purple, c: C.purple, r: 14 }) + t(300, 52, '역할을 준다', { a: 'm', size: 13, b: 1, c: '#fff', halo: false });
      s += t(300, 80, '읽는 사람 · 검토자 · 청중', { a: 'm', size: 13, c: C.purple });
      s += bubble(360, 96, 108, 60, '', { c: C.orange, fill: C.orangeL, notail: 1 }) +
        t(414, 116, '부족한 점', { a: 'm', size: 13, b: 1, halo: false }) + t(414, 138, '3가지', { a: 'm', size: 15, b: 1, c: C.orange, halo: false });
      s += t(414, 174, '칭찬은 빼고', { a: 'm', size: 13, c: C.sub });
      s += F.route([[414, 186], [414, 214], [151, 214], [151, 202]], { c: C.orange, w: 1.8, dash: '6 4', head: 9 });
      s += t(282, 230, '듣고 → 고칠 곳은 내가 정한다', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 246, s);
    } },

  myhand: {
    cap: '마지막은 AI 없이 내 손으로 — 그 자리에 있던 사람만 쓸 수 있는 것을 채운다',
    draw: function () {
      var s = doc(40, 30, 150, 180, { n: 12, heads: [0, 4, 8], hi: [2, 6, 10] });
      [2, 6, 10].forEach(function (i) { s += box(46, 30 + 14 + i * 13.33 - 8, 138, 16, { fill: 'none', c: C.orange, r: 4, w: 1.4, dash: '4 3' }); });
      s += pencil(196, 196);
      s += t(250, 60, '회색 = AI가 쓴 초안', { a: 's', size: 13, c: C.sub });
      s += t(250, 90, '주황 = 내가 채우고 고친 곳', { a: 's', size: 13, b: 1, c: C.orange });
      s += ai(280, 150, 0.9, C.sub, C.grayL) + cross(280, 147, C.red, 16);
      s += t(310, 140, 'AI는 그날', { a: 's', size: 13 }) + t(310, 160, '그곳에 없었다', { a: 's', size: 13, b: 1 });
      s += t(250, 200, '무엇을 보고 느꼈는지는 나만 안다', { a: 's', size: 13 });
      return F.svg(480, 230, s);
    } },

  mine: {
    cap: 'AI 사용 기록 — 선생님이 보려는 것은 “AI를 썼는가”가 아니라 “어디까지가 네 것인가”',
    draw: function () {
      var s = t(20, 26, '내가 낸 결과물', { a: 's', b: 1, size: 15 });
      var seg = [[20, 150, 'AI가 쓴 부분', C.grayL, C.sub], [170, 110, '내가 고친 부분', C.blueL, C.blue], [280, 80, '확인한 사실', C.greenL, C.green], [360, 100, '내가 한 일', C.orangeL, C.orange]];
      seg.forEach(function (g) { s += box(g[0], 40, g[1], 40, { fill: g[3], c: g[4], r: 4, w: 1.6 }) + t(g[0] + g[1] / 2, 60, g[2], { a: 'm', size: 13, b: 1, halo: false }); });
      s += F.path('M172,90 Q172,100 190,100 L442,100 Q460,100 460,90', { c: C.orange, w: 1.8 }) + t(316, 116, '여기가 내 것', { a: 'm', size: 13, b: 1, c: C.orange });
      var rows = [['①', '사용한 AI', C.sub], ['②', '주고받은 횟수', C.sub], ['③', '가장 도움이 된 부분', C.sub], ['④', '내가 고친 부분', C.blue], ['⑤', '사실 확인한 내용과 방법', C.green], ['⑥', '내가 한 일', C.orange]];
      s += t(20, 146, '기록표 여섯 줄', { a: 's', b: 1, size: 15 });
      rows.forEach(function (r, i) {
        var x = 20 + (i % 2) * 230, y = 172 + Math.floor(i / 2) * 30;
        s += t(x, y, r[0], { a: 's', size: 15, b: 1, c: r[2] }) + t(x + 22, y, r[1], { a: 's', size: 14, b: i > 2, c: i > 2 ? r[2] : C.ink });
      });
      s += t(240, 266, 'AI를 쓴 것은 감점이 아니다 — 기록하지 않는 것이 문제', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 284, s);
    } },

  /* ─────────── 1단계 · 약속 3가지 ─────────── */
  promise3: {
    cap: 'AI 쓰기 전 약속 3가지 — 넣을 때 · 받을 때 · 낼 때 하나씩',
    draw: function () {
      var s = person(40, 110, 0.9) + box(84, 70, 84, 40, { fill: '#fff', c: C.ink, r: 6, label: '입력창', size: 14 });
      s += arrow(170, 90, 196, 90, { w: 2 }) + ai(226, 92, 1) + arrow(256, 90, 282, 90, { w: 2 });
      s += box(286, 70, 76, 40, { fill: '#fff', c: C.ink, r: 6, label: 'AI의 답', size: 14 }) + arrow(364, 90, 388, 90, { w: 2 });
      s += doc(392, 60, 66, 60, { n: 4, heads: [0] }) + t(425, 134, '내 과제 제출', { a: 'm', size: 13 });
      s += arrow(126, 150, 126, 116, { c: C.red, w: 2, head: 9 }) + F.route([[247, 152], [247, 136], [324, 136], [324, 116]], { c: C.orange, w: 2, head: 9 }) + arrow(425, 160, 425, 146, { c: C.blue, w: 2, head: 9 });
      s += box(20, 154, 146, 82, { fill: C.redL, c: C.red, r: 10 }) + t(93, 174, '① 넣지 말 것', { a: 'm', b: 1, size: 15, c: C.red, halo: false }) +
        t(93, 198, '사람을 알아볼 수', { a: 'm', size: 13, halo: false }) + t(93, 218, '있는 정보', { a: 'm', size: 13, halo: false });
      s += box(174, 154, 146, 82, { fill: C.orangeL, c: C.orange, r: 10 }) + t(247, 174, '② 믿지 말 것', { a: 'm', b: 1, size: 15, c: C.orange, halo: false }) +
        t(247, 198, '숫자 · 규정은', { a: 'm', size: 13, halo: false }) + t(247, 218, '공식 자료로 확인', { a: 'm', size: 13, halo: false });
      s += box(328, 164, 138, 72, { fill: C.blueL, c: C.blue, r: 10 }) + t(397, 182, '③ 숨기지 말 것', { a: 'm', b: 1, size: 15, c: C.blue, halo: false }) +
        t(397, 204, '어떻게 썼는지', { a: 'm', size: 13, halo: false }) + t(397, 222, '여섯 줄로 남긴다', { a: 'm', size: 13, halo: false });
      s += t(240, 30, 'AI는 마음껏 쓰되, 세 가지만 지킨다', { a: 'm', b: 1, size: 15 });
      return F.svg(480, 252, s);
    } },

  dataflow: {
    cap: '입력창에 쓴 말은 내 컴퓨터에만 남지 않는다 — 한번 넘어가면 되돌릴 수 없다',
    draw: function () {
      var s = box(20, 50, 120, 84, { fill: '#fff', c: C.ink, r: 8 }) + box(32, 62, 96, 44, { fill: C.blueL, c: C.blue, r: 4, w: 1.2 }) +
        t(80, 84, '입력창', { a: 'm', size: 13, b: 1, halo: false }) + line(60, 134, 100, 134, { w: 2 }) + line(80, 134, 80, 144, { w: 2 }) + line(56, 146, 104, 146, { w: 2 });
      s += t(80, 168, '내 컴퓨터', { a: 'm', size: 15, b: 1 });
      s += arrow(146, 92, 196, 92, { c: C.red, w: 2.6, flow: 1 });
      s += box(200, 44, 108, 100, { fill: C.grayL, c: C.ink, r: 8 });
      [0, 1, 2].forEach(function (i) { s += box(212, 56 + i * 28, 84, 20, { fill: '#fff', c: C.sub, r: 4, w: 1.2 }) + '<circle cx="' + 224 + '" cy="' + (66 + i * 28) + '" r="3" fill="' + C.green + '"/>'; });
      s += t(254, 168, 'AI 회사 서버', { a: 'm', size: 15, b: 1 });
      s += arrow(314, 92, 352, 92, { c: C.red, w: 2.2, dash: '6 4' });
      s += ai(396, 76, 0.9) + person(440, 104, 0.8, C.sub, C.grayL);
      s += t(410, 132, '다른 사람의 답을', { a: 'm', size: 13 }) + t(410, 152, '만드는 데 쓰이기도', { a: 'm', size: 13 });
      s += F.route([[254, 190], [254, 206], [80, 206], [80, 186]], { c: C.sub, w: 1.6, dash: '5 4', head: 8 }) + cross(168, 206, C.red, 8);
      s += t(300, 206, '돌아올 수 없다', { a: 's', size: 15, b: 1, c: C.red });
      s += t(240, 244, '헷갈리면 — “학교 게시판에 붙어도 괜찮은가?”', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 262, s);
    } },

  confident: {
    cap: 'AI는 모르는 것도 자신 있게 말한다 — 겉으로는 구별되지 않는다',
    draw: function () {
      var s = ai(50, 124, 1.2) + t(170, 26, 'AI가 하는 말 (겉)', { a: 'm', b: 1, size: 15, c: C.purple }) + t(400, 26, '실제로는 (속)', { a: 'm', b: 1, size: 15 });
      var d = [['확실', C.green, C.greenL], ['추측', C.orange, C.orangeL], ['모름 · 지어냄', C.red, C.redL]];
      d.forEach(function (it, i) {
        var y = 46 + i * 54;
        s += box(90, y, 200, 40, { fill: '#fff', c: C.purple, r: 10 }) + line(104, y + 20, 214, y + 20, { c: C.grayM, w: 3 }) +
          t(224, y + 20, '입니다.', { a: 's', size: 14, b: 1, halo: false });
        s += arrow(296, y + 20, 332, y + 20, { c: C.grayM, w: 1.6, head: 8 });
        s += tag(338, y + 20, 124, it[0], it[1], it[2]);
      });
      s += t(190, 216, '세 문장 모두 똑같이 자신 있는 말투', { a: 'm', size: 13, c: C.purple });
      s += t(240, 244, '그래서 숫자 · 규정은 공식 자료로 직접 확인한다', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 262, s);
    } },

  /* ─────────── 2단계 · 프롬프트 기본기 ─────────── */
  samediff: {
    cap: '같은 질문인데 답이 다르다 — AI는 계산기가 아니다',
    draw: function () {
      var s = box(150, 16, 180, 40, { fill: C.blueL, c: C.blue, r: 10, label: '똑같은 질문', size: 15 });
      s += F.route([[200, 56], [200, 70], [110, 70], [110, 84]], { w: 1.8, head: 9 }) + F.route([[280, 56], [280, 70], [370, 70], [370, 84]], { w: 1.8, head: 9 });
      s += ai(110, 112, 1) + ai(370, 112, 1);
      s += t(110, 142, '첫 번째', { a: 'm', size: 13, c: C.sub }) + t(370, 142, '두 번째 (다른 AI · 새 대화)', { a: 'm', size: 13, c: C.sub });
      s += arrow(110, 152, 110, 168, { w: 1.8, head: 8 }) + arrow(370, 152, 370, 168, { w: 1.8, head: 8 });
      s += doc(60, 172, 100, 70, { n: 5, hi: [0, 3], hc: C.green }) + doc(320, 172, 100, 70, { n: 5, hi: [1, 2, 4], hc: C.orange });
      s += t(240, 206, '≠', { a: 'm', size: 34, b: 1, c: C.red });
      return F.svg(480, 258, s);
    } },

  vague: {
    cap: '대충 물으면 답도 넓고 흐리다 — 자세히 물으면 내게 맞는 답이 온다',
    draw: function () {
      function target(cx) { return circle(cx, 150, 62, { fill: '#fff', c: C.grayM, w: 1.4 }) + circle(cx, 150, 40, { fill: '#fff', c: C.grayM, w: 1.4 }) + circle(cx, 150, 18, { fill: C.greenL, c: C.green, w: 1.8 }); }
      var s = bubble(40, 20, 160, 36, '“○○ 알려 줘.”', { size: 14, b: 1 }) + bubble(260, 20, 200, 36, 'R · C · I · F 를 넣어서', { size: 14, b: 1, c: C.blue, fill: C.blueL });
      s += target(120) + target(360);
      [[78, 118], [160, 112], [96, 190], [150, 186], [66, 156], [172, 150], [120, 96]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="5" fill="' + C.red + '"/>'; });
      [[356, 146], [366, 154], [362, 142], [352, 156], [368, 146]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="5" fill="' + C.blue + '"/>'; });
      s += t(120, 232, '어디에나 맞는 뻔한 답', { a: 'm', size: 13, b: 1, c: C.red }) + t(360, 232, '내 상황에 맞는 답', { a: 'm', size: 13, b: 1, c: C.blue });
      s += t(240, 150, '내가 원한 답', { a: 'm', size: 13, c: C.green }) + line(140, 150, 198, 150, { c: C.green, w: 1.2 }) + line(282, 150, 342, 150, { c: C.green, w: 1.2 });
      return F.svg(480, 250, s);
    } },

  rcif: {
    cap: '프롬프트 4요소 RCIF — 역할 · 맥락 · 지시 · 형식',
    draw: function () {
      var rows = [['R', '역할', '누구처럼 답할지', C.blue, C.blueL], ['C', '맥락', '어떤 상황인지', C.green, C.greenL], ['I', '지시', '무엇을 해 달라는지', C.orange, C.orangeL], ['F', '형식', '어떤 모양으로', C.purple, C.purpleL]], s = '';
      s += box(16, 14, 448, 216, { fill: '#fff', c: C.ink, r: 12, w: 1.8 }) + t(34, 34, '프롬프트 한 통', { a: 's', size: 13, c: C.sub });
      rows.forEach(function (r, i) {
        var y = 48 + i * 44;
        s += box(30, y, 420, 38, { fill: r[4], c: r[3], r: 8 });
        s += box(36, y + 4, 30, 30, { fill: r[3], c: r[3], r: 6 }) + t(51, y + 20, r[0], { a: 'm', b: 1, size: 18, c: '#fff', halo: false });
        s += t(80, y + 19, r[1], { a: 's', b: 1, size: 17, halo: false }) + t(140, y + 19, '— ' + r[2], { a: 's', size: 15, halo: false });
      });
      return F.svg(480, 244, s);
    } },

  /* ─────────── 모듈마다 다른 장치 ─────────── */
  mail: {
    cap: '선생님께 보내는 메일 — 용건이 먼저, 휴대전화 한 화면(7문장 이내)',
    draw: function () {
      var s = box(40, 14, 170, 252, { fill: '#fff', c: C.ink, r: 20, w: 2.4 }) + line(104, 26, 146, 26, { c: C.grayM, w: 4 });
      var rows = [['제목 — [학년·반] 용건', C.orange, C.orangeL, 1], ['나는 누구인지', C.blue, C.blueL, 0], ['용건 · 부탁 한 문장', C.orange, C.orangeL, 1], ['사정 (짧게)', C.sub, C.grayL, 0], ['회신 시점 · 인사', C.sub, C.grayL, 0]];
      rows.forEach(function (r, i) {
        var y = 44 + i * 40;
        s += box(52, y, 146, 32, { fill: r[2], c: r[1], r: 6, w: r[3] ? 2 : 1.2 }) + t(125, y + 16, r[0], { a: 'm', size: 13, b: r[3], halo: false });
      });
      s += line(40, 250, 210, 250, { c: C.red, w: 1.6, dash: '6 4' });
      s += F.callout(204, 60, 250, 50, '용건이 바로 보이게', { c: C.orange, tc: C.orange, b: 1, size: 14 });
      s += F.callout(204, 140, 250, 130, '사정보다 용건이 먼저', { c: C.orange, tc: C.orange, b: 1, size: 14 });
      s += F.callout(212, 250, 250, 232, '한 화면을 넘기면', { c: C.red, tc: C.red, size: 13 }) + t(256, 252, '뒤는 잘 안 읽힌다', { a: 's', size: 13, c: C.red });
      s += t(256, 186, '실명 · 학번 대신 [이름] [학번]', { a: 's', size: 13, c: C.sub });
      return F.svg(480, 280, s);
    } },

  blank: {
    cap: '[조사 필요] — 근거 자리는 비워 두고, 내가 직접 조사해서 채운다',
    draw: function () {
      var s = doc(30, 30, 150, 150, { n: 10, heads: [0, 4, 7] });
      s += box(44, 64, 96, 22, { fill: C.yellowL, c: C.orange, r: 4, w: 1.6 }) + t(92, 75, '[조사 필요]', { a: 'm', size: 13, b: 1, c: C.orange, halo: false });
      s += box(60, 132, 96, 22, { fill: C.yellowL, c: C.orange, r: 4, w: 1.6 }) + t(108, 143, '[조사 필요]', { a: 'm', size: 13, b: 1, c: C.orange, halo: false });
      s += t(105, 200, '건의문 초안', { a: 'm', size: 13 });
      s += ai(250, 62, 0.9, C.sub, C.grayL) + cross(250, 59, C.red, 16) + t(284, 52, 'AI가 채우면', { a: 's', size: 13 }) + t(284, 72, '그 순간 거짓말', { a: 's', size: 13, b: 1, c: C.red });
      s += person(250, 160, 0.95) + check(250, 178) + t(284, 126, '내가 직접 조사', { a: 's', size: 15, b: 1, c: C.blue }) +
        t(284, 150, '세어 보기 · 물어보기', { a: 's', size: 13 }) + t(284, 170, '→ 진짜 숫자로 채운다', { a: 's', size: 13 });
      s += arrow(232, 140, 160, 100, { c: C.blue, w: 1.8, head: 9 });
      return F.svg(480, 218, s);
    } },

  timebar: {
    cap: '대본은 분량이 곧 시간 — 대목마다 몇 초를 쓸지 먼저 정한다 (3분 발표 예시)',
    draw: function () {
      var seg = [['도입', 20, C.blue, C.blueL], ['본론 ①', 60, C.green, C.greenL], ['본론 ②', 60, C.green, C.greenL], ['마무리', 25, C.orange, C.orangeL], ['질문', 15, C.purple, C.purpleL]];
      var x = 20, px = 440 / 180, s = t(20, 26, '전체 3분 = 180초', { a: 's', b: 1, size: 15 });
      seg.forEach(function (g, i) {
        var w = g[1] * px;
        s += box(x, 64, w, 46, { fill: g[3], c: g[2], r: 4, w: 1.6 });
        s += t(x + w / 2, i === 4 ? 134 : 87, g[0], { a: 'm', size: 13, b: 1, halo: i === 4 });
        s += t(x + w / 2, i === 4 ? 154 : 126, g[1] + '초', { a: 'm', size: 13, c: g[2], b: 1 });
        if (i > 0 && i < 4) s += F.poly([[x - 6, 44], [x + 6, 44], [x, 58]], { close: 1, fill: C.red, c: C.red, w: 1 });
        x += w;
      });
      s += F.poly([[26, 176], [38, 176], [32, 190]], { close: 1, fill: C.red, c: C.red, w: 1 }) + t(46, 183, '슬라이드를 넘기는 때', { a: 's', size: 13 });
      s += t(240, 183, '20 + 60 + 60 + 25 + 15 = 180', { a: 's', size: 13, b: 1 });
      s += t(240, 214, '합계가 맞아야 한다', { a: 's', size: 13, c: C.sub });
      return F.svg(480, 232, s);
    } },

  rehearsal: {
    cap: '리허설 두 번 — 처음은 대본을 보며 시간을 재고, 다음은 대본을 덮고 흐름만으로',
    draw: function () {
      var s = box(14, 14, 220, 214, { fill: '#fff', c: C.grayM, r: 12 }) + box(246, 14, 220, 214, { fill: '#fff', c: C.grayM, r: 12 });
      s += t(124, 38, '1차 — 대본을 보며', { a: 'm', b: 1, size: 15, c: C.blue }) + t(356, 38, '2차 — 대본 없이', { a: 'm', b: 1, size: 15, c: C.orange });
      s += person(60, 140, 1) + doc(96, 66, 70, 84, { n: 6 });
      s += circle(196, 96, 20, { fill: '#fff', c: C.ink, w: 1.8 }) + line(196, 96, 196, 82, { w: 1.8 }) + line(196, 96, 206, 100, { w: 1.8 }) + box(191, 70, 10, 6, { fill: C.ink, r: 1 });
      s += t(124, 172, '소리 내어 · 시간을 잰다', { a: 'm', size: 13 });
      s += t(124, 194, '대본과 실제 말을 비교', { a: 'm', size: 13, b: 1 }) + t(124, 214, '빠뜨림 · 덧붙임 · 바뀜', { a: 'm', size: 13, c: C.sub });
      s += person(292, 140, 1, C.orange, C.orangeL) + doc(330, 66, 70, 84, { n: 6, c: C.grayM }) + cross(365, 108, C.red, 18);
      s += tag(410, 84, 46, '도입', C.orange, C.orangeL) + tag(410, 114, 46, '본론', C.orange, C.orangeL) + tag(410, 144, 46, '끝', C.orange, C.orangeL);
      s += t(356, 172, '흐름만 기억하고 말한다', { a: 'm', size: 13 });
      s += t(356, 194, '발표는 읽기가 아니라 말하기', { a: 'm', size: 13, b: 1 }) + t(356, 214, '여기서부터 AI는 못 돕는다', { a: 'm', size: 13, c: C.sub });
      return F.svg(480, 242, s);
    } },

  slide5s: {
    cap: '슬라이드는 5초 안에 읽혀야 한다 — 한 장에 세 줄, 설명은 말로',
    draw: function () {
      var s = box(24, 40, 196, 124, { fill: '#fff', c: C.ink, r: 6, w: 1.8 }) + box(260, 40, 196, 124, { fill: '#fff', c: C.ink, r: 6, w: 1.8 });
      for (var i = 0; i < 9; i++) s += line(36, 56 + i * 12, 208 - (i % 3) * 14, 56 + i * 12, { c: C.sub, w: 2.4 });
      s += line(274, 62, 380, 62, { c: C.blue, w: 5 });
      [0, 1, 2].forEach(function (k) { s += '<circle cx="280" cy="' + (92 + k * 22) + '" r="3.5" fill="' + C.ink + '"/>' + line(292, 92 + k * 22, 366 - k * 12, 92 + k * 22, { c: C.sub, w: 3 }); });
      s += box(386, 82, 58, 62, { fill: C.blueL, c: C.blue, r: 4, w: 1.4 }) + F.poly([[392, 138], [408, 112], [420, 126], [430, 104], [440, 138]], { close: 1, fill: C.blue, c: C.blue, w: 1 });
      s += cross(122, 186, C.red, 8) + t(122, 210, '글자가 가득 — 못 읽는다', { a: 'm', size: 13, b: 1, c: C.red });
      s += check(358, 186) + t(358, 210, '제목 + 세 줄 + 그림', { a: 'm', size: 13, b: 1, c: C.green });
      s += circle(240, 100, 26, { fill: C.orangeL, c: C.orange, w: 2 }) + t(240, 101, '5초', { a: 'm', b: 1, size: 16, c: C.orange, halo: false });
      s += t(240, 24, '짝은 한 장을 5초만 본다 · 발표자는 설명하지 않는다', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 228, s);
    } },

  pseudo: {
    cap: '코드보다 순서가 먼저 — 사람 말로 쓴 순서(의사코드)가 틀리면 코드도 틀린다',
    draw: function () {
      var st = ['이름 칸과 [추가] 버튼을 보여 준다', '[추가] → 목록에 이름이 쌓인다', '[뽑기] → 한 명을 무작위로 고른다', '뽑힌 사람을 보여 주고 지운다', '비면 “다 뽑았습니다”'];
      var s = t(150, 26, '① 사람 말로 쓴 순서', { a: 'm', b: 1, size: 15, c: C.blue });
      s += box(14, 40, 280, 176, { fill: C.blueL, c: C.blue, r: 10 });
      st.forEach(function (x, i) { s += F.num(34, 62 + i * 33, String(i + 1), { r: 11, size: 13 }) + t(52, 62 + i * 33, x, { a: 's', size: 13, halo: false }); });
      s += arrow(300, 128, 332, 128, { w: 2.2 });
      s += t(404, 26, '② 그다음에 코드', { a: 'm', b: 1, size: 15, c: C.sub });
      s += box(338, 40, 128, 176, { fill: '#1f2937', c: C.ink, r: 10 });
      [[0, 60, C.orange], [12, 80, '#93c5fd'], [12, 50, '#86efac'], [24, 64, '#93c5fd'], [12, 40, C.orange], [0, 30, '#86efac'], [0, 70, '#93c5fd'], [12, 56, C.orange]].forEach(function (d, i) {
        s += line(352 + d[0], 60 + i * 19, 352 + d[0] + d[1], 60 + i * 19, { c: d[2], w: 3 });
      });
      s += t(240, 240, '코드가 아니다 — 친구에게 설명하듯 순서만 적는다', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 258, s);
    } },

  errloop: {
    cap: '오류가 나면 “안 돼요” 대신, 화면에 뜬 글자를 그대로 붙여넣는다',
    draw: function () {
      var st = [['실행', C.blue, C.blueL], ['오류 메시지', C.red, C.redL], ['그대로 복사', C.orange, C.orangeL], ['AI에게 붙여넣기', C.purple, C.purpleL], ['고친 코드', C.green, C.greenL]];
      var pos = [[90, 60], [240, 60], [390, 60], [390, 160], [150, 160]], w = 128, s = '';
      st.forEach(function (d, i) { s += box(pos[i][0] - w / 2, pos[i][1] - 22, w, 44, { fill: d[2], c: d[1], r: 10 }) + t(pos[i][0], pos[i][1], d[0], { a: 'm', b: 1, size: 14, halo: false }); });
      s += arrow(156, 60, 174, 60, { w: 2, head: 9 }) + arrow(306, 60, 324, 60, { w: 2, head: 9 }) + arrow(390, 84, 390, 136, { w: 2, head: 9 }) +
        arrow(324, 160, 216, 160, { w: 2, head: 9 }) + F.route([[86, 160], [40, 160], [40, 104], [90, 104], [90, 84]], { w: 2, head: 9 });
      s += t(120, 124, '다시 실행', { a: 's', size: 13, c: C.sub });
      s += t(240, 96, '빨간 글씨 · 경고창 · 하얀 화면', { a: 'm', size: 13, c: C.red });
      s += bubble(40, 204, 110, 32, '“안 돼요”', { size: 14, notail: 1, c: C.red }) + cross(166, 220, C.red, 7);
      s += t(190, 212, '영어라도 그대로 옮기면 된다', { a: 's', size: 13, b: 1 }) + t(190, 232, '해석하지 않아도 된다', { a: 's', size: 13, c: C.sub });
      return F.svg(480, 252, s);
    } },

  leading: {
    cap: '유도 질문 — 답을 정해 놓고 물으면 결과가 한쪽으로 기운다',
    draw: function () {
      function scale(cx, tilt, c) {
        var a = tilt * Math.PI / 180, dx = 70 * Math.cos(a), dy = 70 * Math.sin(a), s = '';
        s += line(cx, 150, cx, 196, { w: 3 }) + line(cx - 30, 196, cx + 30, 196, { w: 3 });
        s += line(cx - dx, 150 - dy, cx + dx, 150 + dy, { w: 3, c: c });
        s += box(cx - dx - 26, 150 - dy + 4, 52, 12, { fill: '#fff', c: c, r: 3 }) + box(cx + dx - 26, 150 + dy + 4, 52, 12, { fill: '#fff', c: c, r: 3 });
        return s;
      }
      var s = bubble(20, 16, 210, 56, '', { c: C.red, fill: C.redL, notail: 1 }) + t(125, 34, '“재미없는 줄다리기 대신', { a: 'm', size: 13, halo: false }) +
        t(125, 54, '피구가 좋지 않나요?”', { a: 'm', size: 13, halo: false });
      s += bubble(250, 16, 210, 56, '', { c: C.green, fill: C.greenL, notail: 1 }) + t(355, 34, '“가장 하고 싶은 종목을', { a: 'm', size: 13, halo: false }) +
        t(355, 54, '하나 고르세요.”', { a: 'm', size: 13, halo: false });
      s += t(125, 92, '유도 질문', { a: 'm', b: 1, size: 16, c: C.red }) + t(355, 92, '중립 질문', { a: 'm', b: 1, size: 16, c: C.green });
      s += scale(125, 16, C.red) + scale(355, 0, C.green);
      s += arrow(60, 112, 60, 126, { c: C.red, w: 2.4, head: 9 });
      s += t(125, 222, '답이 한쪽으로 쏠린다', { a: 'm', size: 13, c: C.red }) + t(355, 222, '양쪽이 열려 있다', { a: 'm', size: 13, c: C.green });
      return F.svg(480, 240, s);
    } },

  factvs: {
    cap: '숫자(사실)는 AI가 정리해도, 해석은 내가 쓴다 (숫자는 예시)',
    draw: function () {
      var d = [['피구', 11], ['배드민턴', 6], ['줄다리기', 4], ['계주', 3]], s = t(120, 26, '사실 — 걷은 숫자', { a: 'm', b: 1, size: 15, c: C.blue });
      d.forEach(function (it, i) {
        var y = 52 + i * 34;
        s += t(84, y + 11, it[0], { a: 'e', size: 13 }) + box(92, y, it[1] * 11, 22, { fill: C.blueL, c: C.blue, r: 3, w: 1.4 }) + t(98 + it[1] * 11, y + 11, String(it[1]), { a: 's', size: 13, b: 1 });
      });
      s += t(120, 204, '24명 응답', { a: 'm', size: 13, c: C.sub }) + ai(40, 216, 0.6);
      s += line(240, 16, 240, 236, { c: C.grayM, w: 1.4, dash: '6 5' });
      s += t(360, 26, '해석 — 내가 쓴다', { a: 'm', b: 1, size: 15, c: C.orange });
      ['① 숫자에서 확인된 사실', '② 내가 생각하는 이유', '③ 그래서 하자는 것', '④ 조심할 점'].forEach(function (x, i) {
        s += box(256, 44 + i * 40, 208, 32, { fill: i ? C.orangeL : C.blueL, c: i ? C.orange : C.blue, r: 8, w: 1.4 }) + t(268, 60 + i * 40, x, { a: 's', size: 13, b: 1, halo: false });
      });
      s += person(276, 236, 0.6, C.orange, C.orangeL) + t(296, 222, '우리 반 사정은 내가 안다', { a: 's', size: 13 });
      return F.svg(480, 248, s);
    } },

  criteria: {
    cap: '기준은 내가 고른다 — AI가 준 10개 중 3개만, 순서까지 정한다',
    draw: function () {
      var s = ai(40, 60, 0.8) + t(40, 96, 'AI가 준 후보', { a: 'm', size: 13, c: C.purple });
      var pick = [1, 4, 8];
      for (var i = 0; i < 10; i++) {
        var x = 86 + (i % 5) * 34, y = 40 + Math.floor(i / 5) * 34, on = pick.indexOf(i) >= 0;
        s += circle(x, y, 13, { fill: on ? C.orangeL : C.grayL, c: on ? C.orange : C.grayM, w: on ? 2.2 : 1.4 });
      }
      s += t(154, 100, '기준 10개', { a: 'm', size: 13 });
      s += arrow(246, 56, 284, 56, { c: C.orange, w: 2.4 });
      s += person(310, 84, 0.8, C.orange, C.orangeL);
      ['1순위', '2순위', '3순위'].forEach(function (x, i) { s += tag(340, 34 + i * 30, 70, x, C.orange, C.orangeL); });
      s += t(440, 64, '3개만', { a: 'm', size: 15, b: 1, c: C.orange });
      s += arrow(375, 112, 375, 134, { w: 2, head: 9 });
      /* 비교표 */
      s += box(150, 138, 310, 96, { fill: '#fff', c: C.ink, r: 6 });
      [162, 186, 210].forEach(function (y) { s += line(150, y, 460, y, { c: C.grayM, w: 1.2 }); });
      [228, 306, 384].forEach(function (x) { s += line(x, 138, x, 234, { c: C.grayM, w: 1.2 }); });
      ['후보', '1순위', '2순위', '3순위'].forEach(function (x, i) { s += t(189 + i * 78, 150, x, { a: 'm', size: 13, b: 1, c: i ? C.orange : C.ink, halo: false }); });
      ['가', '나', '다'].forEach(function (x, i) { s += t(189, 174 + i * 24, x, { a: 'm', size: 13, halo: false }); });
      s += t(20, 160, '기준이 많으면', { a: 's', size: 13 }) + t(20, 180, '아무것도 결정되지', { a: 's', size: 13 }) + t(20, 200, '않는다', { a: 's', size: 13 });
      s += t(20, 228, '고르는 사람은 나', { a: 's', size: 13, b: 1, c: C.orange });
      return F.svg(480, 250, s);
    } },

  bias: {
    cap: '이미 마음이 기운 쪽은 좋은 점만 보인다 — 일부러 반대쪽에서 본다',
    draw: function () {
      var s = t(120, 26, '그냥 두면', { a: 'm', b: 1, size: 15, c: C.sub }) + t(360, 26, '일부러 반대쪽을 보면', { a: 'm', b: 1, size: 15, c: C.blue });
      s += line(240, 16, 240, 216, { c: C.grayM, w: 1.4, dash: '6 5' });
      function side(cx, y, name, plus, minus, c, cl) {
        var o = box(cx - 52, y, 104, 70, { fill: cl, c: c, r: 10 }) + t(cx, y + 18, name, { a: 'm', size: 13, b: 1, halo: false });
        o += t(cx, y + 40, '좋은 점 ' + plus, { a: 'm', size: 13, c: C.green, halo: false }) + t(cx, y + 58, '약점 ' + minus, { a: 'm', size: 13, c: C.red, halo: false });
        return o;
      }
      s += side(66, 60, '기운 후보', '●●●', '○', C.orange, C.orangeL) + side(174, 100, '다른 후보', '○', '●●●', C.sub, C.grayL);
      s += line(40, 176, 200, 196, { w: 3 }) + F.poly([[120, 186], [108, 210], [132, 210]], { close: 1, fill: C.grayM, c: C.ink, w: 1.6 });
      s += side(306, 76, '기운 후보', '●●●', '●●●', C.orange, C.orangeL) + side(414, 76, '다른 후보', '●●●', '●●●', C.blue, C.blueL);
      s += line(280, 186, 440, 186, { w: 3 }) + F.poly([[360, 186], [348, 210], [372, 210]], { close: 1, fill: C.grayM, c: C.ink, w: 1.6 });
      s += t(240, 236, '약점을 모르고 고르는 것과, 알고도 고르는 것은 다르다', { a: 'm', size: 13, b: 1 });
      return F.svg(480, 254, s);
    } }

  };
})();
