function onButtonAdd()
{
    var yt_id = $('#video-yt-id-input').val();
    var name = $('#video-title-input').val();
    var reward = $('#video-reward-input').val();
    var tags = $('#video-tags-input').val();

    if (yt_id == '')
    {
        notify('error', 'A YouTube ID is required.');
        return;
    }
    if (!valid_ytid(yt_id))
    {
        notify('error', 'The YouTube ID provided is not valid.');
        return;
    }
    if (reward == '')
    {
        notify('error', 'A reward amount is required.');
        return;
    }
    if (!valid_reward(reward))
    {
        notify('error', 'Reward amount must be a valid number and cannot be over $1');
        return;
    }

    $.ajax({
        type: 'POST',
        async: false,
        url: '/api/videos/video/',
        data: [
            { name: 'yt_id', value: yt_id },
            { name: 'title', value: name },
            { name: 'reward', value: reward },
            { name: 'tags', value: tags }
        ],
        contentType: 'application/json; charset=utf-8',
        success: function() { notify('success', 'Video successfully added!'); },
        error: function(err) { notify('error', err.responseText); }
    });

}

function notify(type, msg)
{
    $('#add-video-form').notify({
        type: type,
        message: msg,
        timeOut: 5000
    });
}

function valid_ytid(yt_id)
{
    var ytid_re = /[a-zA-Z0-9\-\_]{11}/;
    return ytid_re.test(yt_id)
}

function valid_reward(reward)
{
    var amt = parseFloat(reward)
    if (isNaN(amt) || amt > 1) return false;
    return true;
}
