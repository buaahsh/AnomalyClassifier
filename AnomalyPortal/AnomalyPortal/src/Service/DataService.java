package Service;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Dictionary;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

public class DataService {
	public SeriesItem[] series;
	public static String Path = "/home/hsh/";
	
	private String DataCategory;
	
	public DataService(String dc, String dateStr){	
		DataCategory = Path.concat(dc); 
	}
	
	/**
	 * 返回该数据类别下面的数据项，
	 * @return
	 * {id:name}
	 */
	public HashMap<String, String> LoadItems() {
		HashMap<String, String> items = new HashMap();
		
		return items;
	}
	
	public SeriesItem LoadFile(String fileName) {
		SeriesItem item = new SeriesItem();
		item.name = fileName;
		List<List<Float>> data = new ArrayList<>();
		
		try { 
	        FileInputStream fis = new FileInputStream(fileName); 
	        InputStreamReader isr = new InputStreamReader(fis, "UTF-8"); 
	        BufferedReader br = new BufferedReader(isr); 
	        String line = null;
            
	        while ((line = br.readLine()) != null) {
	        	// Filter the first line
	        	if (line.startsWith("Server") || line.trim().isEmpty())
	        		continue;
	        	String[] tokens = line.split(",");
	        	
//	        	if (tokens[2].startsWith(" "))
//	        		continue;
//	        	System.out.println(tokens[2]);
	        	
	        	float date = new SimpleDateFormat(  
	                     "yyyy/MM/dd HH:mm:ss").parse(tokens[3]).getTime();
	        	
	        	try {
	        		float value = Float.parseFloat(tokens[2]);
		        	List<Float> fItem = new ArrayList<>();
		        	fItem.add(date);
		        	fItem.add(value);
		        	
		        	data.add(fItem);
				} catch (Exception e) {
				}
	        	
            }
	        
	        item.data = data;
	        
	    } catch (Exception e) { 
	        e.printStackTrace(); 
	    }
		return item;
	}
	
	public class SeriesItem{
		public String name;
		public List<List<Float>> data;
	}
}
