document.addEventListener("DOMContentLoaded", function () {
  const messages = [
    "今日はどんな1日だった？",
    "ひとことでも大丈夫だよ",
    "小さなことでもいいよ",
    "うまく書かなくていいよ"
  ];

  const textarea = document.querySelector(".post-texts");
  if (textarea) {
    const randomIndex = Math.floor(Math.random() * messages.length);
    textarea.placeholder = messages[randomIndex];
  }
});