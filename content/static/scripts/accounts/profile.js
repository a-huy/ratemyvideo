var orig_email = $('#user-email').text().trim();
var orig_pp_email = $('#user-pp-email').text().trim();

$(function() {
    $(document).tooltip();
});

$('#email-edit-button').click(function() {
    $('#edit-success').text('');
    if (this.id == 'email-edit-button')
    {
        email = $('#user-email').text().trim();
        $('#user-email').html('<input type="text" id="email-input" name="email-input" value="'
            + email + '" size="35">').removeClass('edited');
        $('#edit-warning').text('');
        $('#email-edit-button').text('Done');
        this.id = 'email-done-button';
    }
    else
    {
        var draft_email = $('#email-input').val().trim();
        $('#user-email').html(draft_email);
        if (draft_email != orig_email)
        {
            $('#user-email').addClass('edited');
            $('#edit-warning').text('You have made edits that must be saved!');
        }
        $('#email-done-button').text('Edit');
        this.id = 'email-edit-button';
    }
});

$('#pp-email-edit-button').click(function() {
    $('#edit-success').text('');
    if (this.id == 'pp-email-edit-button')
    {
        pp_email = $('#user-pp-email').text().trim();
        $('#user-pp-email').html('<input type="text" id="pp-email-input" name="pp-email-input" value="'
            + pp_email + '" size="35">').removeClass('edited');
        $('#edit-warning').text('');
        $('#pp-email-edit-button').text('Done');
        this.id = 'pp-email-done-button';
    }
    else
    {
        var draft_pp_email = $('#pp-email-input').val().trim();
        $('#user-pp-email').html(draft_pp_email);
        if (draft_pp_email != orig_pp_email)
        {
            $('#user-pp-email').addClass('edited');
            $('#edit-warning').text('You have made edits that must be saved!');
        }
        $('#pp-email-done-button').text('Edit');
        this.id = 'pp-email-edit-button';
    }
});

$('#save-button').click(function() {
    $('#edit-success').text('');
    edited = document.getElementsByClassName('edited');
    if (edited.length < 1)
    {
        $('#edit-warning').text('You have no changes to be commited!');
        return;
    }
    var email = $('#user-email').text().trim();
    var pp_email = $('#user-pp-email').text().trim();
    if (email == '')
    {
        $('#edit-warning').text('You cannot submit an empty email.');
        return;
    }
    data = [{ name: 'email', value: email}];
    if (pp_email != '' && pp_email != 'None') data.push({ name: 'pp_email', value: pp_email });
    if (confirm('Confirm Commit Edits\n\nCommit these changes?'))
    {
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-HTTP-Method-Override', 'PUT');
            },
            type: 'POST',
            async: false,
            url: '/api/accounts/user/' + jsonVars['fb_id'] + '/',
            data: data,
            contentType: 'application/json; charset=urf-8',
            error: function(err) { $('#edit-warning').text(err.responseText); },
            success: function(msg)
            {
                $('#edit-warning').text('');
                $('#edit-success').text('Changes successfully commited!');
            }
        });
        $('.edited').removeClass('edited');
    }
});