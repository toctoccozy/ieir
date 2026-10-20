
<!doctype html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Charaffine：{{ $iei_category_jp_name }}｜インペリアル・エンタープライズ株式会社 I･E･I</title>
    <meta name="description" content="xxxxxxxx">
    <meta name="keywords" content="xxxxxxxx">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com/3.4.1"></script>
    <!-- Custom CSS -->
    <link rel="stylesheet" href="/css/customization.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Zen+Maru+Gothic:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.5/dist/cdn.min.js"></script>

</head>

<body class="bg-white">
    <div class="min-h-screen mx-auto">
        <?php
            $headerPath = public_path('/include/header_kitty.html');
            include is_file($headerPath) ? $headerPath : public_path('/include/header_new.html');
        ?>

        <div class="main-content">
        <!-- パンくずナビ -->
        <nav class="bread-clumbs text-gray-600 mx-auto pl-3 leading-snug tracking-tighter max-w-6xl">
            <a href="/charaffine/" class="text-blue-800 hover:text-blue-400 transition-colors">キャラフィネ</a>
            <span class="mx-2">｜</span>
            キティ
        </nav>

        <main class="py-8 px-1 mx-auto max-w-5xl">
            <!-- 商品カテゴリセクション -->
            <!-- <section class="mb-8 px-2 sm:px-4">
                <h2 class="text-center text-2xl md:text-3xl font-bold text-gray-800 mb-6">
                    <span class="inline-block border-b-4 c-border-kitty pb-2 c-font-family-charaffine">{{ $iei_category_jp_name }} グッズ一覧</span>
                </h2>
            </section> -->

            <section>
                <h2 class="mb-6 flex items-center overflow-hidden px-4">
                    <div class="flex flex-col md:flex-row md:items-center flex-shrink-0">
                        <span class="text-4xl py-2 font-bold text-gray-800 c-font-family-title md:text-5xl whitespace-nowrap">KITTY</span>
                        <span class="text-xs c-text-xxs font-normal text-gray-600 ml-4 md:ml-3">キティ グッズ一覧</span>
                    </div>
                    <!-- 装飾ライン -->
                    <div class="flex flex-1 items-center ml-4 min-w-0">
                        <svg class="flex-1 h-1.5 min-w-0" viewBox="0 0 300 6" preserveAspectRatio="none">
                            <!-- 濃いライン（台形） -->
                            <polygon points="4,0 104,0 100,6 0,6" fill="#d65db1"/>
                            <!-- 中間ライン（台形） -->
                            <polygon points="104,0 204,0 200,6 100,6" fill="#d65db1" fill-opacity="0.5"/>
                            <!-- 薄いライン（台形） -->
                            <polygon points="204,0 300,0 296,6 200,6" fill="#d65db1" fill-opacity="0.25"/>
                        </svg>
                    </div>
                </h2>
                <div class="relative bg-white flex items-center justify-center my-5 mx-3 md:mx-10 border rounded-lg border-gray-300">
                    <div class="absolute -top-1.5 left-4 z-10">
                        <svg width="72" height="12" viewBox="0 0 72 12">
                            <polygon points="6,0 18,0 12,12 0,12" fill="#2C5282"/>
                            <polygon points="26,0 38,0 32,12 20,12" fill="#2C5282"/>
                            <polygon points="46,0 58,0 52,12 40,12" fill="#2C5282"/>
                        </svg>
                    </div>
                    <div class="mt-1 ml-2 flex-col items-center p-1 md:px-8">
                        <img class="h-auto w-16 max-w-48" src="/img/parts/logo/logo_iei.jpg" alt="I･E･I">
                    </div>
                    <p class="text-base text-gray-700 leading-tight p-4">
                        ようこそハローキティコレクションへ！<br>ハローキティを愛する大人のために、I・E・Iが心を込めて企画したオリジナル限定品をご紹介します。ごゆっくりお楽しみください。
                    </p>
                </div>
            </section>

            <!-- 商品リストエリア -->
            <section class="px-2 sm:px-4">
                <!-- 件数表示 -->
                <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-6">
                    <!-- 件数表示 -->
                    @if (count($goods_list) > 0)
                        <div class="text-right">
                            <p class="text-sm sm:text-base text-gray-600">全{{ $goods_list->total() }}件を表示</p>
                        </div>
                    @endif
                </div>

                @if (count($goods_list) > 0)
                <ul class="space-y-4">
                    @foreach ($goods_list as $goods)
                    <li class="overflow-hidden duration-200 border c-border-kitty rounded-md p-4">
                        <div class="flex flex-col md:flex-row">
                            <div class="md:w-[40%] max-w-sm h-auto mx-auto p-4">
                                <!-- LPの価格の横の画像? -->
                                <img src="{{ $goods->getImagePathSoro('main_image') }}"
                                    alt="{{ $goods->getConnectTitleList() }}"
                                    class="w-full h-auto mx-auto"
                                    fetchpriority="high">
                            </div>
                            <div class="md:w-[60%] p-2">
                                <dl>
                                    <dt class="text-lg font-bold text-gray-800 mb-3 md:text-xl">
                                        {{ $goods->getConnectTitleList() }}
                                    </dt>
                                    <dd class="text-gray-600 leading-relaxed">
                                        {{ $goods->getIeiCategoryComment() }}
                                    </dd>
                                </dl>
                                <div class="flex justify-center my-6">
                                    <a href="/{{ $goods->getM1prgc() }}"
                                    class="inline-block c-font-family-charaffine c-bg-kitty hover:opacity-50 text-lg sm:text-xl text-white px-12 py-2 rounded-full transition-colors duration-200 font-medium">
                                        詳細はこちら
                                    </a>
                                </div>
                            </div>
                        </div>
                    </li>
                    @endforeach
                </ul>
                @else
                    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-6">
                        <div class="px-4 w-full sm:w-1/2">
                            <label for="product-type-select" class="block font-bold text-gray-700 mb-2">該当データはありません。</label>
                        </div>
                    </div>
                @endif
            </section>
        </main>

        <!-- ページトップボタン -->
        <div id="pagetop" class="fixed bottom-6 right-6 z-50 hidden">
            <a href="#" class="c-bg-second hover:bg-opacity-80 rounded-full p-3 shadow-lg transition-all duration-200 transform  hover:scale-110 text-white font-bold text-lg w-12 h-12 flex items-center justify-center">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                </svg>
            </a>
        </div>
    </div>

    <!-- フッターコンポーネント -->
    <?php include public_path() . '/include/footer_new.html'; ?>

    <!-- JavaScript -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="/js/product.js"></script>
    <script src="/js/common.js"></script>
</body>
</html>
