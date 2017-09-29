(function($) {

    $(document).ready(function() {

        'use strict';

        // Toggle Mail-nav
        // When click #toggle-mailbox-nav > .btn
        $('#toggle-mailbox-nav').click(function(e) {
            e.stopPropagation();
            $('.Mailbox-nav-aside').toggle();
        });

        // Return to Mail-list
        // when click .return-mail-list > a
        $('#return-mailbox-list > a').click(function(e) {
            e.preventDefault();
            $('.Mailbox-list').removeClass('Mailbox-list--slideLeft');
        });

        if ($(window).width() <= 767) {
            $('.Mail > a').click(function(e) {
                e.preventDefault();
                $('.Mailbox-list').addClass('Mailbox-list--slideLeft');
                $('.Mailbox-nav-aside').hide();
            });
        };
        $(window).resize(function() {
            if ($(window).width() <= 767) {
                $('.Mailbox-nav-aside').hide();
                $('.Mail > a').click(function(e) {
                    e.preventDefault();
                    $('.Mailbox-list').addClass('Mailbox-list--slideLeft');
                    $('.Mailbox-nav-aside').hide();
                });
            } else {
                $('.Mailbox-list').removeClass('Mailbox-list--slideLeft');
                $('.Mailbox-nav-aside').show();
                $('.Mail > a').click(function(e) {
                    $('.Mailbox-list').removeClass('Mailbox-list--slideLeft');
                    $('.Mailbox-nav-aside').show();
                });
            }
        });

        if ($(window).width() <= 1200) {
            $('.Mail > a').click(function(e) {
                e.preventDefault();
                $('.Mailbox-list').addClass('Mailbox-list--slideLeft');
            });
        };
        $(window).resize(function() {
            if ($(window).width() <= 1200) {
                $('.Mail > a').click(function(e) {
                    e.preventDefault();
                    $('.Mailbox-list').addClass('Mailbox-list--slideLeft');
                });
            } else {
                $('.Mailbox-list').removeClass('Mailbox-list--slideLeft');
                $('.Mail > a').click(function(e) {
                    $('.Mailbox-list').removeClass('Mailbox-list--slideLeft');
                });
            }
        });

    });

})(window.jQuery);
