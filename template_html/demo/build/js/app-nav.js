+function ($) {

    'use strict';

    $(function(){

        $('[data-toggle="ui-nav"]').on('click', function(e){
            e.preventDefault();
            $('#ui').toggleClass('ui-aside-compact');
        });

        $('[data-toggle="ui-aside-right"]').on('click', function(e){
            e.preventDefault();
            $('#content').toggleClass('ui-content-compact');
        });

        $('[ui-nav]').on('click', 'a', function(e) {

            // locate href
            // if there is no submenu
            var href = $(this).attr('href');
            if(href){
                window.location.href = href;
            }

            // Open submenu
            var $this = $(e.target), $active;
            $this.is('a') || ($this = $this.closest('a'));

            $active = $this.parent().siblings( ".active" );
            $active && $active.toggleClass('active').find('> ul:visible').stop().slideUp(200);

            ($this.parent().hasClass('active') && $this.next().stop().slideUp(200)) || $this.next().stop().slideDown(200);
            $this.parent().toggleClass('active');

            $this.next().is('ul') && e.preventDefault();
        });

        if($('#ui').hasClass('ui-aside-compact')) {
            var uiHasCompact = true;
        }
        if($('#content').hasClass('ui-content-compact')) {
            var uiContentHasCompact = true;
        }

        function doneResizing() {
            if (Modernizr.mq('screen and (min-width:768px)')) {
                // action for screen widths including and above 768 pixels

                if(uiHasCompact === true) {
                    $('#ui').addClass('ui-aside-compact')
                }
                if(uiContentHasCompact === true) {
                    $('#content').addClass('ui-content-compact')
                }

            } else if (Modernizr.mq('screen and (max-width:767px)')) {
                // action for screen widths below 768 pixels
                // console.log('Moblie');

                if(uiHasCompact === true) {
                    $('#ui').removeClass('ui-aside-compact')
                }
                if(uiContentHasCompact === true) {
                    $('#content').removeClass('ui-content-compact')
                }

                $('[data-toggle="ui-nav"]').on('click', function(e){
                    e.preventDefault();

                    var hasAsideCompact = $('#ui').hasClass('ui-aside-compact'),
                    hasContentCompact = $('#content').hasClass('ui-content-compact');

                    if(hasAsideCompact) {
                        if(hasContentCompact) {
                            $('#content').removeClass('ui-content-compact');
                        }
                    }

                });

                $('[data-toggle="ui-aside-right"]').on('click', function(e){
                    e.preventDefault();

                    var hasAsideCompact = $('#ui').hasClass('ui-aside-compact'),
                    hasContentCompact = $('#content').hasClass('ui-content-compact');

                    if(hasContentCompact) {
                        if(hasAsideCompact) {
                            $('#ui').removeClass('ui-aside-compact');
                        }
                    }
                });
            }
        }

        var id;
        $(window).resize(function () {
            clearTimeout(id);
            id = setTimeout(doneResizing, 0);
        });

        doneResizing();

    });
    
}(jQuery);
