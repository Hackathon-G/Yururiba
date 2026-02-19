DROP DATABASE IF EXISTS snsapp_y;

DROP USER IF EXISTS 'testuser_y'@'%';


CREATE USER 'testuser_y'@'%' IDENTIFIED BY 'testuser_y';

CREATE DATABASE IF NOT EXISTS snsapp_y
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;


GRANT ALL PRIVILEGES ON snsapp_y.* TO 'testuser_y'@'%';

FLUSH PRIVILEGES;

USE snsapp_y;

CREATE TABLE
    users (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        UNIQUE KEY uq_users_email (email)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    hobbies (
        hobby_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        hobby_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (hobby_id),
        UNIQUE KEY uq_hobbies_hobby_name (hobby_name)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 中間テーブル
CREATE TABLE
    user_hobbies (
        user_id BIGINT UNSIGNED NOT NULL,
        hobby_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (user_id, hobby_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (hobby_id) REFERENCES hobbies(hobby_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


CREATE TABLE
    posts (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        hobby_id BIGINT UNSIGNED NOT NULL,
        post_text TEXT NOT NULL,
        -- post_image VARCHAR(255),
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        deleted_at DATETIME (6) DEFAULT NULL,
        PRIMARY KEY (id),
        KEY idx_posts_user_id_hobby_id (user_id, hobby_id),
        -- posts テーブルの user_id カラムは users テーブルの id カラムを参照する外部キーとして定義
        CONSTRAINT fk_posts_user_hobby FOREIGN KEY (user_id, hobby_id) REFERENCES user_hobbies (user_id, hobby_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    tags (
        tag_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        hobby_id BIGINT UNSIGNED NOT NULL,
        tag_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (tag_id),
        UNIQUE KEY uq_tags_tag_name (tag_name)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
    

-- 中間テーブル
CREATE TABLE
    saved_posts (
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
        saved_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        deleted_at DATETIME (6) DEFAULT NULL,
        PRIMARY KEY (user_id, post_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (post_id) REFERENCES posts(id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    post_tags (
        post_id BIGINT UNSIGNED NOT NULL,
        tag_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (post_id, tag_id),
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


INSERT INTO users (user_name, email, password, created_at)
VALUES 
    -- ('山田太郎', 'taro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    -- ('鈴木二郎', 'jiro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244');
    ('pome', 'pome@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', '2026-01-01 09:00:00'),
    ('pomeko', 'pomeko@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', '2026-01-10 09:00:00'),
    ('やすよ', 'yasuyo@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', '2025-12-01 09:00:00'),
    ('ともこ', 'tomoko@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', '2025-12-21 09:00:00');

INSERT INTO hobbies (hobby_id, hobby_name)
VALUES 
    (1, 'スポーツ'),
    (2, 'アウトドア'),
    (3, '美容・ライフ'),
    (4, '料理・グルメ'),
    (5, '旅行'),
    (6, '音楽'),
    (7, '資格'),
    (8, 'その他');

INSERT INTO user_hobbies (user_id, hobby_id)
VALUES
    (1, 1),
    (1, 5),
    (1, 6),
    (2, 2),
    (2, 4),
    (3, 4),
    (4, 3);


INSERT INTO posts (user_id, post_text, hobby_id)
VALUES
    (1, 'ゆるゆる', 5),
    (2, '今日はとても良い天気ですね。', 2), 
    (3, '天津飯食べたい！', 4),
    (4, 'こんにちは！初めての投稿です。', 3),
    (1, 'テスト', 1),
    (1, '複数投稿の表示確認用！', 6),
    (1, '大変だ～', 5);

INSERT INTO tags (tag_id, hobby_id, tag_name)
VALUES
    (1, 1, '野球'),
    (2, 1, 'サッカー'),
    (3, 1, 'バスケットボール'),
    (4, 1, 'ラグビー'),
    (5, 1, 'その他のスポーツ'),
    (6, 2, 'BBQ'),
    (7, 2, '釣り'),
    (8, 2, 'サイクリング'),
    (9, 2, 'その他のアウトドア');











-- MySQL コンテナへの接続
-- docker exec -it MySQL bash
-- mysql -u root -p

-- ----------------------
--         重要!!!
-- ----------------------
-- init.sqlは、書き換える度に、
-- docker compose down -v && docker compose up --build
-- で、キャッシュを消して再構築し直すほうが良い！！！
-- そこでエラーが出たら一つ一つ潰していく。



-- データベースの中身（一覧）を確認
-- SHOW DATABASES;
-- 使うデータベースを切り替える
-- USE データベース名;
-- 現在のデータベースを確認
-- SELECT DATABASE();
-- テーブルに値（データ）を挿入
-- INSERT INTO テーブル名（カラム名,カラム名,...）VALUES(データ, データ),(データ,'データ');
-- 例：insert into item_category(category_id, category_name) values (1,”家具”), (2,”飲料”), (3,”食品”);
-- 作ったテーブルを見る
-- show tables;　（全てのテーブル）
-- テーブルの構造を見る
-- DESC テーブル名;
-- show columns from テーブル名;
-- 値（データ）を更新
-- UPDATE [テーブル名] SET [COLUMN名] = '新しい値';
-- UPDATE user SET name = '新しい名前';
-- 値（データ）を削除
-- DELETE FROM [テーブル名] WHERE カラム名 = 値;
-- 例：
-- DELETE FROM user WHERE id = 10;