console.log("base.js 読み込まれた");

const IMAGES = [
  "/static/images/pome_default.png",
  "/static/images/pome_happy.png",
  "/static/images/pome_kyoton.png",
  "/static/images/pome_cloud.png",
];

let clickCount = 0;

function changeImageRandom(imgId) {
  const index = Math.floor(Math.random() * IMAGES.length);
  document.getElementById(imgId).src = IMAGES[index];
}

function changeImageByClick(imgId) {
  const index = clickCount % IMAGES.length;
  document.getElementById(imgId).src = IMAGES[index];
  clickCount++;
}

const POME = {
  DEFAULT: "pome_default.png",
  HAPPY: "pome_happy.png",
  KYOTON: "pome_kyoton.png",
  CLOUD: "pome_cloud.png"
};

// 表情 → メッセージ差分
const POME_TABLE = {
  DEFAULT: {
    img: POME.DEFAULT,
    messages: ["ようこそ", "来てくれてありがとう", "ちょっと慣れてきたね", "ここ、落ち着くね"]
  },
  HAPPY: {
    img: POME.HAPPY,
    messages: ["わーい！", "すごい！", "ありがと！"]
  },
  KYOTON: {
    img: POME.KYOTON,
    messages: ["あれ？？？入力欄が空みたい…", ,"未来の日付みたい…", "てすと（仮）"]
  },
  CLOUD: {
    img: POME.CLOUD,
    messages: ["404NotFound...だいじょうぶ<br>もんだんないよ...うん...", "500??? サーバーエラーだぁ"]
  }
};

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
  if (days < 0) return POME_TABLE.KYOTON;
  if (days <= 7) return POME_TABLE.DEFAULT;
  if (days <= 14) return POME_TABLE.CLOUD;
  return POME_TABLE.HAPPY;
}

// 表示更新（画像＋吹き出し）
function updatePome(days) {
  const state = decidePome(days);

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

