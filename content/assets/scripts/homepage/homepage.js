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
    FB.login(function(response) {
        if (response.authResponse) {
            console.log('woooo');
        } else {
            singnup_notify('error', 
                'Please authorize the Facebook app to send an invite request.', false);
        }
    }, {scope: 'email,user_birthday,user_location,read_stream'});

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

    FB.login(function(response) {
        if (response.authResponse) {
            sendInviteRequest(response.id);
        } else {
            singnup_notify('error', 
                'Please authorize the Facebook app to send an invite request.', false);
        }
    }, {scope: 'email,user_birthday,user_location,read_stream'});
}

function sendInviteRequest(fb_id)
{
     $.ajax({
        type: 'POST',
        async: true,
        url: '/api/accounts/request/invite/',
        data: [
            { name: 'fb_id', value: fb_id },
            { name: 'name', value: real_name },
            { name: 'email', value: email },
            { name: 'description', value: desc }
        ],
        contentType: 'application/json; charset=utf-8',
        success: function(result) { signup_notify('success', 'Thank you for your interest in Rate My Video!', false); },
        error: function(error) { signup_notify('error', error.responseText, false); }
    });
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
