// Product page specific JavaScript functionality for I･E･I project

$(function() {
    // Gallery thumbnail click with fade effect
    $('.photo-area img').on('click', function() {
        var largeSrc = $(this).attr('src');
        var $mainImage = $('#main-gallery-image');
        
        // Fade out, change image, fade in
        $mainImage.fadeOut(200, function() {
            $(this).attr('src', largeSrc).fadeIn(300);
        });
        
        // Update active thumbnail
        $('.photo-area img').removeClass('ring-4');
        $(this).addClass('ring-4');
    });
    
    // Image zoom on click
    $('#main-gallery-image').on('click', function() {
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
        modal.on('click', function(e) {
            if (e.target === this) {
                $(this).fadeOut(300, function() { $(this).remove(); });
            }
        });
    });
});
