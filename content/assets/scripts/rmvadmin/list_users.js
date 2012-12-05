$('#xlsx-export-button').click(function() {
    var ind = window.location.href.indexOf('?');
    export_str = 'export';
    if (ind == -1) export_str = '?' + export_str;
    else export_str = '&' + export_str;
    window.location = window.location.href + export_str;
});
