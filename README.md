# マッチングアプリ Django バックエンド

Django と Django REST Framework を使用したマッチングアプリケーションのバックエンドAPIです。

## プロジェクト概要

このプロジェクトは、ユーザーがプロフィールを作成し、お互いにマッチングしてダイレクトメッセージを送信できるマッチングアプリのバックエンドシステムです。Stripe決済システムを統合し、有料会員登録機能も実装されています。

## 主な機能

### ユーザー管理
- カスタムユーザーモデル（UUID、メール認証）
- JWT認証システム
- ユーザー登録・ログイン・プロフィール管理

### プロフィール機能
- 年齢、性別、自己紹介などの基本情報
- 本人確認（KYC）機能
- 異性のプロフィール一覧表示

### マッチング機能
- ユーザー間のアプローチ機能
- マッチング承認・拒否システム
- マッチング状態の管理

### メッセージ機能
- マッチング済みユーザー間のダイレクトメッセージ
- 送信・受信メッセージの管理
- メッセージ履歴の表示

### 決済機能
- Stripe決済システム統合
- サブスクリプション型の有料会員登録
- 決済完了後のユーザーアクティベーション

## 技術スタック

### バックエンド
- **Django 4.1.10** - Webフレームワーク
- **Django REST Framework 4.7.0** - API構築
- **Django CORS Headers 3.16.0** - CORS対応
- **Djoser 2.3.1** - 認証システム
- **django-environ 0.12.0** - 環境変数管理

### 決済・認証
- **Stripe 12.2.0** - 決済システム
- **djangorestframework-simplejwt** - JWT認証

### データベース
- **SQLite** - 開発環境用データベース
- **PostgreSQL** - 本番環境対応可能

### コンテナ化
- **Docker** - コンテナ化
- **Docker Compose** - マルチコンテナ管理

## セットアップ手順

### 前提条件
- Python 3.9.11以上
- Docker & Docker Compose
- Git

### 1. リポジトリのクローン
```bash
git clone https://github.com/inabayuto/matching-app-django.git
cd matching-app-django
```

### 2. 環境変数の設定
`src/secrets/.env.dev` ファイルを作成し、必要な環境変数を設定：

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGIN_WHITELIST=http://localhost:3000,http://127.0.0.1:3000

# データベース設定
DATABASE_URL=sqlite:///db.sqlite3

# メール設定
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
DEFAULT_FROM_EMAIL=your-email@gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Stripe設定
STRIPE_ITEM_PRICE=price_your_stripe_price_id
STRIPE_API_SECRET_KEY=sk_test_your_stripe_secret_key

# アプリケーションURL
MY_URL=http://127.0.0.1:8000
```

### 3. Docker環境での起動
```bash
# コンテナのビルドと起動
docker compose up -d --build

# コンテナ内に入る
docker exec -it CONTAINER ID bash
```

### 4. データベースマイグレーション
```bash
# コンテナ内でマイグレーション実行
python manage.py makemigrate
python manage.py migrate

# スーパーユーザー作成（オプション）
python manage.py createsuperuser
```

### 5. 開発サーバー起動
```bash
# コンテナ内でサーバー起動
python manage.py runserver 0.0.0.0:8000
```

## API仕様

### 認証
- **JWT認証**を使用
- ヘッダー: `Authorization: JWT <token>`

### 主要エンドポイント

#### ユーザー管理
- `POST /api/users/create/` - ユーザー登録
- `GET /api/users/<pk>/` - ユーザー詳細取得
- `PUT /api/users/<pk>/` - ユーザー情報更新

#### プロフィール管理
- `GET /api/profiles/` - 相手候補プロフィール一覧
- `GET /api/users/me/` - 自分のプロフィール取得・更新

#### マッチング
- `GET /api/favorite/` - マッチング一覧取得
- `POST /api/favorite/` - アプローチ送信
- `PUT /api/favorite/<id>/` - マッチング承認・拒否

#### メッセージ
- `GET /api/dm/` - 送信メッセージ一覧
- `POST /api/dm/` - メッセージ送信
- `GET /api/dm-inbox/` - 受信メッセージ一覧

#### 決済
- `GET /api/users/<token_id>/payment/` - Stripe決済ページ
- `GET /api/users/payment/cancel/` - 決済キャンセル
- `GET /api/users/<activate_token>/activation/` - ユーザーアクティベーション
