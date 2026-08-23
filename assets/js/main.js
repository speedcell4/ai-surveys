(function () {
  'use strict';

  // 三层阅读深度切换：脉络(1) / 完整(2) / 深读(3)
  var btns = Array.prototype.slice.call(document.querySelectorAll('.lvbtn'));
  function setLv(lv) {
    document.body.classList.remove('lv1', 'lv2', 'lv3');
    document.body.classList.add('lv' + lv);
    btns.forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-lv') === lv);
    });
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () { setLv(b.getAttribute('data-lv')); });
  });
  setLv('2');

  // LaTeX 渲染（Temml → MathML Core）：$…$ 行内、$$…$$ 独立行；<code> 里也要渲染
  if (window.temml && window.temml.renderMathInElement) {
    window.temml.renderMathInElement(document.body, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false }
      ],
      ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'option']
    });
  }
})();
