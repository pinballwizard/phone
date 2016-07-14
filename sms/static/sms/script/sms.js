/**
 * Created by pinballwizard on 16.05.16.
 */

function date_repack(item) {
    return [Date.parse(item[0]), item[1]];
}

$(document).ready(function () {
    $.getJSON("/sms/month_graph", function (data, status) {
        var sended = data.sended.map(date_repack);
        var sended_summary = data.sended_summary.map(date_repack);
        var received = data.received.map(date_repack);
        var received_summary = data.received_summary.map(date_repack);
        var successed = data.successed.map(date_repack);
        var successed_summary = data.successed_summary.map(date_repack);
        $('#month').highcharts({
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
                data: successed
            }]
        });
        $('#month-summary').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Суммарное количество по месяцам'
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
                data: sended_summary
            },{
                name: 'Полученные',
                data: received_summary
            },{
                name: 'Успешные',
                data: successed_summary
            }]
        });
    });
    $.getJSON("/sms/daily_graph", function (data, status) {
        var sended = data.sended.map(date_repack);
        var sended_summary = data.sended_summary.map(date_repack);
        var received = data.received.map(date_repack);
        var received_summary = data.received_summary.map(date_repack);
        var successed = data.successed.map(date_repack);
        var successed_summary = data.successed_summary.map(date_repack);
        $('#daily').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Количество по дням'
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
                data: successed
            }]
        });
        $('#daily-summary').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Суммарное количество по дням'
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
                data: sended_summary
            },{
                name: 'Полученные',
                data: received_summary
            },{
                name: 'Успешные',
                data: successed_summary
            }]
        })
    });
    $.getJSON("/sms/subscribers_graph", function (data, status) {
        var subscribers = data.subscribers.map(date_repack);
        var subscribe = data.subscribe.map(date_repack);
        var subscribers_summary = data.subscribers_summary.map(date_repack);
        $('#subscribers').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Количество по дням'
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
                name: 'Новых абонентов',
                data: subscribers
            },{
                name: 'Абонентов в день',
                data: subscribe
            }]
        });
        $('#subscribers-summary').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Суммарное количество по дням'
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
                name: 'Всего абонентов',
                data: subscribers_summary
            }]
        })
    });
});