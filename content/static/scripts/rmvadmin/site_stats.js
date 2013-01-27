google.load('visualization', '1.0', {'packages':['corechart', 'geochart']});
google.setOnLoadCallback(drawAllTheCharts);

CHARTS_LIST = [drawDailyUsersCountChart, drawRatingsChart, drawRatingSumsChart,
    drawNewUsersChart, drawPopulationChart]

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

function drawRatingSumsChart()
{
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'Total (USD)');
    data.addRows(jsonVars['rsums']);
    var options = {
        'title': 'User Earnings',
        'width': 800,
        'height': 600,
        'curveType': 'function',
        'colors': ['green']
    };
    var chart = new google.visualization.LineChart(document.getElementById('ratings-sums-chart'));
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

function drawDailyUsersCountChart()
{
    var data = new google.visualization.DataTable()
    data.addColumn('string', 'Date');
    data.addColumn('number', 'Unique Users');
    data.addRows(jsonVars['ducounts']);
    var options = {
        'title': 'Unique Raters',
        'width': 800,
        'height': 600,
        'colors': ['orange'],
        'curveType': 'function'
    }
    var chart = new google.visualization.LineChart(document.getElementById('ducounts-chart'));
    chart.draw(data, options);
}
