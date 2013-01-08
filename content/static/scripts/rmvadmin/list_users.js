$('#xlsx-export-button').click(function() {
    var ind = window.location.href.indexOf('?');
    export_str = 'export';
    if (ind == -1) export_str = '?' + export_str;
    else export_str = '&' + export_str;
    window.location = window.location.href + export_str;
});

$('#num-select').change(function() {
    var num = $('#num-select').val();
    var loc = window.location.origin + '/rmvadmin/list_users/?';
    if (jsonVars['filter']) loc += 'filter=' + jsonVars['filter'] + '&';
    if (jsonVars['rev'] == 'true') loc += 'rev&';
    if (num != 'all') loc += 'num=' + num;
    else loc = loc.substring(0, loc.length - 1);
    window.location = loc;
});
