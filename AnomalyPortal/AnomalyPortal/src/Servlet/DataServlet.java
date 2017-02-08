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
		
		Gson gson = new Gson();
		response.setHeader("content-type","text/html;charset=UTF-8");
		DataService dataService = new DataService(dc);
		
		if (kind.equals("list")){
			response.getWriter().write(gson.toJson(dataService.LoadItems()));
		}
		else if (kind.equals("data")) {
			String fileId = request.getParameter("fid");
			String p = request.getParameter("p");
			String ratio = request.getParameter("ratio");
			String eps = request.getParameter("eps");
			String minpts = request.getParameter("minpts");
			String r = request.getParameter("r");
			response.getWriter().write(gson.toJson(dataService.LoadData(fileId, p, ratio, eps, minpts, r)));
		}
	}
}
