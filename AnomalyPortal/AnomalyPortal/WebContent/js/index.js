/*
	填写内容
	@author: Shaohan
*/

$(function(){
	//init();
	select_cat();
	select();
})

function init() {
	var arg = 'test1';
	$.getJSON("/AnomalyPortal/Data?file=" + arg + "&date=2015/06" , function(data){
		plot(data);
	});
}

function select_cat(){
	$('#select_cat').change(function(){
		var p1=$(this).children('option:selected').val();
		$.getJSON("/AnomalyPortal/Data?kind=list&dc=" + p1, function(data){
			$.each(data, function(idx, item){
				$('#select').append("<option value='" 
						+ item[1] +  "'> " + item[0] + "</option>");
			})
			
		});
	});
}

function select(){
	$('#select').change(function(){
		var p1=$(this).children('option:selected').val();
		var dc = $('#select_cat').children('option:selected').val();
		$.getJSON("/AnomalyPortal/Data?kind=data&dc=" + dc + "&fid=" + p1, function(data){
			plot(data);
		});
	});
}

function plot(series) {
	var chart = $('#container').highcharts({
		chart: {
//            type: 'spline'
			type: 'scatter',
			zoomType: 'x'
		},
        title: {
            text: '井口环空压力数据分析'
        },
//        subtitle: {
//            text: 'Irregular time data in Highcharts JS'
//        },
        xAxis: {
//            type: 'datetime',
//            dateTimeLabelFormats: { // don't display the dummy year
//                month: '%e. %b',
//                year: '%b'
//            },
            title: {
                text: 'Date'
            }
        },
        yAxis: {
//            title: {
//                text: 'Snow depth (m)'
//            },
        },
//        tooltip: {
//            headerFormat: '<b>{series.name}</b><br>',
//            pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
//        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: true
                }
            }
        },

        series: series
    })
    .highcharts(); // return chart
}