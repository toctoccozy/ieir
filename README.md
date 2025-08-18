# IEI リニューアルプロジェクト - テスト実装

## 概要
このプロジェクトは、既存のiei_renewalサイトをHTML/Tailwind CSS/JavaScriptベースで再構築したテスト実装です。
現在、51325、51347の商品詳細ページとムーミンカテゴリページをサンプルとして実装済みです。
外部開発会社によるLaravelベースの本実装に向けた、フロントエンドのプロトタイプとなります。

## A. ディレクトリ構成

```
ieir/
├── public/                    # 静的リソース
│   ├── css/                  # スタイルシート
│   │   └── customization.css # Tailwind用カスタムCSS
│   ├── img/                  # 画像リソース
│   │   ├── categories/       # カテゴリページ用画像
│   │   │   └── moomin/      # ムーミンカテゴリ画像
│   │   ├── parts/            # 共通パーツ画像
│   │   │   ├── logo/        # ロゴ画像
│   │   │   └── moomin/      # ムーミン共通画像（残置）
│   │   └── products/         # 商品画像
│   │       └── 51300/       # 商品ID 51300番台
│   │           ├── 51325/   # スナフキン時計
│   │           │   ├── pc/  # PC用画像
│   │           │   └── sp/  # SP用画像
│   │           └── 51347/   # ストリートファイター時計
│   │               ├── pc/  # PC用画像
│   │               └── sp/  # SP用画像
│   └── js/                   # JavaScriptファイル
│       └── product.js        # 商品ページ用JS
└── views/                     # HTMLビュー（Laravel移行時のBladeテンプレート候補）
    ├── categories/           # カテゴリページ
    │   └── moomin/
    │       └── index.html    # ムーミンカテゴリトップ
    └── products/             # 商品詳細ページ
        └── 51300/
            ├── 51325.html    # スナフキン時計詳細
            └── 51347.html    # ストリートファイター時計詳細
```

## B. iei_renewalからの移行内容

### 移行元 → 移行先の対応表

| 移行元（iei_renewal） | 移行先（ieir） | 備考 |
|---------------------|---------------|------|
| `/prgc_html/51325.html` | `/views/products/51300/51325.html` | 完全リニューアル |
| `/prgc_html/51347.html` | `/views/products/51300/51347.html` | 完全リニューアル |
| `/premico/goods_img/51325/` | `/public/img/products/51300/51325/` | 画像をpc/sp別に整理 |
| `/premico/goods_img/51347/` | `/public/img/products/51300/51347/` | 画像をpc/sp別に整理 |
| `/premico/streetfighter/cmn_img/` | `/public/img/products/51300/51347/` | 商品フォルダ内に統合 |
| `/moomin/cmn_img/green/` | `/public/img/products/51300/51325/` | 商品フォルダ内に統合 |
| `/moomin/index.html` | `/views/categories/moomin/index.html` | 新規作成 |

### 画像ファイルの整理ルール
- `pc_`で始まるファイル → `/pc/`フォルダへ
- `sp_`で始まるファイル → `/sp/`フォルダへ
- プレフィックスなし → 商品番号直下へ

## C. 主な変更点

### 技術スタックの変更
1. **CSS Framework**: 独自CSS → Tailwind CSS 3.4.1
2. **JavaScript**: jQuery依存 → Vanilla JavaScript
3. **レスポンシブ対応**: メディアクエリ → Tailwindのレスポンシブクラス（md:）
4. **アニメーション**: CSSトランジション → Tailwindクラス + カスタムJS

### UI/UXの改善
1. **ヘッダー**: モバイルファーストのハンバーガーメニュー実装
2. **ギャラリー**: サムネイルクリックで画像切り替え（product.js）
3. **スムーススクロール**: 購入ボタンから価格エリアへの滑らかな遷移
4. **レスポンシブ画像**: PC/SP別画像の自動切り替え

### HTML構造の最適化
1. **セマンティックHTML**: header, main, footer, section, navタグの適切な使用
2. **アクセシビリティ**: alt属性、aria-label、適切な見出し階層
3. **SEO対応**: meta description、は管理画面からの予定

### コンポーネント化について
- **現状**: HTMLやJavaScriptのコンポーネント化は行っていません
- **ファイル格納方針**: 商品詳細ページに関するファイル・画像は、変更することのないプログラムコードを基準に格納しています

## D. パスの注意点

### 重要：パスは全て絶対パスを使用
<img src="/public/img/products/51300/51325/pc/gallery_01_l.jpg">
<link rel="stylesheet" href="/public/css/customization.css">
<script src="/public/js/product.js"></script>


### Laravel移行時の想定パス
- 静的リソース: `/public/` → Laravelのpublicディレクトリ
- ビューファイル: `/views/` → `/resources/views/`（Bladeテンプレート化）

## E. その他の重要事項

### 1. 外部ライブラリ（CDN利用）
- **Tailwind CSS**: `https://cdn.tailwindcss.com/3.4.1`
- **Alpine.js**: `https://cdn.jsdelivr.net/npm/alpinejs@3.13.5/dist/cdn.min.js`
- **jQuery**: `https://code.jquery.com/jquery-3.7.1.min.js`（段階的廃止予定）

### 2. カスタムCSS（customization.css）
```css
/* カスタムユーティリティクラス */
.c-bg-premico { background-color: #4ECDC4; }
.c-bg-moomin-green { background-color: #6ab04c; }
.c-text-moomin-green { color: #6ab04c; }
.c-border-moomin-green { border-color: #6ab04c; }
.c-text-phone { color: #2c3e50; }
.c-bg-phone { background-color: #2c3e50; }
.c-text-xxs { font-size: 0.625rem; }
/* その他、プロジェクト固有のスタイル */
```

**注意**: 現在これらのカスタムクラスは`/public/css/customization.css`に定義しています。

### 3. JavaScript機能
- **ハンバーガーメニュー**: モバイル向けナビゲーション
- **ギャラリー機能**: サムネイルクリックで画像切り替え
- **スムーススクロール**: ページ内リンクのアニメーション
- **ページトップボタン**: スクロール位置に応じた表示制御

### 5. テスト済みブラウザ
- Chrome（最新版）
- モバイル（iOS Safari）

## 開発者向けメモ
- 画像の最適化（WebP対応、遅延読み込み）は本実装時に検討
- **重要**: 各ページは独立したHTMLファイルとして作成されており、コンポーネントの再利用は行っていません

---
最終更新: 2025/8/18