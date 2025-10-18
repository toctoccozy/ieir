## A. ディレクトリ構成

```
ieir/
├── package.json               # Node.js依存関係
├── tailwind.config.js         # Tailwind設定ファイル
├── public/                    # 静的リソース
│   ├── css/                  # スタイルシート
│   │   ├── customization.css # Tailwind用カスタムCSS（実装済み）
│   │   ├── base.css         # 空ファイル（将来用）
│   │   ├── cart.css         # 空ファイル（将来用）
│   │   ├── content.css      # 空ファイル（将来用）
│   │   ├── custom.css       # 空ファイル（将来用）
│   │   ├── style.css        # 空ファイル（将来用）
│   │   └── top.css          # 空ファイル（将来用）
│   ├── img/                  # 画像リソース
│   │   ├── category/       # カテゴリページ用画像
│   │   │   └── moomin/      # ムーミンカテゴリ画像
│   │   ├── parts/            # 共通パーツ画像
│   │   │   ├── icons/       # アイコン画像
│   │   │   ├── logo/        # 各種ロゴ画像
│   │   │   └── moomin/      # ムーミン共通画像
│   │   ├── products/         # 商品画像
│   │   │   └── 51300/       # 商品ID 51300番台
│   │   │       ├── 51325/   # スナフキン時計
│   │   │       │   ├── pc/  # PC用画像
│   │   │       │   └── sp/  # SP用画像
│   │   │       └── 51347/   # ストリートファイター時計
│   │   │           ├── pc/  # PC用画像
│   │   │           └── sp/  # SP用画像
│   │   ├── tmp_top_slider/   # トップページスライダー画像（仮）
│   │   ├── tmp_pickup/        # PickUp商品画像（仮）
│   │   ├── tmp_media/         # メディア掲載画像（仮）
│   │   └── top/              # トップページカテゴリ画像
│   └── js/                   # JavaScriptファイル
│       └── product.js        # 商品ページ用JS
└── views/                     # HTMLビュー（Laravel移行時のBladeテンプレート候補）
    ├── index.html            # トップページ
    ├── test_index/           # テスト用トップページ
    │   └── index.html
    ├── about/                # 空ディレクトリ（将来用）
    ├── admin/                # 空ディレクトリ（将来用）
    ├── auth/                 # 空ディレクトリ（将来用）
    ├── cart/                # 空ディレクトリ（将来用）
    ├── components/           # コンポーネント
    ├── contents/             # 空ディレクトリ（将来用）
    ├── category/           # カテゴリページ
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
| `/moomin/index.html` | `/views/category/moomin/index.html` | 新規作成 |
| （存在しなかった） | `/views/index.html` | トップページ新規作成 |
| （存在しなかった） | `/views/test_index/index.html` | テスト版トップページ |

### 新規作成コンテンツ
- **トップページ**: iei_renewalには存在しなかったトップページを新規開発
  - メインスライダー機能（Slick Carousel使用）
  - カテゴリー一覧セクション
  - PickUp商品セクション
  - メディア掲載情報セクション
- **仮画像素材**: 本実装までの暫定素材として配置
  - `/public/img/tmp_top_slider/` - スライダー用仮画像
  - `/public/img/tmp_pickup/` - PickUp商品用仮画像
  - `/public/img/tmp_media/` - メディア掲載用仮画像

### 画像ファイルの整理ルール
- `pc_`で始まるファイル → `/pc/`フォルダへ
- `sp_`で始まるファイル → `/sp/`フォルダへ
- プレフィックスなし → 商品番号直下へ
- `tmp_`で始まるディレクトリ → 仮配置（本実装時に差し替え予定）

## C. 主な変更点

### 技術スタックの変更
1. **CSS Framework**: 独自CSS → Tailwind CSS 3.4.1
2. **JavaScript**: jQuery依存 → Vanilla JavaScript（一部jQuery併用）
3. **レスポンシブ対応**: メディアクエリ → Tailwindのレスポンシブクラス（md:）
4. **アニメーション**: CSSトランジション → Tailwindクラス + カスタムJS
5. **スライダー**: Slick Carousel導入（トップページメインビジュアル）

### UI/UXの改善
1. **ヘッダー**: モバイルファーストのハンバーガーメニュー実装
2. **ギャラリー**: サムネイルクリックで画像切り替え（product.js）
3. **スムーススクロール**: 購入ボタンから価格エリアへの滑らかな遷移
4. **レスポンシブ画像**: PC/SP別画像の自動切り替え
5. **トップページスライダー**: メイン画像とサムネイル連動のスライダー実装
6. **グラデーション装飾**: ボーダーや背景にグラデーション効果を追加

### HTML構造の最適化
1. **セマンティックHTML**: header, main, footer, section, navタグの適切な使用
2. **アクセシビリティ**: alt属性、aria-label、適切な見出し階層
3. **SEO対応**: meta description、は管理画面からの予定

### カスタムCSSの拡張
customization.cssに以下のカスタムクラスを定義：
- **カラー定義**:
  - プレミコカラー: `c-bg-premico`、`c-text-premico`（#2C5282）
  - セカンドカラー: `c-bg-second`、`c-text-second`、`c-border-second`（#3e9aaf）
  - ムーミングリーン: `c-bg-moomin-green`、`c-text-moomin-green`、`c-border-moomin-green`（#4fa250）
  - 電話番号カラー: `c-text-phone`、`c-bg-phone`（#745424）
- **グラデーション背景**:
  - `c-bg-premico-gradient`: プレミコカラーのグラデーション
  - `c-bg-premico-gradient-2`: プレミコカラーの横方向グラデーション
  - `c-bg-second-gradient`: セカンドカラーのグラデーション
  - `c-bg-second-gradient-2`: セカンドカラーの横方向グラデーション
- **その他**: `c-text-xxs`（極小フォントサイズ）、`c-font-family-title`（タイトル用フォント）

### コンポーネント化について
- **現状**: HTMLやJavaScriptのコンポーネント化は行っていません
- **ファイル格納方針**: 商品詳細ページに関するファイル・画像は、変更することのないプログラムコードを基準に格納しています

## D. パスの注意点

### 重要：パスは全て絶対パスを使用
<img src="/public/img/products/51300/51325/pc/gallery_01_l.jpg">
<link rel="stylesheet" href="/public/css/customization.css">
<script src="/public/js/product.js"></script>

## E. その他の重要事項

### 1. 外部ライブラリ（CDN利用）
- **Tailwind CSS**: `https://cdn.tailwindcss.com/3.4.1`
- **Alpine.js**: `https://cdn.jsdelivr.net/npm/alpinejs@3.13.5/dist/cdn.min.js`
- **jQuery**: `https://code.jquery.com/jquery-3.7.1.min.js`（Slick Carousel用）
- **Slick Carousel**: `https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.min.js`
- **Slick CSS**: `https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css`
- **Google Fonts**: Noto Sans JP、Playfair Display

### 2. カスタムCSS（customization.css）の主要クラス例
```css
/* カスタムカラー定義 */
.c-bg-premico { background-color: #2C5282; }
.c-text-premico { color: #2C5282; }
.c-bg-second { background-color: #3e9aaf; }
.c-bg-moomin-green { background-color: #4fa250; }
.c-text-phone { color: #745424; }

/* グラデーション背景 */
.c-bg-premico-gradient {
  background: linear-gradient(135deg, #2C5282 0%, #3e6fa7 50%, #2C5282 100%);
}

/* フォント設定 */
.c-text-xxs { font-size: 0.6875rem; }
.c-font-family-title { font-family: 'Playfair Display', serif; }
```

**注意**: 現在これらのカスタムクラスは`/public/css/customization.css`に定義しています。

### 3. JavaScript機能
- **ハンバーガーメニュー**: モバイル向けナビゲーション
- **ギャラリー機能**: サムネイルクリックで画像切り替え
- **スムーススクロール**: ページ内リンクのアニメーション
- **ページトップボタン**: スクロール位置に応じた表示制御
- **Slickスライダー**: トップページのメインビジュアルとサムネイル連動

### 4. テスト済みブラウザ
- Chrome（最新版）
- モバイル（iOS Safari）


- `tmp_`プレフィックスのついたディレクトリ内の画像は暫定素材

---
最終更新: 2025/8/19



ーーー2025/10/
■管理画面のタイトルは整理ついたんでしたっけ

■ヘッダー
・ハンバーガーメニューのサイズを少し変更、下にメニューという文字を出した
・メニューのデザイン少し変更(ボタン色・線の長さ)
・上にスクロールしたときに隠れていたヘッダーが現れるようにした(トップページにしか適用していないので、全ページに適用する)


■トップページ
・ヘッダーに検索ボックスを追加
・スライダー下は視認性向上(特に年配の方向けのガイド充実)のため、検索ボックス・ダイレクト注文・広告掲載商品　を変更。
・検索ボックスは、５桁の商品番号、８ケタの商品番号、１１桁の申込み番号でも検索できるようになるか？
・スライダーの大きさを変更

■商品ページ
・商品タイトルの文字の上に「商品番号」を出した。5ケタ。

■カテゴリ　ー　キャラフィネ
・キャラフィネピックアップ→新着商品として、created_atで自動的に表示する。管理画面での変更は行わない。
・ヘッダーはmd以下(二段)とmd以上(一段)で分けた

■カテゴリ　ー　ムーミン系
・トップのイメージ画像がない場合は上下詰める
・ヘッダーはmd以下(二段)とmd以上(一段)で分けた
・カテゴリの並び替え機能は管理画面で必要
・

■カテゴリ　ー　ワンピースなど、プレミコ系のカテゴリ
・SEO対策という意味合いがあり、従来通り静的ページのままいきたいと(URLが変更になると困る)
・カテゴリページの追加・更新は従来通りデスティニーに依頼する
・

■広告掲載一覧
・contents/advertise　新設
・ページネーション設置

