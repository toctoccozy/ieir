// Common JavaScript functionality for I･E･I project

$(document).ready(function() {
    // ヘッダーコンポーネントの初期化
    // モバイルメニュートグル
    $('#mobile-menu-button').click(function() {
        $('#mobile-menu').toggleClass('hidden');
        $(this).find('svg').toggleClass('rotate-180');
    });
    
    // カート数量の更新
    function updateCartCount() {
        const cart = JSON.parse(localStorage.getItem('iei_cart') || '[]');
        const count = cart.length;
        const $cartCount = $('#cart-count');
        
        if (count > 0) {
            $cartCount.text(count).removeClass('hidden');
        } else {
            $cartCount.addClass('hidden');
        }
    }
    
    // 初期カート数量表示
    updateCartCount();
    
    // ローカルストレージの変更を監視
    $(window).on('storage', updateCartCount);
    
    
    // Pagetop button
    var pagetop = $('#pagetop');
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            pagetop.fadeIn();
        } else {
            pagetop.fadeOut();
        }
    });
    pagetop.click(function () {
        $('body, html').animate({ scrollTop: 0 }, 500);
        return false;
    });
    
    // Smooth scroll for anchor links
    $('a[href^="#"]').click(function(e) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 20 // 20px offset for better visibility
            }, 800); // 800ms smooth scroll
        }
    });
    
    // フッターコンポーネントの初期化
    // ニュースレター登録フォーム
    $('footer form').submit(function(e) {
        e.preventDefault();
        
        const email = $(this).find('input[type="email"]').val();
        if (!email) {
            alert('メールアドレスを入力してください');
            return;
        }
        
        // メールアドレス形式チェック
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('正しいメールアドレスを入力してください');
            return;
        }
        
        // 成功メッセージ表示
        const successDiv = $(`
            <div class="notification success">
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                    メールニュースの登録が完了しました
                </div>
            </div>
        `);
        
        $('body').append(successDiv);
        successDiv.hide().fadeIn(300);
        
        setTimeout(() => {
            successDiv.fadeOut(300, function() { $(this).remove(); });
        }, 3000);
        
        // フォームリセット
        $(this).find('input[type="email"]').val('');
    });
});