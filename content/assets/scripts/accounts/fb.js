var APP_ID = jsonVars['APP_ID'];
var DOMAIN = jsonVars['DOMAIN'];
var PERMISSIONS = jsonVars['SCOPE'];

// Additional JS functions here
window.fbAsyncInit = function() {

    FB.init({
        appId      : APP_ID, // App ID
        channelUrl : jsonVars['CHANNEL'], // Channel File
        status     : true, // check login status
        cookie     : true, // enable cookies to allow the server to access the session
        xfbml      : true  // parse XFBML
    });

    login();
    // FB.getLoginStatus(function(response) {
    //         login();
    //         // if (response.status === 'connected') {
    //         //             // connected
    //         //             testAPI();
    //         //             login();
    //         //         } else if (response.status === 'not_authorized') {
    //         //             // not_authorized
    //         //             login();
    //         //         } else {
    //         //             // not_logged_in
    //         //             login();
    //         //         }
    //     });
};

// Load the SDK Asynchronously
(function(d){
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement('script'); js.id = id; js.async = true;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));

function login() {
    FB.login(function(response) {
        if (response.authResponse) {
            // connected
            getUser();
            responseAPI();
        } else {
            // cancelled
            onFBLoginCancel();
        }
    }, {scope: 'email,user_birthday,user_location'});
}

function getUser()
{
    FB.api('/me', function(response) {
        $.ajax({
            type: "GET",
            async: false, 
            url: '/api/accounts/user/' + response.id + '/',
            contentType: 'application/json; charset=utf-8',
            success: function(result) { },
            error: function(error) { console.log(error.responseText); },
            statusCode: {
                200: function() {
                    console.log('success');
                },
                403: function() {
                    window.location = DOMAIN + 'login/invite_required/';
                }
            }
        });
    });
}

function responseAPI() {
    FB.api('/me', function(response) {
        var status = document.getElementById('login_status');
        status.innerText = 'Good to see you, ' + response.name + '!';
    });
}

function onFBLoginCancel()
{
    $('#login_status').html('You must login and approve the requested permissions ' +
        'before using Rate My Video.<br /><br />' + '(Refresh the page to try again)');
}

function onLoginButton()
{
    window.location = 'https://graph.facebook.com/oauth/authorize?' +
        'client_id=' + APP_ID + '&redirect_uri=' + DOMAIN + 'login/&scope=' +
        PERMISSIONS;
}

