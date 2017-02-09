/*
	填写内容
	@author: Shaohan
*/

$(function(){
	select_cat();
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

function select_cat(){
	$('#select_cat').change(function(){
		$('#select').empty();
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
		$.getJSON("/AnomalyPortal/Data?kind=data&dc=" + dc + "&fid=" + p1
				+ "&p=" + p
				+ "&ratio=" + ratio
				+ "&eps=" + eps
				+ "&minpts=" + minpts
				+ "&r=" + r
				, function(data){
			plotNew(data.result);
			plot(data.core);
			$('#myPleaseWait').modal('hide');
		});
	});
}

function plotNew(series) {
	$('#container').empty();
	
	var data = series.points;
    var detailChart;
    // create the detail chart
    function createDetail(masterChart) {

        // prepare the detail chart
        var detailData = [],
            detailStart = data[0].x;

        $.each(masterChart.series[0].data, function () {
            if (this.x >= detailStart) {
            	if (this.description.indexOf('1') == 0){
            		detailData.push({'y':this.y, 'color': 'rgb(247, 163, 92)', 'description': this.description});
            	}
            	else{
            		detailData.push({'y':this.y, 'description': this.description});
            	}
            }
        });

        // create a detail chart referenced by a global variable
        detailChart = Highcharts.chart('detail-container', {
            chart: {
            	type: 'scatter',
                marginBottom: 120,
                reflow: false,
                marginLeft: 50,
                marginRight: 20,
                style: {
                    position: 'absolute'
                }
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'IDBSCAN Results'
            },
            xAxis: {
//                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: null
                },
            },
//            tooltip: {
//                formatter: function () {
//                    var point = this.points[0];
//                    return '<b>' + point.series.name + '</b><br/>' + Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>' +
//                        '1 USD = ' + Highcharts.numberFormat(point.y, 2) + ' EUR';
//                },
//                shared: true
//            },
            tooltip: {
//                headerFormat: 
//                	function(){
//////                	var point = this.points[0];
//////                	d = point.description;
////                	var text = 'Normal'
//////                	if (d.indexOf('1') == 0){
//////                		text = 'Anomaly';
////                	}
//                	return '<b>' + text + '</b><br>';
//                	},
                pointFormatter: 
                	function(){
	                	var d = this.description;
	//                	var text = 'Normal'
	                	if (d.indexOf('1') == 0){
	                		return d;
	                	}
	                	else
	                		return 'Normal';
                	}
                
            },
            legend: {
                enabled: false
            },
            plotOptions: {
            	scatter: {
            		lineWidth:1,
            		dashStyle:'ShortDash',
                    marker: {
                        radius:2
                    }
                },
                series: {
                	turboThreshold:600000
                }
            },
            series: [{
                name: 'Analysis',
                pointStart: detailStart,
                data: detailData
            }],

            exporting: {
                enabled: true
            }

        }); // return chart
    }

    // create the master chart
    function createMaster() {
        Highcharts.chart('master-container', {
            chart: {
                reflow: false,
                borderWidth: 0,
                backgroundColor: null,
                marginLeft: 50,
                marginRight: 20,
                zoomType: 'x',
                events: {

                    // listen to the selection event on the master chart to update the
                    // extremes of the detail chart
                    selection: function (event) {
                        var extremesObject = event.xAxis[0],
                            min = extremesObject.min,
                            max = extremesObject.max,
                            detailData = [],
                            xAxis = this.xAxis[0];

                        // reverse engineer the last part of the data
                        $.each(this.series[0].data, function () {
                            if (this.x > min && this.x < max) {
                            	if (this.description.indexOf('1') == 0){
                            		detailData.push({'x': this.x, 'y':this.y, 'color': 'rgb(247, 163, 92)', 'description': this.description});
                            	}
                            	else{
                            		detailData.push({'x': this.x, 'y':this.y, 'description': this.description});
                            	}
                            }
                        });

                        // move the plot bands to reflect the new detail span
                        xAxis.removePlotBand('mask-before');
                        xAxis.addPlotBand({
                            id: 'mask-before',
                            from: data[0].x,
                            to: min,
                            color: 'rgba(0, 0, 0, 0.2)'
                        });

                        xAxis.removePlotBand('mask-after');
                        xAxis.addPlotBand({
                            id: 'mask-after',
                            from: max,
                            to: data[data.length - 1].x,
                            color: 'rgba(0, 0, 0, 0.2)'
                        });


                        detailChart.series[0].setData(detailData);

                        return false;
                    }
                }
            },
            title: {
                text: null
            },
            xAxis: {
                showLastTickLabel: true,
//                maxZoom: 14 * 24 * 3600000, // fourteen days
                plotBands: [{
                    id: 'mask-before',
                    from: data[0].x,
                    to: data[data.length - 1].x,
                    color: 'rgba(0, 0, 0, 0.2)'
                }],
                title: {
                    text: null
                }
            },
            yAxis: {
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
//                min: 0.6,
                showFirstLabel: false
            },
            tooltip: {
                formatter: function () {
                    return false;
                }
            },
            legend: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            plotOptions: {
                series: {
                	turboThreshold:600000,
                    fillColor: {
                        linearGradient: [0, 0, 0, 70],
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, 'rgba(255,255,255,0)']
                        ]
                    },
                    lineWidth: 1,
                    marker: {
                        enabled: false
                    },
                    shadow: false,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    enableMouseTracking: false
                }
            },

            series: [{
                type: 'area',
                name: series.name,
                pointInterval: 24 * 3600 * 1000,
                pointStart: data[0].x,
                data: data
            }],

            exporting: {
                enabled: false
            }

        }, function (masterChart) {
            createDetail(masterChart);
        }); // return chart instance
    }

    // make the container smaller and add a second container for the master chart
    var $container = $('#container')
        .css('position', 'relative');

    $('<div id="detail-container">')
        .appendTo($container);

    $('<div id="master-container">')
        .css({
            position: 'absolute',
            top: 300,
            height: 100,
            width: '100%'
        })
            .appendTo($container);

    // create master and in its callback, create the detail chart
    createMaster();
    
}

function plot(series){
	$('#container2').empty();
	Highcharts.chart('container2', {
	    title: {
	        text: 'Core Points Changes',
	        x: -20 //center
	    },
	    xAxis: {
	    },
	    yAxis: {
	        title: {
	            text: 'number of core points'
	        },
	        plotLines: [{
	            value: 0,
	            width: 1,
	            color: '#808080'
	        }]
	    },
	    series: [series]
	});
}