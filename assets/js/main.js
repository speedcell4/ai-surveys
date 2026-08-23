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
})();
