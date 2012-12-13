google.load('visualization', '1.0', {'packages':['corechart', 'geochart']});
google.setOnLoadCallback(drawAllTheCharts);

CHARTS_LIST = [drawRatingsChart, drawNewUsersChart, drawPopulationChart]

function drawAllTheCharts()
{
    for (var argi = 0; argi < CHARTS_LIST.length; ++argi) CHARTS_LIST[argi]();
}

function drawRatingsChart()
{
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'Ratings');
    data.addRows(jsonVars['rdates']);
    var options = {
        'title': 'Rating Activity',
        'width': 800,
        'height': 600,
        'curveType': 'function'
    };
    var chart = new google.visualization.LineChart(document.getElementById('ratings-chart'));
    chart.draw(data, options);
}

function drawNewUsersChart()
{
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'New Users');
    data.addRows(jsonVars['udates']);
    var options = {
        'title': 'New Registrations',
        'width': 800,
        'height': 600,
        'colors': ['red'],
        'curveType': 'function'
    };
    var chart = new google.visualization.LineChart(document.getElementById('new-users-chart'));
    chart.draw(data, options);
}

function drawPopulationChart()
{
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'State');
    data.addColumn('number', 'Users');
    data.addRows(jsonVars['ustates']);
    var options = {
        'region': 'US',
        'resolution': 'provinces'
    }
    var chart = new google.visualization.GeoChart(document.getElementById('users-region-chart'));
    chart.draw(data, options);
}
