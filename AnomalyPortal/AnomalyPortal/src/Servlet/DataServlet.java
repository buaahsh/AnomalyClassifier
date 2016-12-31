package Servlet;

import java.io.IOException;
import java.text.ParseException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;

import Service.DataService;

public class DataServlet extends BaseServlet{
	/**
	 * 
	 */
	
	private static final long serialVersionUID = 1L;
	
	/**
	 * @param kind
	 * 	{list|data}
	 * @param dc
	 *  data category y:yahoo, t:tencent
	 * 
	 */
	protected void doGet(HttpServletRequest request,
			HttpServletResponse response) throws  IOException {
		String kind = request.getParameter("kind");
		String dc = request.getParameter("dc");
		String file = request.getParameter("file");
		String date = request.getParameter("date");
		
		if (kind.equals("list")){
			
		}
		else if (kind.equals("data")) {
			
		}
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
