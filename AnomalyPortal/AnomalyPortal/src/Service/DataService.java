package Service;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import Model.PointItem;
import Model.ResultItem;
import Model.SeriesItem;

public class DataService {
//	public static String RootPath = "/Users/hsh/Documents/2015/AnomalyClassifier/y_out";
//	private static String PythonPath = "/Users/hsh/Documents/2015/AnomalyClassifier/DBSCAN4AP/Model";
	
	private static String RootPath = "C:\\Users\\Shaohan\\Documents\\project\\anomaly_detection\\AnomalyClassifier\\y_out";	
	private static String PythonPath = "C:\\Users\\Shaohan\\Documents\\project\\anomaly_detection\\AnomalyClassifier\\DBSCAN4AP\\Model";
	private String DataCategory;
	
	public DataService(String dc){	
		DataCategory = Paths.get(RootPath, dc).toString(); 
	}
	
	public String getDataCategory() {
		return this.DataCategory;
	}
	
	/**
	 * 返回该数据类别下面的数据项
	 * @return
	 * {id:name}
	 */
	public List<String[]> LoadItems() {
		List<String[]> items = new ArrayList<String[]>();
		try { 
	        FileInputStream fis = new FileInputStream(Paths.get(DataCategory, "list.txt").toString()); 
	        InputStreamReader isr = new InputStreamReader(fis, "UTF-8"); 
	        @SuppressWarnings("resource")
			BufferedReader br = new BufferedReader(isr); 
	        String line = null;
            
	        while ((line = br.readLine()) != null) {
	        	String[] tokens = line.split(",");
	        	items.add(tokens);
            }
	    } catch (Exception e) { 
	        e.printStackTrace(); 
	    }
		return items;
	}
	
	/**
	 * 加载数据
	 * @param fileName
	 * @return
	 */
	public SeriesItem LoadData(String fileName) {
		SeriesItem item = new SeriesItem();
		item.name = fileName;
		List<PointItem> points = new ArrayList<>();
		List<List<Float>> data = new ArrayList<>();
		
		try { 
	        FileInputStream fis = new FileInputStream(Paths.get(DataCategory, fileName).toString()); 
	        InputStreamReader isr = new InputStreamReader(fis, "UTF-8"); 
	        @SuppressWarnings("resource")
			BufferedReader br = new BufferedReader(isr); 
	        String line = null;
            
	        while ((line = br.readLine()) != null) {
	        	if (line.startsWith("Server") || line.trim().isEmpty())
	        		continue;
	        	String[] tokens = line.split(",");
	        	
//	        	float date = new SimpleDateFormat(  
//	                     "yyyy/MM/dd HH:mm:ss").parse(tokens[3]).getTime();

	        	float date = Float.parseFloat(tokens[0]);
	        	
	        	try {
	        		float value = Float.parseFloat(tokens[1]);
	        		PointItem fItem = new PointItem();
	        		fItem.x = date;
	        		fItem.y = value;
		        	
	        		float label = Float.parseFloat(tokens[2]);
	        		String d = String.format("Monitoring value: <b>%s</b> at %s", 
	        				value, date);
	        		
	        		if (label > 0){
//	        			String color = "rgb(247, 163, 92)";
//	        			fItem.description = "1," + label + d;
	        			d = "Anomaly point<br>" + d;
	        			d = d + "<br>" + "Anomaly degree:<b>" + label + "</b>";
	        		}
	        		else {
	        			d = "Normal point<br>" + d;
					}
	        		fItem.description = d;
	        		
	        		points.add(fItem);
	        		List<Float> dataItem = new ArrayList<>();
	        		dataItem.add(date);
	        		dataItem.add(value);
		        	data.add(dataItem);
				} catch (Exception e) {
				}
            }
	        item.points = points;
	        item.data = data;
	        fis.close();
	    } catch (Exception e) { 
	        e.printStackTrace(); 
	    }
//		SeriesItem[] items = new SeriesItem[]{item};
		return item;
	}
	
	public SeriesItem LoadCore(String fileName) {
		SeriesItem item = new SeriesItem();
		SeriesItem item2 = new SeriesItem();
		item.name = "# core points";
		item2.name = "# core points without pruning";
		List<PointItem> points = new ArrayList<>();
		List<List<Float>> data = new ArrayList<>();
		
		try { 
	        FileInputStream fis = new FileInputStream(Paths.get(DataCategory, fileName).toString()); 
	        InputStreamReader isr = new InputStreamReader(fis, "UTF-8"); 
	        @SuppressWarnings("resource")
			BufferedReader br = new BufferedReader(isr); 
	        String line = null;
            
	        while ((line = br.readLine()) != null) {
	        	if (line.startsWith("Server") || line.trim().isEmpty())
	        		continue;
	        	String[] tokens = line.split(",");
	        	
//	        	float date = new SimpleDateFormat(  
//	                     "yyyy/MM/dd HH:mm:ss").parse(tokens[3]).getTime();

	        	float date = Float.parseFloat(tokens[0]);
	        	
	        	try {
	        		float value = Float.parseFloat(tokens[3]);
	        		PointItem fItem = new PointItem();
	        		fItem.x = date;
	        		fItem.y = value;
	        		points.add(fItem);
	        		
	        		List<Float> dataItem = new ArrayList<>();
	        		dataItem.add(date);
	        		dataItem.add(value);
		        	data.add(dataItem);
				} catch (Exception e) {
				}
            }
	        item.points = points;
	        item.data = data;
	        fis.close();
	    } catch (Exception e) { 
	        e.printStackTrace(); 
	    }
		
//		SeriesItem[] items = new SeriesItem[]{item};
		return item;
	}
	
	/**
	 * 加参数的加载数据，首先运行python程序跑出结果
	 * @param fileName
	 * @param pamameter
	 * @return
	 */
	public ResultItem LoadData(String fileName, String p, String ratio, String eps, String minpts, String r) {
		String outputFile = Paths.get(DataCategory, fileName + ".result").toString();
		
		File file = new File(outputFile);
		file.delete();

		String inputFile = Paths.get(DataCategory, fileName).toString();
		
		File input_file = new File(inputFile);
		
		if (! input_file.exists()){
			return null;
		}
		
		String command = String.format("python %s/command.py --input %s --output %s --per %s --ratio %s --eps %s --minpt %s --r %s", 
				PythonPath, inputFile, outputFile, p, ratio, eps, minpts, r);
		
		System.out.println(command);
		RuntimeService.RunCommand(command);
		
		while (true) {
			file = new File(outputFile);
			
			if (file.exists()){
				try {
					Thread.sleep(1500);
					break;
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		
		ResultItem resultItem = new ResultItem();
		
		resultItem.result = LoadData(fileName + ".result");
		resultItem.core = LoadCore(fileName + ".result");
		
		return resultItem;
	}
}
