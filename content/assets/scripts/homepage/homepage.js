var APP_ID = '397851696951181';
var RED_URL = 'http://www.ratemyvideo.co/api/accounts/request/invite/';
var perms = 'email,user_birthday,user_location,read_stream';

$(document).ready(function() {
    $('#invite-submit-button').click(function() {
        onSubmitInviteRequest();
    });
    $('#desc-input').keyup(function(evt) {
        if (evt.keyCode == 13) onSubmitInviteRequest();
    });
});

function onSubmitInviteRequest()
{
    var desc = $('#desc-input').val();
    if (desc == '') {
        signup_notify('error', 'Please tell us how you heard about Rate My Video.', false);
        return;
    }

    window.location = 'https://www.facebook.com/dialog/oauth/?client_id=' +
        APP_ID + '&redirect_uri=' + RED_URL + '&state=' + desc + '&scope=' +
        perms;
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
