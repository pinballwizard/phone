/**
 * Created by pinballwizard on 16.05.16.
 */

$(document).ready(function () {
    $.getJSON("/sms/month_graph", function (data, status) {
        var sended = data.sended;
        var received = data.received;
        var success = data.success;
        sended = sended.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        received = received.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        success = success.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        $('#month-chart').highcharts({
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
                name: 'Отправленные',
                data: sended
            },{
                name: 'Полученные',
                data: received
            },{
                name: 'Успешные',
                data: success
            }]
        })
    });
        $.getJSON("/sms/daily_graph", function (data, status) {
        var sended = data.sended;
        var received = data.received;
        var success = data.success;
        sended = sended.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        received = received.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        success = success.map(function (item) {
            return [Date.parse(item[0]), item[1]];
        });
        $('#daily-chart').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Количество по по дням'
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
                name: 'Отправленные',
                data: sended
            },{
                name: 'Полученные',
                data: received
            },{
                name: 'Успешные',
                data: success
            }]
        })
    });
});