google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(drawAllTheCharts);

CHARTS_LIST = [drawRatingsChart, drawRatingSumsChart]

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
        'colors': ['green']
    };
    var chart = new google.visualization.LineChart(document.getElementById('ratings-sums-chart'));
    chart.draw(data, options);
}

