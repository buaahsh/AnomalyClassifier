package Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.nio.file.Paths;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

import Model.Dot;
import Model.PointItem;
import Model.ResultItem;
import Model.Series;
import Model.SeriesItem;

public class MultiDataService {
	public static String RootPath = "/Users/hsh/Documents/2015/AnomalyClassifier/y_out";
	private static String PythonPath = "/Users/hsh/Documents/2015/AnomalyClassifier/DBSCAN4AP/Model";
	
//	private static String RootPath = "C:\\Users\\Shaohan\\Documents\\project\\anomaly_detection\\AnomalyClassifier\\y_out";	
//	private static String PythonPath = "C:\\Users\\Shaohan\\Documents\\project\\anomaly_detection\\AnomalyClassifier\\DBSCAN4AP\\Model";
	private String DataCategory;
	
	public MultiDataService(String dc){	
		DataCategory = Paths.get(RootPath, dc).toString(); 
	}
	
	public String getDataCategory() {
		return this.DataCategory;
	}
	
	public Series[] LoadData(int labelIdx)
	{
		String fileName = Paths.get(DataCategory, "all.data").toString();
		try {
			return LoadCore(fileName, labelIdx);
		} catch (NumberFormatException | IOException | ParseException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public Series[] LoadCore(String fileName, int labelIdx) throws NumberFormatException, IOException, ParseException {
        int num = 13;
        if(labelIdx < num)
        	num = 8;
        
        FileInputStream fis = new FileInputStream(fileName);
        InputStreamReader isr = new InputStreamReader(fis, "UTF-8"); 
        BufferedReader br = new BufferedReader(isr); 
        String line = br.readLine();
        String[] names = line.split(",");
        Series[] items = new Series[num];
        
        for (int i = 0; i < num; i++) {
        	Series item = new Series();		
    		List<Dot> data = new ArrayList<Dot>();//数据
            item.name = names[i + 1];
            item.data = data;
            items[i] = item;
        }
        
        int j = 0; 
        while ((line = br.readLine()) != null) {
        	j += 1;
        	if(num != 8)
        	{
        		if(j % 10 != 0)
        			continue;
        	}
        		
        	// Filter the first line
        	if (line.startsWith("Server") || line.trim().isEmpty())
        		continue;
        	String[] tokens = line.split(",");
        	
        	float x = Float.parseFloat(tokens[0]);
        	
        	for (int i = 0; i < num; i++) {
        		String color = new String();
        		float y = Float.parseFloat(tokens[i + 1]);
        		float l = Float.parseFloat(tokens[labelIdx]);
        		
        		float label = Float.parseFloat(tokens[num + 1]);
            	if(label == 2){//是否对异常数据进行标记
            		color = "#FF3030";//红色
            	}
            	else if(l != 0){
                    color = "#FFB300";
           	}
            	
            	items[i].data.add(new Dot(color, x, y));   
			}
        	     	
        }
        br.close();   
		return items;
	}
	
	public String LoadAna(String x){
		String fileName = Paths.get(DataCategory, "all.data.ana").toString();
		FileInputStream fis;
		try {
			fis = new FileInputStream(fileName);
			InputStreamReader isr = new InputStreamReader(fis, "UTF-8"); 
	        BufferedReader br = new BufferedReader(isr); 
	        String line = null;
	        while ((line = br.readLine()) != null) {
	        	String[] tokens = line.split("\t");
	        	if (tokens[0].equals(x))
	        		return tokens[1];
	        }
		} catch (IOException e) {
			e.printStackTrace();
		}
        return "";
	}
}
