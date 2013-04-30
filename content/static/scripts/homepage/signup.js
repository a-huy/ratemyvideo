var APP_ID = jsonVars['APP_ID'];
var RED_URL = jsonVars['RED_URL'];
var perms = jsonVars['SCOPE'];

$(function() {
    $(document).tooltip();
});

$(document).ready(function() {
    $('#invite-submit-button').click(function() {
        onSubmitInviteRequest();
    });
    $('#pp-email-input').keyup(function(evt) {
        if (evt.keyCode == 13) onSubmitInviteRequest();
    });
});

function onSubmitInviteRequest()
{
    var desc = $('#referral-input').val();
    if (desc == '') {
        signup_notify('error', 'Please tell us how you heard about Rate My Video.', false);
        return;
    }
    var pp_email = $('#pp-email-input').val();
    if (pp_email == '') {
        signup_notify('error', 'Please enter a Paypal email.', false);
        return;
    }

    var state = desc + '$|' + pp_email;
    window.location = 'https://www.facebook.com/dialog/oauth/?client_id=' +
        APP_ID + '&redirect_uri=' + RED_URL + '&state=' + state + '&scope=' +
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
