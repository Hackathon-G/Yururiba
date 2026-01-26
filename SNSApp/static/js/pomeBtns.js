// ===== state管理 =====
const STATE_KEYS = ["DEFAULT", "HAPPY", "KYOTON", "CLOUD"];

// クリック回数カウント（表情とメッセージで分ける）
let faceClickCount = 0;
let currentStateKey = "DEFAULT"; // ★ 今の表情 state

// ===== 表情クリック =====
async function changeFaceByClick(imgId) {
  const POME_DATA = await loadPomeData();

  const index = faceClickCount % STATE_KEYS.length;
  currentStateKey = STATE_KEYS[index]; // ★ state を更新
  faceClickCount++;

  const imgFile = POME_DATA.states[currentStateKey].img;

  console.log("現在の表情:", currentStateKey);

  document.getElementById(imgId).src =
    "/static/images/" + imgFile;
}

// ===== メッセージクリック =====
async function changeMessageByClick(textId) {
  const POME_DATA = await loadPomeData();

  // ★ 現在の表情 state に紐づく messages だけ使う
  const messages =
    POME_DATA.states[currentStateKey].messages;

  const message = pickRandom(messages);

  console.log("メッセージ:", currentStateKey, message);

  document.getElementById(textId).innerHTML = message;
}

// ===== トグルで state を直接切り替える =====
// ===== ④ 入力（トグル） =====
async function inputToggle(stateKey) {
  const POME_DATA = await loadPomeData();

  if (!POME_DATA.states[stateKey]) {
    console.warn("存在しない state:", stateKey);
    return;
  }

  currentStateKey = stateKey;

  console.log("input → state:", currentStateKey);

  applyStateToUI(stateKey);
}
// UI反映
async function applyStateToUI(stateKey) {
  const POME_DATA = await loadPomeData();
  const state = POME_DATA.states[stateKey];

  // 表情
  document.getElementById("clickImage3").src =
    "/static/images/" + state.img;

  // メッセージ
  const message = pickRandom(state.messages);
  document.getElementById("clickMessage3").innerHTML = message;
}
