// ------------------------------
// 投稿中...ローディング
// ------------------------------
// 「投稿中...」用ドットアニメ
function startLoadingDots(balloonId, duration = 3000) {
  const balloon = document.getElementById(balloonId);
  if (!balloon) return; // 存在確認

  let dots = 0;

  // 0.5秒ごとにドット更新
  const intervalId = setInterval(() => {
    dots = (dots + 1) % 4; // 0 → 1 → 2 → 3 → 0
    balloon.textContent = "投稿中" + ".".repeat(dots);
  }, 500);

  // duration 経過後に停止して完了メッセージ
  setTimeout(() => {
    clearInterval(intervalId);
    balloon.textContent = "投稿完了！";
  }, duration);
}

function startPosting() {
  const overlay = document.getElementById("postingOverlay");
  const body = document.body;

  overlay.classList.add("open");
  body.style.overflow = "hidden";

  startLoadingDots("loadingMessage", 2000);

  // 投稿完了後に戻す
  setTimeout(endPosting, 3000);
}

function endPosting() {
  const overlay = document.getElementById("postingOverlay");
  const body = document.body;

  overlay.classList.remove("open");
  body.style.overflow = "";
}


