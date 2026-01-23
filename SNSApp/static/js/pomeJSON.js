// console.log("base.js 読み込まれた");

async function loadPomeData() {
  const res = await fetch("/static/js/pomeData.json");
  return res.json();
}

let clickCount = 0;

async function changeImageRandom(imgId, textId) {
  const POME_DATA = await loadPomeData();
  const keys = Object.keys(POME_DATA["images"]);
  const index = Math.floor(Math.random() * Object.keys(POME_DATA["images"]).length);
  document.getElementById(imgId).src = "/static/images/" + POME_DATA["images"][keys[index]];
  document.getElementById(textId).innerHTML = pickRandom(POME_DATA["states"][keys[index]]["messages"]);
}

async function changeImageByClick(imgId, textId) {
  const POME_DATA = await loadPomeData();
  const keys = Object.keys(POME_DATA["images"]);
  const index = clickCount % Object.keys(POME_DATA["images"]).length;
  clickCount++;
}

// 配列からランダム取得
function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// 日付差分計算
function calcDaysFrom(dateStr) {
  const today = new Date();
  const target = new Date(dateStr);

  today.setHours(0, 0, 0, 0);
  target.setHours(0, 0, 0, 0);

  const diffMs = today - target;
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

// 日数 → 表情決定
function decidePome(days) {
  console.log("decidePome")
  if (days < 0) return "KYOTON";
  if (days <= 7) return "DEFAULT";
  if (days <= 14) return "CLOUD";
  return "HAPPY";
}

// 表示更新（画像＋吹き出し）
async function updatePome(days) {
  const key = decidePome(days);
  const POME_DATA = await loadPomeData();
  const state = POME_DATA["states"][key];

  document.getElementById("pomeImage").src =
    "/static/images/" + state.img;

  document.getElementById("pomeMessage").innerHTML =
    pickRandom(state.messages);
}

// ボタン処理
document.getElementById("checkBtn").addEventListener("click", () => {
  const dateStr = document.getElementById("registerDate").value; // "YYYY-MM-DD"（文字列）
  if (!dateStr) return;

  const days = calcDaysFrom(dateStr);
  updatePome(days);
});
