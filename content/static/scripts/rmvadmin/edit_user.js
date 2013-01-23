$('#name-edit-button').click(function() {
    if (this.id == 'name-edit-button')
    {
        var name = $('#user-name-input').text().trim();
        $('#user-name-input').html('<input type="text" id="name-input" name="name-input" value="'
            + name + '" size="35">').removeClass('edited');
        $('#name-edit-button').text('Done');
        this.id = 'name-done-button';
    }
    else
    {
        var name = $('#name-input').val();
        $('#user-name-input').html(name).addClass('edited');
        $('#edit-warning').text('You have made edits that must be saved!');
        $('#name-done-button').text('Edit');
        this.id = 'name-edit-button';
    }
});

$('#pp-email-edit-button').click(function() {
    if (this.id == 'pp-email-edit-button')
    {
        var pp_email = $('#user-pp-email-input').text().trim();
        $('#user-pp-email-input').html('<input type="text" id="pp-email-input" name="pp-email-input" value="'
            + pp_email + '"  size="35">').removeClass('edited');
        $('#pp-email-edit-button').text('Done');
        this.id = 'pp-email-done-button';
    }
    else
    {
        var pp_email = $('#pp-email-input').val();
        $('#user-pp-email-input').html(pp_email).addClass('edited');
        $('#edit-warning').text('You have made edits that must be saved!');
        $('#pp-email-done-button').text('Edit');
        this.id = 'pp-email-edit-button';
    }
});

$('#balance-edit-button').click(function() {
    if (this.id == 'balance-edit-button')
    {
        var balance = $('#user-balance-input').text().trim();
        $('#user-balance-input').html('<input type="text" id="balance-input" name="balance-input" value="'
            + balance + '" size="35">').removeClass('edited');
        $('#balance-edit-button').text('Done');
        this.id = 'balance-done-button';
    }
    else
    {
        var balance = $('#balance-input').val();
        var earned = parseFloat($('#user-earned-input').text().trim());
        if (balance == '')
        {
            $('#edit-warning').text('Please enter a balance amount.');
            return;
        }
        balance = parseFloat(balance);
        if (isNaN(balance))
        {
            $('#edit-warning').text('The balance amount is not valid.');
            return;
        }
        $('#user-balance-input').html(balance).addClass('edited');
        $('#edit-warning').text('You have made edits that must be saved!');
        $('#balance-done-button').text('Edit');
        this.id = 'balance-edit-button';
    }
});

$('#verified-toggle-button').click(function() {
    var state = $('#user-verified-input').html().trim().charCodeAt(0);
    if (state == 10007) $('#user-verified-input').html('&#x2713;');
    else $('#user-verified-input').html('&#x2717;');
    $('#user-verified-input').addClass('edited');
    $('#edit-warning').text('You have made edits that must be saved!');
});

$('#save-button').click(function() {
    edited = document.getElementsByClassName('edited');
    if (edited.length < 1)
    {
        $('#edit-warning').text('You have no changes to be commited!');
        return;
    }
    var name = $('#user-name-input').text().trim();
    var pp_email = $('#user-pp-email-input').text().trim();
    var verified = $('#user-verified-input').text().trim().charCodeAt(0);
    var balance = parseFloat($('#user-balance-input').text().trim());
    verified = verified == 10003 ? 'true' : 'false'
    if (name == '')
    {
        $('#edit-warning').text('You are in the middle of editing one or more fields. ' +
            'Finish editing before saving your changes.');
        return;
    }
    if (confirm('Confirm Commit Edits\n\nCommit these changes?'))
    {
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-HTTP-Method-Override', 'PUT');
            },
            type: 'POST',
            async: false,
            url: '/api/accounts/user/' + jsonVars['fb_id'] + '/',
            data: [
                { name: 'verified', value: verified },
                { name: 'real_name', value: name },
                { name: 'pp_email', value: pp_email },
                { name: 'balance', value: balance }
            ],
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
