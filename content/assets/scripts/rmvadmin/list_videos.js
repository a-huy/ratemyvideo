$('#num-select').change(function() {
    var num = $('#num-select').val();
    var loc = window.location.origin + '/rmvadmin/list_videos/?';
    if (jsonVars['filter']) loc += 'filter=' + jsonVars['filter'] + '&';
    if (jsonVars['rev'] == 'true') loc += 'rev&';
    loc += 'num=' + num;
    window.location = loc;
});
