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
            pointFormat: '<b>{point.y:.2f}</b><br> at {point.x}'
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
//            		legendItemClick:function(event){return false;}//屏蔽单击图例事件，防止卡顿
            	},
            	point: {
                    events: {
                        click: function () {
                        	analysis(this.x);
                        }
                    }
                }
            }
        },

        series: series
    })
    .highcharts(); // return chart
}

function analysis(x){
	$('#container2').empty();
	$('#myPleaseWait').modal('show');
	
	var p1=$('#select').children('option:selected').val();
	var dc = $('#select_cat').children('option:selected').val();
	$.get("/AnomalyPortal/Data?kind=ana&dc=" + dc + "&fid=" + p1
			+ "&x=" + x
			, function(data){
		
		var items = eval(data);
		var table = '<table class="table table-striped"><thead><tr><th>Name</th><th>Score</th><th>Context</th></tr><tbody>';
		$.each(items, function(idx, item){
			var itemob = JSON.parse(item); 
			table += '<tr><th scope="row">' + itemob.name + '</th>';
			table += '<td>' + itemob.score + '</td>';
			table += '<td>' + itemob.context + '</td></tr>';
		});
		table += '</tbody></table>';
		$('#container2').append(table);
		$('#myPleaseWait').modal('hide');
	});
}