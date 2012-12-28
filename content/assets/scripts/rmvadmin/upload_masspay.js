$('#commit-button').click(function() {
    if (confirm('Confirm Mass Payout\n\nSubmit this mass payout?'))
    {
        var entries = document.getElementsByClassName('po-entry');
        var num_errors = 0
        var error_msgs = ''
        for (var argi = 0; argi < entries.length; ++argi)
        {
            var fb_id = entries[argi].getElementsByClassName('po-fb-id')[0].innerHTML;
            var amount = entries[argi].getElementsByClassName('po-amount')[0].innerHTML;
            var amt_float = parseFloat(amount);
            if (isNaN(amt_float))
            {
                num_errors += 1;
                error_msgs += amount + ' is not a valid floating point number\n';
            }

            $.ajax({
                type: 'POST',
                async: false,
                url: '/api/accounts/payout/',
                data: [
                    { name: 'fb_id', value: fb_id },
                    { name: 'amount', value: amt_float }
                ],
                contentType: 'application/json; charset=utf-8',
                error: function(err) { num_errors += 1; error_msgs += err.responseText + '\n'; },
            });
        }
        if (num_errors != 0) { $("#pending-payouts").notify({type: 'error', message: error_msgs}); }
        else { $("#pending-payouts").notify({type: 'success', 
            message: 'Payouts have been commited!'}); }
    }
});