package Servlet;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Paths;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import Servlet.Util;

import com.google.gson.Gson;

import Service.DataService;
import Service.MultiDataService;

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
		else if (kind.equals("download")) {
			String DataCategory = dataService.getDataCategory();
			String fileId = request.getParameter("fid");
			returnFile(request, response, fileId, DataCategory);
		}
		else if (kind.equals("multi")) {
			MultiDataService multiDataService = new MultiDataService(dc);
//			String fileId = request.getParameter("fid");
			response.getWriter().write(gson.toJson(multiDataService.LoadData()));
		}else if (kind.equals("ana")) {
			MultiDataService multiDataService = new MultiDataService(dc);
			String x = request.getParameter("x");
			response.getWriter().write(multiDataService.LoadAna(x));
		}
	}
	
	private boolean returnFile(HttpServletRequest request,
			HttpServletResponse response, String fileId, String DataCategory) {
		String fileName = fileId + "-result.txt";

		response.reset();
		// 设置response的Header
		response.setContentType("application/x-cortona");

		byte[] result;
		try {
			String filename = Paths.get(DataCategory, fileId + ".result").toString();
//			String filename = fileId + ".result";
			result = Util.toByteArray(filename);
			response.addHeader("Content-Disposition", "attachment;filename="
					+ fileName);
			response.addHeader("Content-Length", "" + result.length);
			OutputStream outputStream = null;
			outputStream = response.getOutputStream();
			outputStream.write(result, 0, result.length);
			outputStream.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return true;
	}
}
