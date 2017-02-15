/*
	填写内容
	@author: Shaohan
*/

$(function(){
	select();
	init();
})

function init() {
	$.getJSON("/AnomalyPortal/Data?kind=list&dc=y", function(data){
		$.each(data, function(idx, item){
			$('#select').append("<option value='" 
					+ item[1] +  "'> " + item[0] + "</option>");
		})
		var p1 = $($('#select').children()[0]).val();
//		$.getJSON("/AnomalyPortal/Data?kind=data&dc=y&fid=" + p1, function(data){
//			plotNew(data);
//		});
	});
}

function select(){
	$('#submit').click(function(){
		$('#myPleaseWait').modal('show');
//	$('#select').change(function(){
		var p1=$('#select').children('option:selected').val();
		var dc = $('#select_cat').children('option:selected').val();
		var p = $('#p').val();
//		var ratio = $('#ratio').val();
		var ratio = 0;
		var eps = $('#eps').val();
		var minpts = $('#minpts').val();
		var r = $('#r').val();
		$.getJSON("/AnomalyPortal/Data?kind=multi&dc=" + dc + "&fid=" + p1
				+ "&p=" + p
				+ "&ratio=" + ratio
				+ "&eps=" + eps
				+ "&minpts=" + minpts
				+ "&r=" + r
				, function(data){
			plot(data);
			$('#myPleaseWait').modal('hide');
		});
	});
	
	$('#download').click(function(){
		var p1=$('#select').children('option:selected').val();
		var dc = $('#select_cat').children('option:selected').val();
		window.location = "/AnomalyPortal/Data?kind=download&dc=" + dc + "&fid=" + p1;
//		$('#myPleaseWait').modal('show');
//		var p1=$('#select').children('option:selected').val();
//		var dc = $('#select_cat').children('option:selected').val();
//		$.get("/AnomalyPortal/Data?kind=download&dc=" + dc + "&fid=" + p1, function(data){
//			$('#myPleaseWait').modal('hide');
//		});
	});
}

function plot(series){
	$('#container').empty();
//	Highcharts.setOptions({colors: ['#87ceff','#6b8e23','#4876ff']});
	var chart = $('#container').highcharts({
		chart: {
            type: 'scatter',
			zoomType: 'x'
		},
        title: {
            text: ''
        },
        xAxis: {
//            type: 'datetime',
//            dateTimeLabelFormats: { // don't display the dummy year
//                month: '%e. %b',
//                year: '%b'
//            },
//            title: {
//                text: 'Date'
//            }
        },
        yAxis: {
            title: {
                text: null
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }],
        } 
        ,
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:2005/%m/%d %H:%M}<br>{point.y:.2f}'
        },

        plotOptions: {      
        	scatter: {
        		lineWidth:1,
        		dashStyle:'ShortDash',
                marker: {
                    radius:3
                }
            },
            series:{
            	turboThreshold:600000,
            	events:{
            		legendItemClick:function(event){return false;}//屏蔽单击图例事件，防止卡顿
            	}
            }
        },

        series: series
    })
    .highcharts(); // return chart
			
}