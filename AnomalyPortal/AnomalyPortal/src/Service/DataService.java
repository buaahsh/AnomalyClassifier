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
import Model.SeriesItem;

public class DataService {
//	public static String RootPath = "/Users/hsh/Documents/2015/AnomalyClassifier/y_out";
	
	private static String RootPath = "C:\\Users\\Shaohan\\Documents\\project\\anomaly_detection\\AnomalyClassifier\\y_out";	
	private static String PythonPath = "C:\\Users\\Shaohan\\Documents\\project\\anomaly_detection\\AnomalyClassifier\\DBSCAN4AP\\Model\\Command";
	private String DataCategory;
	
	public DataService(String dc){	
		DataCategory = Paths.get(RootPath, dc).toString(); 
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
	        		if (label > 0){
//	        			String color = "rgb(247, 163, 92)";
	        			fItem.description = "1," + label;
	        		}
	        		else {
	        			fItem.description = "0";
					}
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
	public SeriesItem LoadData(String fileName, String p, String ratio, String eps, String minpts, String r) {
		String outputFile = Paths.get(DataCategory, fileName + ".result").toString();
		String inputFile = Paths.get(DataCategory, fileName).toString();
		
		File input_file = new File(inputFile);
		
		if (! input_file.exists()){
			return null;
		}
		
		String command = String.format("python %s\\command.py --input %s --output %s --per %s --ratio %s --eps %s --minpt %s --r %s", 
				PythonPath, inputFile, outputFile, p, ratio, eps, minpts, r);
		
		System.out.println(command);
		RuntimeService.RunCommand(command);
		
		while (true) {
			File file = new File(outputFile);
			
			if (file.exists()){
				try {
					Thread.sleep(1000);
					break;
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		
		return LoadData(fileName + ".result");
	}
}
