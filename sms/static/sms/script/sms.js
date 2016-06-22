/**
 * Created by pinballwizard on 16.05.16.
 */

$(document).ready(function () {
    $.getJSON("/sms/xhr", function (data, status) {
        var sended = data.sended;
        var received = data.received;
        sended = sended.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        received = received.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        $('#chart-container').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Количество по месяцам'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Количество'
                }
            },
            series: [{
                name: 'Отправленные sms',
                data: sended
            },{
                name: 'Полученные sms',
                data: received
            }]
        })
    });
});