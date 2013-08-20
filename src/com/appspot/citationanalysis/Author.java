package com.appspot.citationanalysis;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLDecoder;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.IdentityType;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;

@PersistenceCapable(identityType = IdentityType.APPLICATION)
public class Author {
	
	public static Key generateKeyFromID(String userid) {
		return KeyFactory.createKey(Author.class.getSimpleName(), userid);
	}
	
	
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Key	key;

	
	@Persistent
	private String userid;
	
	@Persistent
	private String name;
	
	@Persistent
	private Long citationsTimestamp;
	@Persistent
	private Map<Integer, Integer> citations;
	
	@Persistent
	private Long coauthorsTimestamp;
	@Persistent
	private Set<String> coauthors;
	
	@Persistent
	private Long papersTimestamp;
	@Persistent
	private Set<String> papers;
	
	@Persistent
	private String mathematica;
	
	@Persistent
	private String firstYear;
	
	
	public Key getKey() {
		return key;
	}


	public void setKey(Key key) {
		this.key = key;
	}


	public String getUserid() {
		return userid;
	}


	public void setUserid(String userid) {
		this.userid = userid;
	}


	public String getName() {
		return name;
	}


	public void setName(String name) {
		this.name = name;
	}


	public Long getCitationsTimestamp() {
		return citationsTimestamp;
	}


	public void setCitationsTimestamp(Long citationsTimestamp) {
		this.citationsTimestamp = citationsTimestamp;
	}


	public Map<Integer, Integer> getCitations() {
		return citations;
	}


	public void setCitations(Map<Integer, Integer> citations) {
		this.citations = citations;
	}


	public Long getCoauthorsTimestamp() {
		return coauthorsTimestamp;
	}


	public void setCoauthorsTimestamp(Long coauthorsTimestamp) {
		this.coauthorsTimestamp = coauthorsTimestamp;
	}


	public Set<String> getCoauthors() {
		return coauthors;
	}


	public void setCoauthors(Set<String> coauthors) {
		this.coauthors = coauthors;
	}


	public Long getPapersTimestamp() {
		return papersTimestamp;
	}


	public void setPapersTimestamp(Long papersTimestamp) {
		this.papersTimestamp = papersTimestamp;
	}


	public Set<String> getPapers() {
		return papers;
	}


	public void setPapers(Set<String> papers) {
		this.papers = papers;
	}


	public Author(String userid) {
		this.userid = userid;
		this.key = Author.generateKeyFromID(userid);
		
		this.name = null;
		
		this.citationsTimestamp = -1L;
		this.citations = null;
		
		this.coauthorsTimestamp = -1L;
		this.coauthors = null;
		
		this.papersTimestamp = -1L;
		this.papers = null;
		
		this.mathematica = null;
	}
	
	
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (!(obj instanceof Author))
			return false;
		Author other = (Author) obj;
		if (userid == null) {
			if (other.userid != null)
				return false;
		} else if (!userid.equals(other.userid))
			return false;
		return true;
	}
	
	private String extractAuthorName(Document d) {
		String result = null;
		try {
			Element nameElement = d.select("span[id=cit-name-display]").first();
			result = nameElement.html();
		} catch (Exception e) {
			;
		}
		return result;
	}


	private Set<String> extractCoauthors(Document d) {
		
		Set<String> result = new TreeSet<String>();
		
		Elements coauthors = d.select("a[href^=/citations?user=]");
		for (Element e : coauthors) {
			String coauthor = e.attr("title");
			String url = "http://scholar.google.com" + e.attr("href");
			Map<String, String> params = null;
			try {
				params = splitQuery(new URL(url));
			} catch (MalformedURLException e1) {
				e1.printStackTrace();
			}
			String userid = params.get("user");
			if (!coauthor.equals("")) {
				result.add(userid);
			}
		}
		return result;
	}
	

	private Set<String> extractPapers(Document d) {
		
		Set<String> result = new TreeSet<String>();
		
		Elements papers = d.select("a[href^=/citations?view_op=view_citation]");
		for (Element e : papers) {
			
			String url = "http://scholar.google.com" + e.attr("href");
			Map<String, String> params = null;
			try {
				params = splitQuery(new URL(url));
			} catch (MalformedURLException e1) {
				e1.printStackTrace();
			}
			String paperid = params.get("citation_for_view");
			result.add(paperid);
			
		}
		return result;
	}
	
	private Map<Integer, Integer> extractYearCitation(Document doc) {
		Map<Integer, Integer> map = new HashMap<Integer, Integer>();
		
		Element imgElement = doc.select("img[src^=http://www.google.com/chart?]").first();
		if (imgElement==null) return map;
		
		URL imgURL = null;
		try {
			imgURL = new URL(imgElement.attr("src"));
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}

		Map<String, String> params = splitQuery(imgURL);

		// Get the chd element that contains the evolution of citations over
		// time and trim the initial "t:" part
		String[] values = params.get("chd").substring(2).split(",");

		// Get the chxr element that contains the max value of citations
		// which corresponds to the 100 value in the chd
		double max = Double.parseDouble(params.get("chxr").split(",")[3]) / 100.0;

		Calendar rightNow = Calendar.getInstance();
		
		for (int i = values.length - 1; i >= 0; i--) {
			int key = rightNow.get(Calendar.YEAR) - i;
			double value = max * Double.parseDouble(values[values.length - 1 - i]);
			if (i == 0) {
				// The last variable corresponds to the current year, so it is
				// "censored". Assuming equal accumulation of citations over 
				// the year, we adjust the last variable by projecting to year end.
				double coef = rightNow.get(Calendar.DAY_OF_YEAR) / 365.0;
				value = value / coef;
			}
			map.put(key, (int)Math.round(value));
		}
		return map;
	}
	
	/**
	 * This function fetches information about the author name, citations 
	 * over the years, and list of coauthors from the start page of the author.
	 * 
	 * @throws IOException
	 */
	public void fetch() {
		
		String url = "http://scholar.google.com/citations?user="+this.userid+"&hl=en";
		try {
			Document startpage = Jsoup.connect(url).get();
			
			this.name = extractAuthorName(startpage);
			
			this.citations = extractYearCitation(startpage);
			this.citationsTimestamp = (new Date()).getTime();
			
			this.coauthors =  extractCoauthors(startpage);
			this.coauthorsTimestamp = (new Date()).getTime();
			
			this.papers =  extractPapers(startpage);
			this.papersTimestamp = (new Date()).getTime();
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((userid == null) ? 0 : userid.hashCode());
		return result;
	}
	
	public String printCitations() {
		StringBuffer sb = new StringBuffer();
		for (Integer year : new TreeSet<Integer>(this.citations.keySet())) {
			Integer value = this.citations.get(year);
			sb.append(year + " : " + Math.round(value));
			sb.append("\n");
		}
		return sb.toString();	
	}

	public String getMathematica() {
		StringBuffer sb = new StringBuffer();
		//sb.append("data = {");
		sb.append("{");
		TreeSet<Integer> years = new TreeSet<Integer>(this.citations.keySet());
		Integer firstYear = years.first();
		for (Integer year : years) {
			Integer value = this.citations.get(year);
			sb.append("{" + (year-firstYear+1) + ", " + Math.round(value) + "},");
		}
		sb.deleteCharAt(sb.length()-1);
		sb.append("}");
		//sb.append("};");
		return sb.toString();	
	}
	
	public Integer getFirstYear() {
		TreeSet<Integer> years = new TreeSet<Integer>(this.citations.keySet());
		Integer firstYear = years.first();
		return firstYear;
	}

	public String printCoauthors() {
		StringBuffer sb = new StringBuffer();
		for (String authorid : this.coauthors) {
			sb.append("Authorid: " + authorid);
			sb.append("\n");
		}
		return sb.toString();	
	}


	public String printPapers() {
		StringBuffer sb = new StringBuffer();
		for (String paperid : this.papers) {
			sb.append("Paperid: " + paperid);
			sb.append("\n");
		}
		return sb.toString();	
	}
	
	public String toString() {
		StringBuffer sb = new StringBuffer();
		sb.append("Name: "+this.name+"\n");
		sb.append("Userid: "+this.userid+"\n");
		sb.append(printCitations());
		sb.append(printCoauthors());
		sb.append(printPapers());
		return sb.toString();	
	}

	private Map<String, String> splitQuery(URL url) {
		Map<String, String> query_pairs = new LinkedHashMap<String, String>();
		String query = url.getQuery();
		String[] pairs = query.split("&");
		for (String pair : pairs) {
			int idx = pair.indexOf("=");
			try {
				query_pairs.put(URLDecoder.decode(pair.substring(0, idx), "UTF-8"),
						URLDecoder.decode(pair.substring(idx + 1), "UTF-8"));
			} catch (UnsupportedEncodingException e) {
				e.printStackTrace();
			}
		}
		return query_pairs;
	}
}