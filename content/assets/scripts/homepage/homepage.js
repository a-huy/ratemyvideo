$(document).ready(function() {
    $('#invite_submit_button').click(function() { 
        onSubmitInviteRequest();
    });
});

function onSubmitInviteRequest()
{
    var real_name = $('#full_name_input').val();
    var email = $('#email_input').val();
    console.log('real name = ' + real_name);
    if (real_name == '') {
        signup_notify('error', 'Please provide a name', false);
        return;
    }
    if (email == '') {
        signup_notify('error', 'Please provide an email', false);
        return;
    }

    $.ajax({
        type: 'POST',
        async: true,
        url: '/api/accounts/request/invite/',
        data: [
            { name: 'name', value: real_name },
            { name: 'email', value: email }
        ],
        contentType: 'application/json; charset=utf-8',
        success: function(result) { signup_notify('success', 'Thank you for your interest in Rate My Video!', false); },
        error: function(error) { signup_notify('error', error.responseText, false); }
    });

    signup_notify('success', 'Thank you for your interest in Rate My Video!', false);
}

function signup_notify(type, msg, refresh)
{
    $("#signup").notify({
            type: type,
            message: msg,
            timeOut: 5000,
            refresh: refresh
    });
}
