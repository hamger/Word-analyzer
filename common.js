// 页面置顶
$('#hg-to-top').click(function () {
  window.scroll(0, 0);
})

// 页面置底
$('#hg-to-bottom').click(function () {
  window.scroll(0, document.body.clientHeight);
})

// 根据页面位置显示置顶或置底的按钮
var toTopBtn = document.getElementById('hg-to-top');
var toBottomBtn = document.getElementById('hg-to-bottom');
window.addEventListener('scroll', (e) => {
  var scrollTop = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
  if (scrollTop > window.screen.availHeight) {
    toTopBtn.style.display = 'block';
    toBottomBtn.style.display = 'none';
  }
  else {
    toTopBtn.style.display = 'none';
    toBottomBtn.style.display = 'block';
  }
});

// 页面跳转
function toward (url) {
  window.location.href = url
}