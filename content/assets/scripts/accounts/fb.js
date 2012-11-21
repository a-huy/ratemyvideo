var APP_ID = '397851696951181';
var DOMAIN = 'http://www.ratemyvideo.co/';
var PERMISSIONS = 'email,user_birthday,user_location,read_stream';

// Additional JS functions here
window.fbAsyncInit = function() {

    FB.init({
        appId      : '397851696951181', // App ID
        channelUrl : 'http://www.ratemyvideo.co/login/channel/', // Channel File
        status     : true, // check login status
        cookie     : true, // enable cookies to allow the server to access the session
        xfbml      : true  // parse XFBML
    });

    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            // connected
            testAPI();
            login();
        } else if (response.status === 'not_authorized') {
            // not_authorized
            login();
        } else {
            // not_logged_in
            login();
        }
    });

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
            testAPI();
        } else {
            // cancelled
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
            success: function(result) { console.log('success!'); },
            error: function(error) { console.log(error.responseText); }
        });
    });
}

function testAPI() {
    FB.api('/me', function(response) {
        var status = document.getElementById('login_status');
        status.innerText = 'Good to see you, ' + response.name + '!';
    });
}

function onLoginButton()
{
    window.location = 'https://graph.facebook.com/oauth/authorize?' +
        'client_id=' + APP_ID + '&redirect_uri=' + DOMAIN + 'login/&scope=' +
        PERMISSIONS;
}

