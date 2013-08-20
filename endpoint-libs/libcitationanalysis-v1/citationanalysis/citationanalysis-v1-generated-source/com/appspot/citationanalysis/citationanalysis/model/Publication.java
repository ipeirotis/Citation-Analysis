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
 * Model definition for Publication.
 *
 * <p> This is the Java data model class that specifies how to parse/serialize into the JSON that is
 * transmitted over HTTP when working with the . For a detailed explanation see:
 * <a href="http://code.google.com/p/google-http-java-client/wiki/JSON">http://code.google.com/p/google-http-java-client/wiki/JSON</a>
 * </p>
 *
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public final class Publication extends com.google.api.client.json.GenericJson {

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
  private Key key;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String pubid;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String title;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.Integer year;

  /**
   * @return value or {@code null} for none
   */
  public JsonMap getCitations() {
    return citations;
  }

  /**
   * @param citations citations or {@code null} for none
   */
  public Publication setCitations(JsonMap citations) {
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
  public Publication setCitationsTimestamp(java.lang.Long citationsTimestamp) {
    this.citationsTimestamp = citationsTimestamp;
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
  public Publication setKey(Key key) {
    this.key = key;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getPubid() {
    return pubid;
  }

  /**
   * @param pubid pubid or {@code null} for none
   */
  public Publication setPubid(java.lang.String pubid) {
    this.pubid = pubid;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getTitle() {
    return title;
  }

  /**
   * @param title title or {@code null} for none
   */
  public Publication setTitle(java.lang.String title) {
    this.title = title;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Integer getYear() {
    return year;
  }

  /**
   * @param year year or {@code null} for none
   */
  public Publication setYear(java.lang.Integer year) {
    this.year = year;
    return this;
  }

  @Override
  public Publication set(String fieldName, Object value) {
    return (Publication) super.set(fieldName, value);
  }

  @Override
  public Publication clone() {
    return (Publication) super.clone();
  }

}