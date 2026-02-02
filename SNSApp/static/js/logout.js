// ==============================
// JSONデータ読み込み
// ==============================
let POME_DATA = null;

async function initPomeData() {
  const res = await fetch("/static/js/pomeData.json");
  POME_DATA = await res.json();
}

document.addEventListener("DOMContentLoaded", async () => {
  await initPomeData();
});

// ==============================
// ログアウト処理
// ==============================
function startLogout(event) {
  event.preventDefault();
  const overlay = document.getElementById("logoutOverlay");
  const message = document.getElementById("logoutMessage");
  const pome = document.getElementById("logoutPome");

  // 初期化
  const logoutState = POME_DATA.states.LOGOUT;
  const messages = logoutState.messages;
  message.textContent =
    messages[Math.floor(Math.random() * messages.length)];
  pome.src = "/static/images/" + logoutState.img;

  overlay.classList.add("open");
  document.body.style.overflow = "hidden";

  // 少し見せてからログアウト
  setTimeout(() => {
    window.location.href = "/logout";
  }, 1000);
}

