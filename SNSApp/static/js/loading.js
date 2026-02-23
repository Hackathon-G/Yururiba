// ------------------------------
// 投稿中ローディング
// ------------------------------
document.querySelector(".post-input form").addEventListener("submit", async function(e) {
  e.preventDefault();   // ページ遷移を止める

  startPosting();       // 既存関数を使う

  const formData = new FormData(this);

  const response = await fetch("/posts", {
    method: "POST",
    body: formData
  });

  if (response.redirected) {
    setTimeout(() => {
      window.location.href = response.url;
    }, 3000);  // アニメーション時間と合わせる
  }

});

function startLoadingDots(balloonId, imgId, duration = 2000) {
  const balloon = document.getElementById(balloonId);
  if (!balloon) return;

  let dots = 0;
  balloon.classList.remove("show"); // 初期化
  const intervalId = setInterval(() => {
    dots = (dots + 1) % 4;
    balloon.textContent = "投稿中" + ".".repeat(dots);
  }, 600);

  setTimeout(() => {
    clearInterval(intervalId);
    balloon.textContent = "投稿完了！";
    document.getElementById(imgId).src = "/static/" + "images/pome_happy.png";
  }, duration);
}

function startPosting() {
  const overlay = document.getElementById("postingOverlay");
  const body = document.body;
  const message = document.getElementById("loadingMessage");
  const pome = document.getElementById("postingPome");

  message.textContent = "投稿中";
  pome.src = "/static/" + "images/pome_default.png";

  overlay.classList.add("open");
  body.style.overflow = "hidden";

  startLoadingDots("loadingMessage", "postingPome", 2000);

  // 完了演出を見せてから戻す
  setTimeout(endPosting, 3000);
}

function endPosting() {
  const overlay = document.getElementById("postingOverlay");
  const body = document.body;

  overlay.classList.remove("open");
  body.style.overflow = "";
}
