$('#payout-button').click(function() {
    var amount = $('#amount-input').val();
    if (amount == '')
    {
        $('#notify-bar').notify({type: 'error', message: 'Please enter a payout amount.',
            timeOut: 5000, refresh: false});
        return;
    }
    amount = parseFloat(amount);
    if (isNaN(amount))
    {
        $('#notify-bar').notify({type: 'error', message: 'Please enter a valid number.',
            timeOut: 5000, refresh: false});
        return;
    }
    if (confirm('Confirm Payout\n\nSubmit this payout?'))
    {
        $.ajax({
            type: 'POST',
            async: false,
            url: '/api/accounts/payout/',
            data: [
                { name: 'fb_id', value: jsonVars['fb_id'] },
                { name: 'amount', value: amount }
            ],
            contentType: 'application/json; charset=utf-8',
            error: function(err)
            {
                $('#notify-bar').notify({type: 'error', message: err.responseText,
                    timeOut: 5000, refresh: false});
            },
            success: function(msg)
            {
                $('#notify-bar').notify({type: 'success', 
                    message: 'Payout has been successfully submitted!',
                    timeOut: 5000, refresh: true});
            }
        });
    }
});

