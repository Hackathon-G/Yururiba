-- =========================
-- view.sql
-- このファイルはアプリで使用する VIEW 定義をまとめたもの
-- 実行順序：
--   1. init.sql（テーブル作成）
--   2. view.sql（ビュー作成）
-- =========================

-- 既存のビューがあれば削除（再実行できるように）
DROP VIEW IF EXISTS saved_posts_view;
DROP VIEW IF EXISTS timeline_view;
DROP VIEW IF EXISTS my_posts_view;

-- なぜ書くのか
-- 「これは何のファイルか」一瞬で分かる
-- DROP VIEW IF EXISTS を書いておくと
-- 👉 何度でも実行できる（超重要）
-- 実務でもほぼ必ずこの形
-- 👉 init.sql と同じノリでOK
-- 「DBの初期化ファイルの一種」だと思ってください。


-- 保存画面（/list）の保存投稿一覧（/bookmark/posts）
CREATE VIEW saved_posts_view AS
	SELECT
		-- 保存者、投稿ID、投稿者、内容、保存日時
		saved_posts.user_id,
		posts.post_id,
		users.user_name,
		posts.post_text,
		posts.post_image,
		saved_posts.saved_at
	-- saved_postsテーブルを基準に
	FROM saved_posts
	-- post_idの紐付け
	-- saved_postsテーブルのpost_idとpostsテーブルのpost_idの紐付け
	JOIN posts ON posts.post_id = saved_posts.post_id
	-- 投稿者の紐付け
	-- saved_postsテーブルのuser_idとpostsテーブルのuser_idの紐付け
	JOIN users ON users.user_id = posts.user_id;


-- タイムライン(/timeline)の投稿一覧(/hobbies/{hobby_id}/posts)
CREATE VIEW timeline_view AS
	SELECT 
		-- 投稿ID、投稿者、内容、作成日時
		-- 注意！　　posts.hobby_idを含めると投稿者の趣味全部が表示される
		posts.post_id,
		users.user_name,
		post.post_text,
		posts.post_image,
		posts.created_at,
		user_hobbies.hobby_id
	FROM posts
	JOIN users ON users.user_id = posts.user_id
	JOIN user_hobbies ON user_hobbies.hobby_id = posts.hobby_id;

-- 注意！　　以下のようにすると投稿を見ているユーザーの趣味と、投稿者の趣味の共通の趣味全てが表示される
-- JOIN user_hobbies ON user_hobbies.user_id = users.user_id

		
-- home(/home)の自分の投稿一覧（/me/posts)
CREATE VIEW my_posts_view AS
	SELECT 
		posts.post_id,
		posts.post_text,
		posts.post_image,
		posts.created_at,
		posts.user_id
	FROM posts;