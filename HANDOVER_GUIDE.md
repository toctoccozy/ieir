# I･E･I オンラインショップ リニューアル 引き継ぎガイド

## 📋 プロジェクト概要

インペリアル・エンタープライズ株式会社のECサイトリニューアルプロトタイプです。
既存のCGIベースのシステムから、モダンなLaravel + Tailwind CSSベースのシステムへの移行を前提に設計されています。

### 実装済み機能

#### ✅ 完成済みページ
- **商品詳細ページ**: `/views/products/51300/51325.html`
- **カテゴリページ（ムーミン）**: `/views/categories/moomin/index.html`

#### ✅ コンポーネント
- **ヘッダー**: `/views/components/header.html`
- **フッター**: `/views/components/footer.html`
- **コンポーネントローダー**: `/public/js/components/component-loader.js`

---

## 🏗️ 技術スタック

### プロトタイプ（現在）
```json
{
  "フロントエンド": "HTML5 + Tailwind CSS 3.4.1（CDN）",
  "JavaScript": "jQuery 3.7.1 + Alpine.js 3.13.5（CDN）",
  "スライダー": "Slick Carousel 1.8.1（CDN）",
  "フォント": "Noto Sans JP（Google Fonts）"
}
```

### 本番環境（移行後）
```json
{
  "バックエンド": "Laravel 10.x",
  "テンプレート": "Blade",
  "CSS": "Tailwind CSS 3.4.1（npm）",
  "JavaScript": "Alpine.js 3.13.5（npm）",
  "ビルド": "Laravel Mix または Vite"
}
```

---

## 📁 ディレクトリ構造

```
ieir/
├── README.md                     # プロジェクト説明
├── HANDOVER_GUIDE.md            # このファイル
├── package.json                  # npm依存関係
├── tailwind.config.js            # Tailwind設定
│
├── public/                       # 静的ファイル（Laravel public/）
│   ├── css/
│   ├── js/
│   │   └── components/
│   │       └── component-loader.js
│   └── img/
│       ├── categories/moomin/    # カテゴリ画像
│       ├── products/51300/51325/ # 商品画像
│       ├── parts/buttons/        # ボタン画像
│       └── parts/icons/          # アイコン画像
│
└── views/                        # HTMLテンプレート（Laravel resources/views/）
    ├── categories/moomin/        # カテゴリページ
    ├── products/51300/           # 商品詳細ページ  
    └── components/               # 共通コンポーネント
```

---

## 🎨 デザインシステム

### カラーパレット
```css
:root {
  --iei-primary: #2C5282;      /* 紺色（メインカラー） */
  --iei-secondary: #ED8936;    /* オレンジ（アクセント） */
  --moomin: #7FB3D5;           /* ムーミンブルー */
  --charaffine: #FF6B6B;       /* コーラルレッド */
  --premico: #4ECDC4;          /* ターコイズ */
}
```

### レスポンシブブレークポイント
```javascript
{
  'sm': '640px',   // タブレット
  'md': '768px',   // タブレット（横）
  'lg': '1024px',  // デスクトップ
  'xl': '1280px',  // 大画面
  '2xl': '1536px'  // 超大画面
}
```

### コンポーネントクラス
```css
.btn-primary     // プライマリボタン
.product-card    // 商品カード
.section-title   // セクションタイトル
.nav-link       // ナビゲーションリンク
```

---

## ⚙️ 実装機能詳細

### 1. 商品詳細ページ (`51325.html`)

#### 🖼️ ギャラリー機能
- サムネイルクリックで大画像切り替え（フェード効果）
- 大画像クリックでモーダル拡大表示
- ホバーヒント表示
- アクティブサムネイルの視覚的フィードバック

#### 🛒 カート機能（モック）
- フォームバリデーション（サイズ未選択時エラー）
- ローディング状態表示
- ローカルストレージでのデータ保存
- SVGアイコン付き通知メッセージ

#### 📱 レスポンシブ対応
- PC/SP画像の統合（PC版でレスポンシブ対応）
- グリッドレイアウトでの価格・仕様表示
- モバイルファーストデザイン

### 2. カテゴリページ (`moomin/index.html`)

#### 🎠 スライダー機能
- Slick Carouselによる自動再生スライダー
- カスタムアロー・ドット
- レスポンシブ設定

#### 📦 商品リスト
- カード型レイアウト
- ホバーエフェクト
- 商品詳細へのリンク

### 3. 共通コンポーネント

#### 📤 ヘッダー (`components/header.html`)
- レスポンシブナビゲーション
- ドロップダウンメニュー
- モバイルハンバーガーメニュー
- カート数量のリアルタイム表示
- 検索機能
- スクロール時の固定ヘッダー

#### 📥 フッター (`components/footer.html`)
- 4カラムレスポンシブレイアウト
- SNSアイコン
- ニュースレター登録
- 法的情報・認証マーク

#### 🔧 コンポーネントローダー
```javascript
// 使用例
loadComponent('header', '#header-container');
loadComponents([
  {name: 'header', target: '#header-container'},
  {name: 'footer', target: '#footer-container'}
]);
```

---

## 🔄 Laravel移行手順

### Step 1: Laravel環境構築
```bash
composer create-project laravel/laravel iei-shop
cd iei-shop
npm install tailwindcss@3.4.1 alpinejs@3.13.5
npm install -D @tailwindcss/forms @tailwindcss/typography
```

### Step 2: ファイル移行
```bash
# HTMLファイルをBladeテンプレートに変換
views/ → resources/views/
public/ → public/

# 拡張子変更
*.html → *.blade.php
```

### Step 3: Blade変換
```html
<!-- Before -->
<!-- @include('components.header') -->

<!-- After -->
@include('components.header')
```

### Step 4: ルート設定
```php
// routes/web.php
Route::get('/products/51300/51325', [ProductController::class, 'show']);
Route::get('/categories/moomin', [CategoryController::class, 'moomin']);
```

### Step 5: API実装
```php
// 商品データ取得API
Route::apiResource('products', ProductController::class);
Route::post('cart/add', [CartController::class, 'add']);
```

---

## 🧪 テスト項目

### 機能テスト
- [ ] ギャラリー画像切り替え
- [ ] モーダル拡大表示
- [ ] カートモック機能
- [ ] フォームバリデーション
- [ ] スライダー動作
- [ ] レスポンシブ表示
- [ ] コンポーネント読み込み

### パフォーマンステスト
- [ ] 画像読み込み速度
- [ ] JavaScript実行速度
- [ ] モバイル表示速度

### ブラウザ互換性
- [ ] Chrome（最新版）
- [ ] Safari（最新版）
- [ ] Edge（最新版）
- [ ] Firefox（最新版）
- [ ] iOS Safari
- [ ] Android Chrome

---

## 📋 実装予定機能（本番環境）

### データベース設計
```sql
-- 主要テーブル
users           -- 会員情報
products        -- 商品情報
categories      -- カテゴリ
orders          -- 注文
order_items     -- 注文明細
cart_items      -- カート
```

### API設計
```
GET    /api/products          -- 商品一覧
GET    /api/products/{id}     -- 商品詳細
POST   /api/cart/add          -- カート追加
GET    /api/cart              -- カート取得
POST   /api/orders            -- 注文作成
```

### セキュリティ
- CSRF対策（Laravel標準）
- XSS対策（Blade自動エスケープ）
- SQL Injection対策（Eloquent ORM）
- 認証（Laravel Sanctum）
- HTTPS必須

---

## 🔧 開発環境セットアップ

### プロトタイプ確認用
1. ローカルサーバーで `ieir/views/` ディレクトリを開く
2. `51325.html` または `moomin/index.html` を表示
3. ブラウザの開発者ツールでレスポンシブ確認

### Laravel開発環境
```bash
# 依存関係インストール
composer install
npm install

# 設定
cp .env.example .env
php artisan key:generate

# データベース
php artisan migrate
php artisan db:seed

# アセットビルド
npm run dev

# サーバー起動
php artisan serve
```

---

## 📞 サポート・質問

### 技術的な質問
- プロトタイプ実装: [開発者連絡先]
- Laravel移行: [技術責任者連絡先]

### デザイン・UX
- UI/UX設計: [デザイナー連絡先]
- ブランドガイドライン: [マーケティング連絡先]

---

## 📋 チェックリスト

### 引き継ぎ前確認
- [ ] 全ページの動作確認完了
- [ ] レスポンシブ表示確認完了
- [ ] ブラウザ互換性確認完了
- [ ] コード整理・最適化完了
- [ ] ドキュメント作成完了

### 引き継ぎ時確認
- [ ] ファイル構造の説明完了
- [ ] 技術スタックの説明完了
- [ ] 実装機能の説明完了
- [ ] Laravel移行手順の説明完了
- [ ] 質疑応答完了

---

**更新日**: 2024年1月14日  
**バージョン**: 1.0.0  
**作成者**: I･E･I 開発チーム