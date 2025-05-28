document.addEventListener('DOMContentLoaded', function() {
  const nav = document.querySelector("#navArea");
  const btn = document.querySelector(".toggle-btn");
  console.log("btn:", btn); // 追加

  if (btn) {
    btn.onclick = () => {
      nav.classList.toggle("open");
    };
  } else {
    console.error(".toggle-btn が見つかりませんでした。");
  }
});