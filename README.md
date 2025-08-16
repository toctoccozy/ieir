# I･E･I オンラインショップ プロトタイプ

## 概要
このプロジェクトは、インペリアル・エンタープライズ株式会社のECサイトリニューアルのためのプロトタイプです。
開発会社への引き継ぎを前提に、Laravel移行しやすい構造で作成しています。

## 技術スタック

### フロントエンド（プロトタイプ）
- HTML5
- Tailwind CSS 3.4.1（CDN）
- Alpine.js 3.13.5（CDN）
- Vanilla JavaScript

### 本番環境（予定）
- Laravel 10.x
- Blade テンプレートエンジン
- Tailwind CSS 3.4.1（npm）
- Alpine.js 3.13.5（npm）

## ディレクトリ構造

```
ieir/
├── README.md                     # このファイル
├── tailwind.config.js           # Tailwind設定
├── package.json                 # npmパッケージ情報
├── public/                      # 静的ファイル（Laravel publicに対応）
│   ├── css/                     # スタイルシート
│   ├── js/                      # JavaScript
│   └── img/                     # 画像ファイル
└── views/                       # HTMLテンプレート（Laravel viewsに対応）
    ├── index.html              # トップページ
    ├── layouts/                # レイアウトテンプレート
    ├── components/             # 共通コンポーネント
    └── pages/                  # 各ページ
```

## 使用ライブラリバージョン

| ライブラリ | CDN バージョン | npm バージョン | 用途 |
|-----------|---------------|---------------|------|
| Tailwind CSS | 3.4.1 | 3.4.1 | UIフレームワーク |
| Alpine.js | 3.13.5 | 3.13.5 | 軽量リアクティブ |
| jQuery | 3.7.1 | - | 既存コード互換用 |

## カスタム設定

### Tailwindカスタムカラー
- `iei-primary`: #2C5282（紺色）
- `iei-secondary`: #ED8936（オレンジ）
- `charaffine`: #FF6B6B（コーラルレッド）
- `premico`: #4ECDC4（ターコイズ）

### カスタムコンポーネントクラス
- `.btn-primary`: プライマリボタン
- `.product-card`: 商品カード
- `.section-title`: セクションタイトル

## 開発環境セットアップ

### プロトタイプ開発（CDN利用）
1. このディレクトリをローカルサーバーで開く
2. ブラウザでindex.htmlを開く

### 本番環境への移行手順

1. **Laravelプロジェクト作成**
```bash
composer create-project laravel/laravel iei-shop
cd iei-shop
```

2. **npm パッケージインストール**
```bash
npm install tailwindcss@3.4.1 alpinejs@3.13.5
npm install -D @tailwindcss/forms @tailwindcss/typography
```

3. **ファイル移行**
- `/public/` → Laravel `/public/`
- `/views/` → Laravel `/resources/views/`
- HTMLファイルを `.blade.php` に変換

4. **Blade変換**
- `<!-- @include('components.header') -->` → `@include('components.header')`
- `<!-- @yield('content') -->` → `@yield('content')`
- データ属性の置換

## API仕様（要実装）

### 商品関連
- `GET /api/products` - 商品一覧
- `GET /api/products/{id}` - 商品詳細
- `GET /api/categories` - カテゴリ一覧

### カート関連
- `GET /api/cart` - カート内容取得
- `POST /api/cart/add` - カート追加
- `DELETE /api/cart/{id}` - カート削除

### 認証関連
- `POST /api/login` - ログイン
- `POST /api/register` - 会員登録
- `POST /api/logout` - ログアウト

## データベース設計（参考）

### テーブル構成
- users（会員）
- products（商品）
- categories（カテゴリ）
- orders（注文）
- order_items（注文明細）
- cart_items（カート）

## セキュリティ考慮事項

1. **CSRF対策**: Laravel標準機能を使用
2. **XSS対策**: Bladeの自動エスケープ
3. **SQL Injection対策**: Eloquent ORM使用
4. **認証**: Laravel Sanctum推奨
5. **HTTPS**: 本番環境では必須

## 注意事項

### CDNから本番への移行時
1. CDNのバージョンと同じnpmパッケージを使用
2. Tailwind設定ファイルをそのまま利用
3. カスタムクラスの動作確認必須

### ブラウザ対応
- Chrome 最新版
- Safari 最新版
- Edge 最新版
- Firefox 最新版

## 連絡先
開発に関する質問は以下までご連絡ください：
- プロジェクト管理者: [連絡先]
- 技術的な質問: [連絡先]

## 更新履歴
- 2024-01-14: 初版作成
- [更新日]: [更新内容]