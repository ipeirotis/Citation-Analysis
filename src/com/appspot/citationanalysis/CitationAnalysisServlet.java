package com.appspot.citationanalysis;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@SuppressWarnings("serial")
public class CitationAnalysisServlet extends HttpServlet {
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		//resp.setContentType("text/plain");
		

		String authorid = req.getParameter("authorid");

		AuthorEndpoint endpoint = new AuthorEndpoint();

		Author author = endpoint.getAuthor(authorid);
		for (String id : author.getCoauthors()) {
			endpoint.getAuthor(id);
		}
		
		String query = "NonlinearModelFit["+author.getMathematica()+",m*((p+q)^2/p)*(Exp[-(p+q)*t]/(1+(q/p)*Exp[-(p+q)*t])^2),{m,p,q},t]";
		String url = "http://api.wolframalpha.com/v2/query?input="+java.net.URLEncoder.encode(query,"UTF-8")+"&appid=VKUWRH-KH8LHER2LG&format=minput&parsetimeout=60";
		//System.out.println(url);
		//resp.getWriter().println("-------------");
		//resp.getWriter().println(url);
		//resp.getWriter().println("-------------");
		resp.sendRedirect(url);
	}

}
