$('#lightbox').click(function() { $('#lightbox').fadeOut(); });

$('#contact-submit').click(function() {
    var error_css = '2px inset #FF1D1D';
    var default_css = '1px inset #ccc';
    var name = $('#contact-name').val()
    var email = $('#contact-email').val()
    var comment = $('#contact-comment').val()
    var error = false;
    if (name == '')
    {
        $('#contact-name').css('border', error_css);
        error = true;
    }
    else $('#contact-name').css('border', default_css);
    if (email == '')
    {
        $('#contact-email').css('border', error_css);
        error = true;
    }
    else $('#contact-email').css('border', default_css);
    if (comment == '')
    {
        $('#contact-comment').css('border', error_css);
        error = true;
    }
    else $('#contact-comment').css('border', default_css);
    if (error) return;

    $.ajax({
        type: 'POST',
        async: false,
        url: '/info/comment/',
        data: [
            { name: 'name', value: name },
            { name: 'email', value: email },
            { name: 'comment', value: comment }
        ],
        contentType: 'application/json; charset=utf-8',
        error: function(err)
        {
            alert(err.responseText);
        },
        success: function(msg)
        {
            alert('Thank you for your input! We will get back to you as soon as we can.');
        }
    });
});