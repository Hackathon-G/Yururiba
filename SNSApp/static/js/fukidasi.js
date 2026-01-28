// ------------------------------
// 吹き出し演出（遊び）
// ------------------------------
// 吹き出しをふわっと表示する関数
function showBubbleWithText(balloon, text) {
  if (!balloon) return;

  // 初期状態に戻す
  balloon.classList.add("hidden"); 
  balloon.innerHTML = text;

  // 少し遅延して表示
  setTimeout(() => {
    balloon.classList.add("show");
  }, 50); // 50msで次の tick
}

// 例: ランダム表示・クリック回数表示の中で使用
// クリック回数用関数例（既存 changeImageByClick の中に組み込むイメージ）
async function changeImageByClick(imgId, textId) {
  const POME_DATA = await loadPomeData();
  const keys = Object.keys(POME_DATA.images);
  const index = clickCount % keys.length;
  clickCount++;

  // 画像差し替え
  document.getElementById(imgId).src = "/static/images/" + POME_DATA.images[keys[index]];

  // 吹き出し差し替え + 演出
  const balloon = document.getElementById(textId);
  const messages = POME_DATA.states[keys[index]].messages;
  showBubbleWithText(balloon, pickRandom(messages));
}

// ランダム表示用にも同様に showBubbleWithText を使う
async function changeImageRandom(imgId, textId) {
  const POME_DATA = await loadPomeData();
  const keys = Object.keys(POME_DATA.images);
  const index = Math.floor(Math.random() * keys.length);

  document.getElementById(imgId).src = "/static/images/" + POME_DATA.images[keys[index]];

  const balloon = document.getElementById(textId);
  const messages = POME_DATA.states[keys[index]].messages;
  showBubbleWithText(balloon, pickRandom(messages));
}
