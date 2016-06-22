/**
 * Created by pinballwizard on 16.05.16.
 */

$(document).ready(function () {
    $('#chart-container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'статистика по смс'
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
    })
});