package Servlet;
import java.io.IOException;
import java.io.OutputStream;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;

import Service.DataService;

public class DataServlet extends BaseServlet{
	/**
	 * 
	 */
	
	private static final long serialVersionUID = 1L;

	protected void doGet(HttpServletRequest request,
			HttpServletResponse response) throws  IOException {
		String file = request.getParameter("file");
		String date = request.getParameter("date");
		
		if (file != null)
		{
			DataService dataService;
			try {
				dataService = new DataService(file, date);
				Gson gson = new Gson();
				response.setHeader("content-type","text/html;charset=UTF-8");
				response.getWriter().write(gson.toJson(dataService.series));
			} catch (ParseException e) {
				e.printStackTrace();
			}
			
		}
	}
}
