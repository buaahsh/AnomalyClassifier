function PlotOneContainer(ContainerId, x){
	
	var data = GetPlotData(ContainerId, x);
	$('#' + ContainerId).highcharts({
//		chart: {
//			type : 'scatter',
//			zoomType : 'xy'
//		},
	    xAxis: {
//	        title: {
//	            text: 'Temperature (°C)'
//	        },
	    },
	    yAxis: {
//	        title: {
//	            text: 'Temperature (°C)'
//	        },
	        plotLines: [{
	            value: 0,
	            width: 1,
	            color: '#808080'
	        }]
	    },
	    legend: {
	        layout: 'vertical',
	        align: 'right',
	        verticalAlign: 'middle',
	        borderWidth: 0
	    },
	    series:  data
	});
}

function PlotContainer(){
	$.each($(".plot_container"), function(idx, item){
		var ContainerId = $(item)[0].id;
		PlotOneContainer(ContainerId, 0);
	});
}

function GetPlotData(ContainerId, xaxis){
	var data = new Array();
	var tokens = ContainerId.split("_")
	var tableid = tokens[0] + "_" + tokens[1] + "_table";
	var num = 0;
	var x_group = new Array();
	$.each($("#" + tableid + " tbody tr"), function(idx, item){
		var tds = $(item).children("td");
		num = tds.length;
		$.each(tds, function(i, tem){
			if (i == xaxis){
				x_group.push(parseFloat($(tem).text()));
			}
		});
	});
	
	for (var j=0; j<num ;j++)
	{
		if (j==xaxis)
			continue;
		var subdata = new Array();
		$.each($("#" + tableid + " tbody tr"), function(idx, item){
			var tds = $(item).children("td");
			num = tds.length;
			$.each(tds, function(i, tem){
				if (i == j){
					subdata.push([x_group[idx], parseFloat($(tem).text())]);
				}
			});
		});
		var name = "";
		$.each($("#" + tableid + " thead th span"), function(idx, item){
			if (idx == j)
				name = $(item).text();
		});
		data.push({
			name : name,
			data: subdata,
		});
	}
	return data;
}

function DataItemProc(dataItem)
{
	var html = getLittletitle(dataItem.id, dataItem.title);
	html += "<div class=\"highlight\">";
	switch(dataItem.type){ 
		case "TitleDataItem":    
			return getTitle(dataItem.id, dataItem.title)
    	break; 
	    case "SubtitleDataItem":    
	    	return getSubtitle(dataItem.id, dataItem.title)
	    	break; 
	    case "ImageDataItem":
	    	html += ImageDataItemProc(dataItem.id, dataItem.data);
	    	break;
	    case "FileDataItem":
	    	html += FileDataItemProc(dataItem.id, dataItem.data);
	    	break;
	    case "TextDataItem":
	    	html += TextDataItemProc(dataItem.id, dataItem.data);
	    	break;
	    case "FloatDataItem":
	    	html += FloatDataItemProc(dataItem.id, dataItem.data);
	    	break;
	    case "RadioDataItem":
	    	html += RadioDataItemProc(dataItem.id, dataItem.data);
	    	break;
	    case "UrlDataItem":
	    	html += UrlDataItemProc(dataItem.id, dataItem.data);
	    	break;
	    case "CurveDataItem":
	    	html += CurveDataItemProc(dataItem.id, dataItem.data);
	    	break;
	    case "D3DataItem":
	    	html += D3DataItemProc(dataItem.id, dataItem.data);
	    	break;	
	    default:
	    	break;
	}
	html += "</div>";
	return html;
}

function getTitle(id, title){
	return "<h1 id=\""+id+"\"><span>"+title+"</span></h1>";
}

function getSubtitle(id, title){
	return "<h2 id=\""+id+"\">"+title+"</h2>";
}

function getLittletitle(id, title){
	return "<h3 id=\""+id+"\">"+title+"</h3>";
}

function ImageSilde(){
	$.each($(".imgslides"), function(idx, item){
		$(item).slidesjs({
		      width: 940,
		      height: 528,
		      //navigation: false
	    });
	});
}

function CurveDataItemProc(id, data)
{
	var tableid = id + "_table";
	var plotid = id + "_plot";
	var thead = "<tr>";
	$.each(data.table[0], function(idx, item){
		thead += "<th><span>"+item
		+"</span><label><input onclick='RadioClick(this)' type=\"radio\" class='table_radio' name=\"radio_"+tableid+"\"> X轴</label>"
		+"</th>";
	});
	thead += "</tr>";
	
	var tbody = "";
	$.each(data.table, function(idx, item){
		if (idx != 0){
			tbody += "<tr>";
			$.each(item, function(i, tem){
				tbody += "<td>"+tem+"</td>";
			});
			tbody += "</tr>";
		}
	});
	
	var html = 
		"<ul class=\"nav nav-tabs\">"
		+"   <li class=\"active\">"
		+"      <a href=\"#"+tableid+"\" data-toggle=\"tab\">"
		+"         数据"
		+"      </a>"
		+"   </li>"
		+"   <li><a href=\"#"+plotid+"\" data-toggle=\"tab\">曲线</a></li>"
		+"</ul>"
		+"<div  class=\"tab-content\">"
		+"   <div class=\"tab-pane fade in active\" id=\""+tableid+"\">"
		+"      <table class=\"table table-bordered\">"
		+"          <thead>"
		+ thead
		+"          </thead>"
		+"          <tbody>"
		+ tbody
		+"          </tbody>"
		+"        </table>"
		+"   </div>"
		+"   <div class=\"tab-pane fade\" id=\""+plotid+"\">"
		+"        <div id=\""+plotid+"_container\" class='plot_container' style=\"min-width:1000px; height:400px\"></div>   "
		+"   </div>"
		+"</div>";
	//min-width:700px;
	return html;
}

function ImageDataItemProc(id, data)
{
	if (data.flag == 1){
		var html = "<div class='imgslides'>";
		$.each(data.urls, function(idx, item){
			html += "<img src=\"\DataItem?arg=file&file="+item+"\">";
		});
	    return html;
	}
	else{
		var html = "<div class='imgslides'>";
		$.each(data.urls, function(idx, item){
			html += "<img src=\""+item+"\">";
		});
	    return html;
	}
}

function FileDataItemProc(id, data){
	var html = "";
	$.each(data.filePaths, function(idx, item){
		html += "<p><span class=\"glyphicon glyphicon-file\" aria-hidden=\"true\"></span><a>"
			+item+"</a></p>";
	});
  	return html;
}

function TextDataItemProc(id, data){
	var html = "";
	$.each(data.text, function(idx, item){
		html += "<p>"+item+"</p>";
	});
  	return html;
}

function FloatDataItemProc(id, data){
	var html = "";
	html = "<p class=\"float\"><span>"+data.value+"</span>"+data.unit+"</p>";
  	return html;
}

function RadioDataItemProc(id, data){
	var html = "";
	$.each(data.filePaths, function(idx, item){
		html += "<p><span class=\"glyphicon glyphicon-music\" aria-hidden=\"true\"></span><a>"
			+item+"</a></p>";
	});
  	return html;
}

function UrlDataItemProc(id, data){
	var html = "";
	$.each(data.links, function(idx, item){
		html += "<p><a>"+item+"</a></p>";
	});
  	return html;
}

function D3DataItemProc(id, data){
	var html = "<div style='text-align: center;'>"
		+ "<embed src=\"\DataItem?arg=file&file="+data.link+"\" width=\"80%\" height=\"400\" "
		+" type=\"application/x-cortona\"   pluginspage=\"http://www.cortona3d.com/cortona\"   vrml_splashscreen=\"false\" "
		+" vrml_dashboard=\"false\"   vrml_background_color=\"#f7f7f9\"   contextmenu=\"false\" ></div>"
  	return html;
}