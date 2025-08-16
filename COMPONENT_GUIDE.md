# コンポーネント設計書

## 📦 コンポーネント一覧

### 1. ヘッダーコンポーネント (`components/header.html`)

#### 🎯 用途
全ページ共通のヘッダー部分。ナビゲーション、検索、カート機能を提供。

#### 🔧 機能
- **レスポンシブナビゲーション**: デスクトップとモバイルで表示切り替え
- **ドロップダウンメニュー**: キャラフィネカテゴリの子メニュー
- **検索機能**: キーワード・商品番号検索
- **カート表示**: リアルタイム数量更新
- **固定ヘッダー**: スクロール時に上部固定
- **お知らせバー**: 電話番号などの重要情報

#### 📱 レスポンシブ対応
```css
/* デスクトップ（md以上） */
.hidden.md:block     /* ナビゲーション表示 */
.md:flex             /* フレックスレイアウト */

/* モバイル（md未満） */
.md:hidden           /* ハンバーガーメニュー表示 */
#mobile-menu         /* モバイル専用メニュー */
```

#### 🎨 使用カラー
- `bg-iei-primary`: メインボタン
- `bg-iei-secondary`: お知らせバー
- `text-moomin`: ホバー色

#### 💾 データ連携
```javascript
// カート数量の更新
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('iei_cart') || '[]');
    $('#cart-count').text(cart.length);
}
```

---

### 2. フッターコンポーネント (`components/footer.html`)

#### 🎯 用途
全ページ共通のフッター部分。企業情報、リンク集、SNS連携を提供。

#### 🔧 機能
- **4カラムレイアウト**: 会社情報、カテゴリ、サポート、SNS
- **SNSアイコン**: Twitter、Facebook、Instagram、Pinterest
- **ニュースレター登録**: メールアドレス収集
- **法的情報**: 利用規約、プライバシーポリシー等
- **認証マーク**: SSL、JMA認証表示

#### 📱 レスポンシブ対応
```css
/* デスクトップ */
.grid.lg:grid-cols-4  /* 4カラム */

/* タブレット */
.md:grid-cols-2       /* 2カラム */

/* モバイル */
.grid-cols-1          /* 1カラム */
```

#### 📧 ニュースレター機能
```javascript
// バリデーション付きメール登録
$('footer form').submit(function(e) {
    const email = $(this).find('input[type="email"]').val();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // 処理...
});
```

---

### 3. コンポーネントローダー (`public/js/components/component-loader.js`)

#### 🎯 用途
HTMLコンポーネントの動的読み込みシステム。Laravel移行を見据えたコンポーネント化。

#### 🔧 主要機能

##### ✨ 基本的な読み込み
```javascript
// 単体読み込み
componentLoader.load('header', '#header-container');

// 複数同時読み込み
componentLoader.loadMultiple([
    {name: 'header', target: '#header-container'},
    {name: 'footer', target: '#footer-container'}
]);
```

##### 💾 キャッシュシステム
```javascript
// キャッシュ有効（デフォルト）
componentLoader.load('header', '#header', true);

// キャッシュ無効
componentLoader.load('header', '#header', false);

// キャッシュクリア
componentLoader.clearCache('header');
```

##### 🚀 プリロード機能
```javascript
// 事前読み込みでパフォーマンス向上
componentLoader.preload(['header', 'footer']);
```

##### 🤖 自動読み込み
```html
<!-- data-component属性で自動読み込み -->
<div id="header-container" data-component="header">
    読み込み中...
</div>
```

#### 🛠 エラーハンドリング
```javascript
// ロードエラー時のフォールバック表示
catch (error) {
    targetElement.innerHTML = `
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p>コンポーネントの読み込みに失敗: ${componentName}</p>
        </div>
    `;
}
```

#### 📋 Laravel移行対応
```javascript
// jQuery拡張
$.fn.loadComponent = function(componentName) {
    return componentLoader.load(componentName, this);
};

// ES6モジュール対応
export default ComponentLoader;
```

---

## 🎨 デザインパターン

### カードコンポーネント
```html
<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
    <div class="p-6">
        <!-- カード内容 -->
    </div>
</div>
```

### ボタンパターン
```html
<!-- プライマリボタン -->
<button class="bg-iei-primary hover:bg-iei-secondary text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200">

<!-- セカンダリボタン -->  
<button class="border-2 border-iei-primary text-iei-primary hover:bg-iei-primary hover:text-white px-6 py-3 rounded-lg font-medium transition-all duration-200">
```

### 入力フォーム
```html
<input class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-iei-primary focus:border-transparent transition-all duration-200">
```

---

## 🔧 カスタマイズガイド

### 新しいコンポーネントの作成

#### Step 1: HTMLファイル作成
```html
<!-- views/components/new-component.html -->
<div class="new-component">
    <!-- コンポーネント内容 -->
    <script>
        // コンポーネント固有のスクリプト
    </script>
</div>
```

#### Step 2: 読み込み
```javascript
componentLoader.load('new-component', '#target-element');
```

#### Step 3: スタイル適用
```html
<style>
.new-component {
    /* カスタムスタイル */
}
</style>
```

### 既存コンポーネントの拡張

#### ヘッダーのカスタマイズ例
```javascript
// ヘッダー読み込み後にカスタマイズ
componentLoader.load('header', '#header').then(() => {
    // 追加機能の実装
    $('#header').addClass('custom-class');
});
```

---

## 🧪 テスト方法

### 単体テスト
```javascript
// コンポーネントローダーのテスト例
test('コンポーネント読み込み', async () => {
    await componentLoader.load('header', '#test-container');
    expect($('#test-container').html()).toContain('header');
});
```

### 統合テスト
```javascript
// 複数コンポーネントの連携テスト
test('ヘッダー・フッター連携', async () => {
    await componentLoader.loadMultiple([
        {name: 'header', target: '#header'},
        {name: 'footer', target: '#footer'}
    ]);
    // 連携動作の確認
});
```

### パフォーマンステスト
```javascript
// 読み込み速度測定
console.time('component-load');
await componentLoader.load('header', '#header');
console.timeEnd('component-load');
```

---

## 📋 Laravel移行チェックリスト

### Bladeテンプレート化
- [ ] `.html` → `.blade.php` 変更
- [ ] コメント形式の include を Blade ディレクティブに変更
- [ ] データバインディングの実装

### ルーティング
- [ ] コンポーネント用ルートの設定
- [ ] APIエンドポイントの実装

### アセット管理
- [ ] Laravel Mix/Vite設定
- [ ] CSS/JSのビルドプロセス
- [ ] 画像最適化

### パフォーマンス
- [ ] コンポーネントキャッシュ
- [ ] レスポンシブ画像
- [ ]遅延読み込み

---

**更新日**: 2024年1月14日  
**バージョン**: 1.0.0  
**メンテナ**: I･E･I 開発チーム