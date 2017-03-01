/*
	填写内容
	@author: Shaohan
*/

$(function(){
	select();
})

function select(){
	$('#submit').click(function(){
		$('#myPleaseWait').modal('show');
//	$('#select').change(function(){
		
		var p1=$('#select').children('option:selected').val();
		var dc = $('#select_cat').children('option:selected').val();
		
		$('#tb_label').empty();
		if (dc == 'r'){
			$('#tb_label').append('<a href="http://10.4.13.214:6007/" target="_blank"> TensorBoard</a>');
		}
		if (dc == 'i'){
			$('#tb_label').append('<a href="http://10.4.13.214:6006/" target="_blank"> TensorBoard</a>');
		}
		if (dc == 'te'){
			$('#tb_label').append('<a href="http://10.4.13.214:6008/" target="_blank"> TensorBoard</a>');
		}
			
		$.getJSON("/AnomalyPortal/Data?kind=multireal&dc=" + dc + "&fid=" + p1
				, function(data){
			$("#container").empty();
			plot(data, '#container');
			$.getJSON("/AnomalyPortal/Data?kind=multi&dc=" + dc + "&fid=" + p1
					, function(data){
				$("#container3").empty();
				plot(data, '#container3');
				$('#myPleaseWait').modal('hide');
			});
		});
	});
	
	$('#download').click(function(){
		var p1=$('#select').children('option:selected').val();
		var dc = $('#select_cat').children('option:selected').val();
		window.location = "/AnomalyPortal/Data?kind=download&dc=" + dc + "&fid=" + p1;
	});
}

function plot(series, id){
	
//	Highcharts.setOptions({colors: ['#87ceff','#6b8e23','#4876ff']});
	var chart = $(id).highcharts({
		chart: {
            type: 'scatter',
			zoomType: 'x'
		},
        title: {
            text: ''
        },
        xAxis: {
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
	$.getJSON("/AnomalyPortal/Data?kind=ana&dc=" + dc + "&fid=" + p1
			+ "&x=" + x
			, function(data){
		$('#container2').append('<h4>real label:' + data.label + '</h4>');
		$('#container2').append('<h4>predict score:' + data.score + '</h4>');
		
		var items = data.items;
		var table = '<table class="table table-striped"><thead><tr><th>Name</th><th>Score</th><th>Current</th><th>Context</th></tr><tbody>';
		$.each(items, function(idx, item){
			var itemob = JSON.parse(item); 
			table += '<tr><th scope="row">' + itemob.name + '</th>';
			table += '<td>' + itemob.score + '</td>';
			table += '<td>' + itemob.current + '</td>';
			table += '<td>' + itemob.context + '</td></tr>';
		});
		table += '</tbody></table>';
		$('#container2').append(table);
		$('#myPleaseWait').modal('hide');
	});
	$('#myPleaseWait').modal('hide');
}