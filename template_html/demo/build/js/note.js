(function($) {
    
    $(document).ready(function() {

    'use strict';

    // Return to Mail-list
    // when click .return-mail-list > a
    $('.return-note-list').click(function(e) {
        e.preventDefault();
        $('.Note-aside').removeClass('Note-aside--slideleft');
    });

    if ($(window).width() <= 767) {
        $('.Note-list').on('click', '.Note', function(e){
            e.preventDefault();
            $('.Note-aside').addClass('Note-aside--slideleft');
        });
    };


    $(window).resize(function() {
        if ($(window).width() <= 767) {
            $('.Note-list').on('click', '.Note', function(e){
                e.preventDefault();
                $('.Note-aside').addClass('Note-aside--slideleft');
            });
        } else {
            $('.Note-aside').removeClass('Note-aside--slideleft');
            $('.Note-list').on('click', '.Note', function(e){
                e.preventDefault();
                $('.Note-aside').removeClass('Note-aside--slideleft');
            });
        }
    });

});

})(window.jQuery);
