$(document).ready(function() {
    $('#sel-all-checkbox').click(function() { toggleAllRequests(); });
    $('#confirm-button').click(function() { onButtonConfirm(); });
});

function toggleAllRequests()
{
    var invites_list = $('.invite-checkbox')
    for (var argi = 0; argi < invites_list.length; ++argi)
    {
        if ($('#sel-all-checkbox').is(':checked')) 
            invites_list[argi].setAttribute('checked', true);
        else invites_list[argi].removeAttribute('checked');
    }
}

function onButtonConfirm()
{
    var checked_list = $('.invite-checkbox').filter(':checked');
    var action = $('#action-list').val();
    var action_error;
    if (checked_list.length == 0)
    {
        actionNotify('error', 'There are no selected requests', false);
        return;
    }
    for (var argi = 0; argi < checked_list.length; ++argi)
    {
        var fb_id = checked_list[argi].getAttribute('name');
        if (action == 'accept') {
            $.ajax({
                type: 'POST',
                async: false,
                url: '/api/accounts/whitelist/',
                data: [
                    { name: 'fb_id', value: fb_id }
                ],
                contentType: 'application/json; charset=utf-8',
                error: function(err) { action_error = 'Error while saving request with FB ID ' + fb_id + ': ' + err.responseText; }
            });
        }
        else if (action == 'ignore') {
            $.ajax({
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-HTTP-Method-Override', 'DELETE');
                },
                type: 'POST',
                async: false,
                url: '/api/accounts/request/invite/',
                data: [
                    { name: 'fb_id', value: fb_id }
                ],
                contentType: 'application/json; charset=utf-8',
                error: function(err) { action_error = 'Error while deleting request with FB ID ' + fb_id + ': ' + err.responseText; }
            });
        }
        if (action_error != undefined) actionNotify('error', action_error, true);
    }
    actionNotify('success', 'Changes have been applied!', true);
}

function actionNotify(type, msg, refresh)
{
    $('#invite-actions').notify({
        type: type,
        message: msg,
        timeOut: 5000,
        refresh: refresh
    });
}
