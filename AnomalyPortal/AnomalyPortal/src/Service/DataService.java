package Service;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

public class DataService {
	public SeriesItem[] series;
	
	@SuppressWarnings("deprecation")
	public DataService(String fileName, String dateStr) throws ParseException{
		series = new SeriesItem[2]; 
				
		String path = "/home/hsh/";
		fileName = path.concat(fileName); 
		
		series[0] = LoadFile(fileName);
		series[1] = LoadFile(path.concat("test2"));
		
		// Filter the series
		
		int year = Integer.parseInt(dateStr.split("/")[0]);
		int month = Integer.parseInt(dateStr.split("/")[1]);
		
		for (SeriesItem seriesItem : series) {
			for (Iterator<List<Float>> it=seriesItem.data.iterator(); it.hasNext();) {
				List<Float> now = it.next();
				Date nowDate = new Date(now.get(0).longValue());
				
				if (nowDate.getYear() + 1900 == year && nowDate.getMonth() + 1 == month)
					continue;
				
		        it.remove(); // NOTE: Iterator's remove method, not ArrayList's, is used.
			}
		}
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
