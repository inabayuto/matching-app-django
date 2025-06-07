# vegeket-app-django セットアップ手順

## アプリ概要

野菜・食品などを扱うECサイトのDjangoバックエンド実装。ユーザー登録、商品一覧・詳細、カート、注文、Stripe決済、管理画面などの機能を持つ。

## ディレクトリ・ファイル構成（主なもの）

- `src/`
  - `manage.py` … Django管理コマンド用エントリポイント
  - `config/` … プロジェクト全体の設定（settings.py, urls.py, wsgi.py など）
  - `base/` … アプリ本体（モデル・ビュー・フォーム・テンプレート等）
    - `models/` … DBモデル（ユーザー、商品、注文、カテゴリ等）
    - `views/` … 各種View（商品一覧・カート・注文・決済・アカウント管理など）
    - `forms/` … ユーザー登録や商品登録などのフォーム定義
    - `templates/` … HTMLテンプレート（ページごとにサブフォルダ分割）
    - `static/` … 静的ファイル（CSS, JS, 画像など）
  - `secrets/` … 秘密鍵や環境変数など（git管理外推奨）

---

このリポジトリはDjango + Docker構成の開発用プロジェクトです。

---

## 1. Docker環境の立ち上げ

1. 必要なファイル（`Dockerfile`, `docker-compose.yml` など）がプロジェクトルートにあることを確認。
2. 以下のコマンドでDockerコンテナをビルド＆起動。

```sh
docker-compose up --build
```

- 初回はイメージのビルドが走るため少し時間がかかります。
- バックグラウンドで起動したい場合は `-d` オプションを付けてください。

```sh
docker compose up -d --build
```

コンテナ内に入る

   ```bash
   docker exec -it CONTAINER ID bash
   ```
---

## 2. Djangoアプリケーションの作成

### 2-1. Djangoプロジェクトの作成

Dockerコンテナ内で以下のコマンドを実行し、Djangoプロジェクト（例: `config`）を作成。

```sh
dockdjango-admin startproject config .
```

- `config` ディレクトリが作成され、Djangoの初期設定ファイルが配置されます。
- すでにプロジェクトが存在する場合はこの手順は不要です。

### 2-2. Djangoアプリ（例: `base`）の作成

```sh
python manage.py startapp base
```

- `base` ディレクトリが作成され、アプリ用の各種ファイルが生成されます。
- 必要に応じて `INSTALLED_APPS` に `base` を追加してください。

---

## 3. マイグレーションの適用

```sh
python manage.py makemigrations

python manage.py migrate
```

---

## 4. 開発サーバーの起動

```sh
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```

- ブラウザで [http://0.0.0.0:8000/](http://0.0.0.0:8000/) にアクセスして動作確認できます。

---

## 5. その他

- superuser作成:  

```sh
python manage.py createsuperuser`
```
---

## 補足
- Dockerコンテナ名（`web`）は `docker-compose.yml` のサービス名に合わせてください。
- コマンドはプロジェクトルートで実行してください。 