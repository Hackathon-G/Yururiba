// ==============================
// JSONデータ読み込み
// ==============================
async function loadPomeData() {
  const res = await fetch("/static/js/pomeData.json");
  return res.json();
}

// ==============================
// ランダム取得ヘルパー
// ==============================
function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// ==============================
// 吹き出しフェード + 文字遅延
// ==============================
function showBubbleWithText(balloon, text) {
  balloon.classList.remove("show"); // 初期化
  balloon.innerHTML = text;

  // 吹き出しふわっと表示
  setTimeout(() => {
    balloon.classList.add("show");
  }, 200); // 0.2秒遅延

  // 文字も少し遅らせる場合は span に分けてもOK
}

// ==============================
// クリック回数カウンター
// ==============================
let clickCount = 0;

// ==============================
// ランダム表示
// ==============================
async function changeImageRandom(imgId, textId) {
  const POME_DATA = await loadPomeData();
  const keys = Object.keys(POME_DATA.images);
  const index = Math.floor(Math.random() * keys.length);

  document.getElementById(imgId).src = "/static/images/" + POME_DATA.images[keys[index]];

  const balloon = document.getElementById(textId);
  const messages = POME_DATA.states[keys[index]].messages;
  showBubbleWithText(balloon, pickRandom(messages));
}

// ==============================
// クリック回数で表示変更
// ==============================
async function changeImageByClick(imgId, textId) {
  const POME_DATA = await loadPomeData();
  const keys = Object.keys(POME_DATA.images);
  const index = clickCount % keys.length;
  clickCount++;

  document.getElementById(imgId).src = "/static/images/" + POME_DATA.images[keys[index]];

  const balloon = document.getElementById(textId);
  const messages = POME_DATA.states[keys[index]].messages;
  showBubbleWithText(balloon, pickRandom(messages));
}

// ==============================
// 日付差分計算
// ==============================
function calcDaysFrom(dateStr) {
  const today = new Date();
  const target = new Date(dateStr);

  today.setHours(0, 0, 0, 0);
  target.setHours(0, 0, 0, 0);

  const diffMs = today - target;
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

// ==============================
// 日数 → 表情決定
// ==============================
function decidePome(days) {
  if (days < 0) return "KYOTON";
  if (days <= 7) return "DEFAULT";
  if (days <= 14) return "CLOUD";
  return "HAPPY";
}

// ==============================
// 日付による更新
// ==============================
async function updatePome(days) {
  const key = decidePome(days);
  const POME_DATA = await loadPomeData();
  const state = POME_DATA.states[key];

  document.getElementById("pomeImage").src = "/static/images/" + state.img;
  const balloon = document.getElementById("pomeMessage");
  showBubbleWithText(balloon, pickRandom(state.messages));
}

// ==============================
// ボタン処理
// ==============================
document.getElementById("checkBtn")?.addEventListener("click", () => {
  const dateStr = document.getElementById("registerDate").value;
  if (!dateStr) return;

  const days = calcDaysFrom(dateStr);
  updatePome(days);
});

