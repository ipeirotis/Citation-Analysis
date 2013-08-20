/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
/*
 * This code was generated by https://code.google.com/p/google-apis-client-generator/
 * (build: 2013-08-14 15:32:06 UTC)
 * on 2013-08-20 at 02:54:19 UTC 
 * Modify at your own risk.
 */

package com.appspot.citationanalysis.citationanalysis.model;

/**
 * Model definition for Author.
 *
 * <p> This is the Java data model class that specifies how to parse/serialize into the JSON that is
 * transmitted over HTTP when working with the . For a detailed explanation see:
 * <a href="http://code.google.com/p/google-http-java-client/wiki/JSON">http://code.google.com/p/google-http-java-client/wiki/JSON</a>
 * </p>
 *
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public final class Author extends com.google.api.client.json.GenericJson {

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private JsonMap citations;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key @com.google.api.client.json.JsonString
  private java.lang.Long citationsTimestamp;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.util.List<java.lang.String> coauthors;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key @com.google.api.client.json.JsonString
  private java.lang.Long coauthorsTimestamp;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.Integer firstYear;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private Key key;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String mathematica;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String name;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.util.List<java.lang.String> papers;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key @com.google.api.client.json.JsonString
  private java.lang.Long papersTimestamp;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String userid;

  /**
   * @return value or {@code null} for none
   */
  public JsonMap getCitations() {
    return citations;
  }

  /**
   * @param citations citations or {@code null} for none
   */
  public Author setCitations(JsonMap citations) {
    this.citations = citations;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getCitationsTimestamp() {
    return citationsTimestamp;
  }

  /**
   * @param citationsTimestamp citationsTimestamp or {@code null} for none
   */
  public Author setCitationsTimestamp(java.lang.Long citationsTimestamp) {
    this.citationsTimestamp = citationsTimestamp;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.util.List<java.lang.String> getCoauthors() {
    return coauthors;
  }

  /**
   * @param coauthors coauthors or {@code null} for none
   */
  public Author setCoauthors(java.util.List<java.lang.String> coauthors) {
    this.coauthors = coauthors;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getCoauthorsTimestamp() {
    return coauthorsTimestamp;
  }

  /**
   * @param coauthorsTimestamp coauthorsTimestamp or {@code null} for none
   */
  public Author setCoauthorsTimestamp(java.lang.Long coauthorsTimestamp) {
    this.coauthorsTimestamp = coauthorsTimestamp;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Integer getFirstYear() {
    return firstYear;
  }

  /**
   * @param firstYear firstYear or {@code null} for none
   */
  public Author setFirstYear(java.lang.Integer firstYear) {
    this.firstYear = firstYear;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public Key getKey() {
    return key;
  }

  /**
   * @param key key or {@code null} for none
   */
  public Author setKey(Key key) {
    this.key = key;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getMathematica() {
    return mathematica;
  }

  /**
   * @param mathematica mathematica or {@code null} for none
   */
  public Author setMathematica(java.lang.String mathematica) {
    this.mathematica = mathematica;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getName() {
    return name;
  }

  /**
   * @param name name or {@code null} for none
   */
  public Author setName(java.lang.String name) {
    this.name = name;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.util.List<java.lang.String> getPapers() {
    return papers;
  }

  /**
   * @param papers papers or {@code null} for none
   */
  public Author setPapers(java.util.List<java.lang.String> papers) {
    this.papers = papers;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getPapersTimestamp() {
    return papersTimestamp;
  }

  /**
   * @param papersTimestamp papersTimestamp or {@code null} for none
   */
  public Author setPapersTimestamp(java.lang.Long papersTimestamp) {
    this.papersTimestamp = papersTimestamp;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getUserid() {
    return userid;
  }

  /**
   * @param userid userid or {@code null} for none
   */
  public Author setUserid(java.lang.String userid) {
    this.userid = userid;
    return this;
  }

  @Override
  public Author set(String fieldName, Object value) {
    return (Author) super.set(fieldName, value);
  }

  @Override
  public Author clone() {
    return (Author) super.clone();
  }

}