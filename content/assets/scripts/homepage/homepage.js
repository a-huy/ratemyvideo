var APP_ID = '397851696951181';
var RED_URL = 'http://warm-ocean-6030.herokuapp.com/api/accounts/request/invite/';
var perms = 'email,user_birthday,user_location,read_stream';

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

    var desc = $('#desc_input').val();
    if (desc == '') {
        signup_notify('error', 'Please tell us how you heard about Rate My Video.', false);
        return;
    }

    window.location = 'https://www.facebook.com/dialog/oauth/?client_id=' + 
        APP_ID + '&redirect_uri=' + RED_URL + '&state="' + desc + '"&scope=' +
        perms;
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
