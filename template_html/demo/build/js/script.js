(function($) {

    'use strict';

    $(document).ready(function() {

        $('[data-toggle="tooltip"]').tooltip();
        $('[data-toggle="popover"]').popover();

        // collapsible panel
        $('.panel .tools .collapse-box').click(function () {
            var el = $(this).parents(".panel").children(".panel-body");
            if ($(this).hasClass("fa-chevron-down")) {
                $(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
                el.slideUp(200);
            } else {
                $(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
                el.slideDown(200); }
        });

        // close panel
        $('.panel .tools .close-box').click(function () {
            $(this).parents(".panel").parent().remove();
        });

        // refresh panel

        $('.refresh-box').on('click', function(br) {
            br.preventDefault();
            $("<div class='refresh-block'><span class='refresh-loader'><i class='fa fa-spinner fa-spin'></i></span></div>").appendTo($(this).parents('.tools').parents('.panel-heading').parents('.panel'));

            setTimeout(function() {
                $('.refresh-block').remove();
            }, 1000);

        });

        // Auto size textarea
        autosize($('.autosize'));

        // searchCollapse
        $('.search-collapse').each(function() {
            var $searchInput = $('.form-control'),
            $searchBtn = $('.btn-search-collapse');

            $searchBtn.click(function(e) {
                e.preventDefault();
                $searchInput.toggleClass('form-control-open').focus();
            });

        });

        // niceScroll
        $(".niceScroll").niceScroll({
            cursorcolor : "#000000",
            cursoropacitymax : 0.3,
            cursorwidth : "8px",
            cursorborder : "2px solid transparent",
            cursordragontouch : true, // drag cursor in touch / touchbehavior mode also
            zindex : "10", // change z-index for scrollbar div
            cursorborderradius: "10px",
        });

    });

})(window.jQuery);
