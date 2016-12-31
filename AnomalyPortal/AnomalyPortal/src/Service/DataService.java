package Service;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class DataService {
	public static String RootPath = "/home/hsh/anomaly_predict";
	
	private String DataCategory;
	
	public DataService(String dc){	
		DataCategory = Paths.get(RootPath, dc).toString(); 
		
//		ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
//		Properties properties = new Properties();
//		try {
//			properties.load(classLoader.getResourceAsStream("/parameter.properties"));'
		
	}
	
	/**
	 * 返回该数据类别下面的数据项，
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
	
	public SeriesItem[] LoadData(String fileName) {
		SeriesItem item = new SeriesItem();
		item.name = fileName;
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
		SeriesItem[] items = new SeriesItem[]{item};
		return items;
	}
	
	public class SeriesItem{
		public String name;
		public List<List<Float>> data;
	}
}