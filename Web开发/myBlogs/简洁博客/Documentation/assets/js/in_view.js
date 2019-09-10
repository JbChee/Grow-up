( function ( $ ) {

/*!
 * In Viewport.js v1.0
 *
 * Copyright 2018 shady.ro
 */

$.in_viewport = function( options ) {

    // default setup
    var defaults = {
        elements: {},
        loop: false,
    };

    // extend settings
    var settings = $.extend( {}, defaults, options );

    var windowHeight,
    documentHeight,
    percentsToTop;

    function init() {

        // init data
        windowHeight = $(window).height();
        documentHeight = $(document).height();

        // scanned elements
        var elements = {};

        var i = 0;
        $.each( settings.elements, function( k, f ) {
            $('body').find( k ).each( function() {
                elements[i] = {};
                elements[i]['element']      = $(this);
                elements[i]['height']       = $(this).height();
                elements[i]['position_top'] = $(this).offset().top;
                elements[i]['in_viewport']  = [elements[i]['position_top'] - windowHeight, elements[i]['position_top'] + elements[i]['height']];
                elements[i]['in_view_now']  = false,
                elements[i]['callback_in']  = f.callback_in;
                elements[i]['callback_out'] = f.callback_out;
                elements[i]['position_callback'] = f.position_callback;
                elements[i]['loop']         = 'loop' in f ? f.loop : settings.loop;
                i++;
            });
        });

        return elements;

    }

    var elements = init();

    $(window).resize( function() {
        elements = init();
    } );

    Number.prototype.between = function( x ) {
        var min = Math.min.apply( Math, x ),
        max = Math.max.apply( Math, x );
        return this > min && this < max;
    };

    $(window).scroll( function() {

        var pixelsToTop = $(window).scrollTop();

        if( Object.keys( elements ).length > 0 ) {

            $.each( elements, function( k, e ) {
                var in_view_now = pixelsToTop.between( e.in_viewport );
                var has_out_callback = $.isFunction( e.callback_out );
                // check if in viewport now
                if( in_view_now ) {
                    if( e.loop && $.isFunction( e.position_callback ) ) {
                        var elementToTop = pixelsToTop - e.position_top;
                        e.position_callback.call( e.element, elementToTop );
                    }
                    if( !e.in_view_now ) {
                        if( $.isFunction( e.callback_in ) ) {
                            elements[k]['in_view_now'] = true;
                            e.callback_in.call( e.element );
                            if( !has_out_callback && !e.loop ) {
                                delete elements[k];
                            }
                        }
                    }
                // check if no longer in viewport
                } else if( !in_view_now && e.in_view_now ) {
                    elements[k]['in_view_now'] = false;
                    if( has_out_callback ) {
                        e.callback_out.call( e.element );
                        if( !e.loop ) {
                            delete elements[k];
                        }
                    }
                }
           } );

        }

        if( $.isFunction( settings.position ) ) {
            percentsToTop = parseInt( pixelsToTop / ( documentHeight - windowHeight ) * 100 );
            settings.position.call( this, percentsToTop );
        }

        if( $.isFunction( settings.position_px ) ) {
            settings.position_px.call( this, pixelsToTop );
        }

    }).scroll();

};

}( jQuery ));