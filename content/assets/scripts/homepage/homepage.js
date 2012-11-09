(function(doc) {
    var js, id = 'facebook-jssdk', ref = doc.getElementsByTagName('script')[0];
    if (doc.getElementById(id)) {return;}
    js = doc.createElement('script'); js.id = id; js.async = true;
    js.src = '//connect.facebook.net/en_US/all.js';
    ref.parentNode.insertBefore(js, ref);
}(document));

window.fbAsyncInit = function() {
    FB.init({
        appId      : '397851696951181', // App ID
        channelUrl : 'http://warm-ocean-6030.herokuapp.com/login/channel/', // Channel File
        status     : true, // check login status
        cookie     : true, // enable cookies to allow the server to access the session
        xfbml      : true  // parse XFBML
    });
};

$(document).ready(function() {
    $('#invite_submit_button').click(function() { 
        onSubmitInviteRequest();
    });
});

function onSubmitInviteRequest()
{
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            // connected
            console.log('You are logged in!');
        } else if (response.status === 'not_authorized') {
            // not_authorized
            console.log('You are not authorized');
        } else {
            // not_logged_in
            console.log('You are not logged in');
        }
    });
    return;

    var real_name = $('#full_name_input').val();
    var email = $('#email_input').val();
    var desc = $('#desc_input').val();
    if (real_name == '') {
        signup_notify('error', 'Please provide a name.', false);
        return;
    }
    if (email == '') {
        signup_notify('error', 'Please provide an email.', false);
        return;
    }
    if (desc == '') {
        signup_notify('error', 'Please tell us how you heard about Rate My Video.', false);
        return;
    }

    $.ajax({
        type: 'POST',
        async: true,
        url: '/api/accounts/request/invite/',
        data: [
            { name: 'name', value: real_name },
            { name: 'email', value: email },
            { name: 'description', value: desc }
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
