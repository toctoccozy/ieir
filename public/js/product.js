// Product page specific JavaScript functionality for I･E･I project

$(document).ready(function() {
    // Gallery thumbnail click with fade effect
    $('.photo-area img').click(function() {
        var thumbnailSrc = $(this).attr('src');
        // SPサムネイルからPCの大画像パスに変換
        var largeSrc = thumbnailSrc.replace('/sp/gallery_', '/pc/gallery_').replace('.jpg', '_l.jpg');
        var $mainImage = $('#main-gallery-image');
        
        // Fade out, change image, fade in
        $mainImage.fadeOut(200, function() {
            $(this).attr('src', largeSrc).fadeIn(300);
        });
        
        // Update active thumbnail
        $('.photo-area img').removeClass('ring-4 ring-moomin');
        $(this).addClass('ring-4 ring-moomin');
    });
    
    // Image zoom on click
    $('#main-gallery-image').click(function() {
        var currentSrc = $(this).attr('src');
        
        // Create modal overlay
        var modal = $(`
            <div class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4" id="image-modal">
                <div class="relative max-w-4xl max-h-full">
                    <img src="${currentSrc}" class="max-w-full max-h-full object-contain rounded-lg">
                    <button class="absolute top-4 right-4 text-white text-3xl hover:text-gray-300 transition-colors" onclick="$('#image-modal').fadeOut(300, function() { $(this).remove(); })">&times;</button>
                </div>
            </div>
        `);
        
        $('body').append(modal);
        modal.hide().fadeIn(300);
        
        // Close on background click
        modal.click(function(e) {
            if (e.target === this) {
                $(this).fadeOut(300, function() { $(this).remove(); });
            }
        });
    });
});

// Cart function (enhanced mock)
function cart() {
    // フォームバリデーション
    const sizeSelect = $('select[name="m5siz"]').val();
    if (!sizeSelect || sizeSelect === '▼お選びください。') {
        // エラー表示
        const errorDiv = $(`
            <div class="notification error">
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    サイズを選択してください
                </div>
            </div>
        `);
        
        $('body').append(errorDiv);
        errorDiv.hide().fadeIn(300);
        
        // サイズ選択にフォーカス
        $('select[name="m5siz"]').focus().addClass('ring-2 ring-red-500');
        
        setTimeout(() => {
            errorDiv.fadeOut(300, function() { $(this).remove(); });
            $('select[name="m5siz"]').removeClass('ring-2 ring-red-500');
        }, 3000);
        
        return false;
    }
    
    // ローディング表示
    const loadingDiv = $(`
        <div class="notification info">
            <div class="flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                カートに追加中...
            </div>
        </div>
    `);
    
    $('body').append(loadingDiv);
    
    // カートデータをローカルストレージに保存
    setTimeout(() => {
        const cartItem = {
            id: '51325',
            name: 'MOOMIN セイコー スナフキン 釣り人の時間',
            price: 43780,
            size: sizeSelect,
            image: '../../../../../iei/ieir/public/img/products/51300/51325/pc/gallery_01_l.jpg',
            timestamp: new Date().toISOString()
        };
        
        let cart = JSON.parse(localStorage.getItem('iei_cart') || '[]');
        cart.push(cartItem);
        localStorage.setItem('iei_cart', JSON.stringify(cart));
        
        loadingDiv.remove();
        
        // 成功メッセージ
        const successDiv = $(`
            <div class="notification success">
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                    商品をカートに追加しました (${sizeSelect})
                </div>
                <div class="mt-2 text-sm">
                    <a href="#" class="underline hover:no-underline">カートを見る</a>
                </div>
            </div>
        `);
        
        $('body').append(successDiv);
        successDiv.hide().fadeIn(300);
        
        setTimeout(() => {
            successDiv.fadeOut(300, function() { $(this).remove(); });
        }, 4000);
        
    }, 1500); // 1.5秒のローディング時間
    
    return false;
}

