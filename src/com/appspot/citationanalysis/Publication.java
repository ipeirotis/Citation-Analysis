package com.appspot.citationanalysis;

import java.util.Map;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.IdentityType;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;

@PersistenceCapable(identityType = IdentityType.APPLICATION)
public class Publication {
	
	public static Key generateKeyFromID(String userid) {
		return KeyFactory.createKey(Publication.class.getSimpleName(), userid);
	}
	
	
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Key	key;
	
	@Persistent
	private String pubid;
	
	@Persistent
	private String title;
	
	@Persistent
	private Integer year;
	
	@Persistent
	private Long citationsTimestamp;
	@Persistent
	private Map<Integer, Double> citations;
	
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((pubid == null) ? 0 : pubid.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (!(obj instanceof Publication))
			return false;
		Publication other = (Publication) obj;
		if (pubid == null) {
			if (other.pubid != null)
				return false;
		} else if (!pubid.equals(other.pubid))
			return false;
		return true;
	}

	public Publication(String pubid) {
		this.pubid = pubid;
		this.key = Publication.generateKeyFromID(pubid);
		
		this.title = null;
		this.year = null;
		
		this.citationsTimestamp = -1L;
		this.citations = null;
		
	}

	public Key getKey() {
		return key;
	}

	public void setKey(Key key) {
		this.key = key;
	}

	public String getPubid() {
		return pubid;
	}

	public void setPubid(String pubid) {
		this.pubid = pubid;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public Integer getYear() {
		return year;
	}

	public void setYear(Integer year) {
		this.year = year;
	}

	public Long getCitationsTimestamp() {
		return citationsTimestamp;
	}

	public void setCitationsTimestamp(Long citationsTimestamp) {
		this.citationsTimestamp = citationsTimestamp;
	}

	public Map<Integer, Double> getCitations() {
		return citations;
	}

	public void setCitations(Map<Integer, Double> citations) {
		this.citations = citations;
	}
	
	
}