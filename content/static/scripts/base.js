// Notify
(function($) {
    $.fn.notify = function(options){
        var settings = {
            type: 'alert',   // type should equal 'error', 'alert', 'loading', or 'success'
            message: '',
            timeOut: null,   // time to display, in ms
            effect: 'blind', // effect for jQuery show() method
            refresh: false
        }

        $.extend(settings, options);

        return this.each(function(){
            var $notify = $(this).find('.notify').first();

            clearTimeout($notify.data('notifyTimeoutId'));
            $notify.stop(true, true);
            $notify.removeClass('error loading alert success');
            $notify.html(settings.message).addClass(settings.type);

            //for some reason, using :hidden or :visible doesn't work here.
            //we have to directly look at the css display property
            if ($notify.is(':hidden')) {
                $notify.show(settings.effect);
            }

            if (settings.timeOut) {
                $notify.data('notifyTimeoutId', setTimeout(function() { 
                    $notify.hide(settings.effect); 
                    if (settings.refresh) window.location = document.URL;
                }, settings.timeOut));
            }
        });
    }
})(jQuery);

