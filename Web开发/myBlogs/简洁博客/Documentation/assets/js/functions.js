$(document).ready(function () {
    "use strict";
    // Smooth scrolling using jQuery easing
    $('[data-go-to]:not([href="#"])').on("click", function () {
        var target = $('#' + $(this).data('go-to'));
        if( target.length ){
            $('html, body').animate({
                scrollTop: (target.offset().top - 10)
            }, 1000 );
        }
    });

    jQuery.in_viewport( {
        loop: true,
        elements: {

            '[data-in-view]': {
                'callback_in': function() {
                    $('.nav-menu').find('[data-go-to="' + $(this).attr('id') + '"]').addClass('active');
                },
                'callback_out': function() {
                    $('.nav-menu').find('[data-go-to="' + $(this).attr('id') + '"]').removeClass('active');
                },
                'loop': true
            }

        }
    });

});

(function() {
    var pre = document.getElementsByTagName('pre'),
        pl = pre.length;
    for (var i = 0; i < pl; i++) {
        pre[i].innerHTML = '<span class="line-number"></span>' + pre[i].innerHTML + '<span class="cl"></span>';
        var num = pre[i].innerHTML.split(/\n/).length;
        for (var j = 0; j < num; j++) {
            var line_num = pre[i].getElementsByTagName('span')[0];
            line_num.innerHTML += '<span>' + (j + 1) + '</span>';
        }
    }
})();