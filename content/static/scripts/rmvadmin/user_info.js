$('#verify-toggle').click(function() {
    var verified = jsonVars['verified'] == 'True' ? true : false;
    var fb_id = jsonVars['fb_id'];
    var verify_str = verified ? 'unverify' : 'verify';
    if (confirm('Confirm Toggle User Verification\n\n' +
        'Are you sure you want to ' + verify_str + ' this user?'))
    {
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-HTTP-Method-Override', 'PUT');
            },
            type: 'POST',
            async: false,
            url: '/api/accounts/user/' + fb_id + '/',
            data: [
                { name: 'verified', value: !verified }
            ],
            contentType: 'application/json; charset=urf-8',
            error: function(err) { alert(err.responseText); },
            success: function(msg) { window.location = window.location.href; }
        });
    }
});
