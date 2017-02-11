package Servlet;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.List;


public class Util {
	public static byte[] toByteArray(String filename) throws IOException {
		File f = new File(filename);
		if (!f.exists()) {
			throw new FileNotFoundException(filename);
		}

		ByteArrayOutputStream bos = new ByteArrayOutputStream((int) f.length());
		BufferedInputStream in = null;
		try {
			in = new BufferedInputStream(new FileInputStream(f));
			int buf_size = 1024;
			byte[] buffer = new byte[buf_size];
			int len = 0;
			while (-1 != (len = in.read(buffer, 0, buf_size))) {
				bos.write(buffer, 0, len);
			}
			return bos.toByteArray();
		} catch (IOException e) {
			e.printStackTrace();
			throw e;
		} finally {
			try {
				in.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
			bos.close();
		}
	}

	public static String readToString(String fileName) {
	        String encoding = "GBK";  
	        File file = new File(fileName);  
	        Long filelength = file.length();  
	        byte[] filecontent = new byte[filelength.intValue()];  
	        try {  
	            FileInputStream in = new FileInputStream(file);  
	            in.read(filecontent);  
	            in.close();  
	        } catch (FileNotFoundException e) {  
	            e.printStackTrace();  
	        } catch (IOException e) {  
	            e.printStackTrace();  
	        }  
	        try {  
	            return new String(filecontent, encoding);  
	        } catch (UnsupportedEncodingException e) {  
	            System.err.println("The OS does not support " + encoding);  
	            e.printStackTrace();  
	            return null;  
	        }  
	    }

	public static String recover(String str) {        
		try {
			return new String(str.getBytes("GBK"), "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}    
		return "";
	}
	
	public static String byte2str(String hexStr) {
		// String hexStr = "e68891e698afe6b58be8af95313233e696b0e5b9b4e5a5bd";
		if (hexStr == null)
			return "";
		int length = hexStr.length();
		if (length % 2 != 0) {
			System.out.println("hex error,长度必须是偶数");
		}
		byte[] bytes = new byte[length / 2];
		for (int i = 0, j = 0; i < length; i += 2, j++) {
			String elementHex = String.format("%c%c", hexStr.charAt(i),
					hexStr.charAt(i + 1));
			int value = Integer.parseInt(elementHex, 16);
//			System.out.println(elementHex + ":" + value);
			bytes[j] = (byte) (value & 0xFF);
		}
		try {
			String str = new String(bytes, "utf-8");
//			System.out.println(str);
			return str;
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		return "";
	}
	
	
	public class TableJson{
		public List<List<String>> body;
		public List<String> header; 
	}
}
