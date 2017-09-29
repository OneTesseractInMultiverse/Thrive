(function($) {

    'use strict';

    $(document).ready(function() {

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
