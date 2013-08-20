package com.appspot.citationanalysis;

import java.util.HashMap;
import java.util.List;

import javax.annotation.Nullable;
import javax.inject.Named;
import javax.jdo.PersistenceManager;
import javax.jdo.Query;
import javax.persistence.EntityExistsException;
import javax.persistence.EntityNotFoundException;

import com.google.api.server.spi.config.Api;
import com.google.api.server.spi.config.ApiMethod;
import com.google.api.server.spi.config.ApiNamespace;
import com.google.api.server.spi.response.CollectionResponse;
import com.google.appengine.api.datastore.Cursor;
import com.google.appengine.datanucleus.query.JDOCursorHelper;

@Api(name = "citationanalysis", namespace = @ApiNamespace(ownerDomain = "appspot.com", ownerName = "appspot.com", packagePath = "citationanalysis"))
public class AuthorEndpoint {

	/**
	 * This method lists all the entities inserted in datastore.
	 * It uses HTTP GET method and paging support.
	 *
	 * @return A CollectionResponse class containing the list of all entities
	 * persisted and a cursor to the next page.
	 */
	@SuppressWarnings({ "unchecked", "unused" })
	@ApiMethod(name = "listAuthor")
	public CollectionResponse<Author> listAuthor(
			@Nullable @Named("cursor") String cursorString,
			@Nullable @Named("limit") Integer limit) {

		PersistenceManager mgr = null;
		Cursor cursor = null;
		List<Author> execute = null;

		try {
			mgr = getPersistenceManager();
			Query query = mgr.newQuery(Author.class);
			if (cursorString != null && cursorString != "") {
				cursor = Cursor.fromWebSafeString(cursorString);
				HashMap<String, Object> extensionMap = new HashMap<String, Object>();
				extensionMap.put(JDOCursorHelper.CURSOR_EXTENSION, cursor);
				query.setExtensions(extensionMap);
			}

			if (limit != null) {
				query.setRange(0, limit);
			}

			execute = (List<Author>) query.execute();
			cursor = JDOCursorHelper.getCursor(execute);
			if (cursor != null)
				cursorString = cursor.toWebSafeString();

			// Tight loop for fetching all entities from datastore and accomodate
			// for lazy fetch.
			for (Author obj : execute)
				;
		} finally {
			mgr.close();
		}

		return CollectionResponse.<Author> builder().setItems(execute)
				.setNextPageToken(cursorString).build();
	}

	/**
	 * This method gets the entity having primary key id. It uses HTTP GET method.
	 *
	 * @param id the primary key of the java bean.
	 * @return The entity with primary key id.
	 */
	@ApiMethod(name = "getAuthor", path="/author/id/{id}")
	public Author getAuthor(@Named("id") String id) {
		PersistenceManager mgr = getPersistenceManager();
		Author author = null;
		try {
			author = mgr.getObjectById(Author.class, Author.generateKeyFromID(id));
			author.getCitations();
		} catch(Exception e) {
			author = new Author(id);
			author.fetch();
			this.insertAuthor(author);
		} finally {
			mgr.close();
		}
		return author;
	}
	
	/**
	 * This method gets the entity having primary key id. It uses HTTP GET method.
	 *
	 * @param id the primary key of the java bean.
	 * @return The entity with primary key id.
	 */
	@ApiMethod(name = "fetchAuthor", path="/author/fetch/{id}")
	public Author fetchAuthor(@Named("id") String id) {
		PersistenceManager mgr = getPersistenceManager();
		Author author = null;
		try {
			author = mgr.getObjectById(Author.class, Author.generateKeyFromID(id));
			author.fetch();
			this.updateAuthor(author);
		} catch(Exception e) {
			author = new Author(id);
			author.fetch();
			this.insertAuthor(author);
		} finally {
			mgr.close();
		}
		return author;
	}
	

	/**
	 * This inserts a new entity into App Engine datastore. If the entity already
	 * exists in the datastore, an exception is thrown.
	 * It uses HTTP POST method.
	 *
	 * @param author the entity to be inserted.
	 * @return The inserted entity.
	 */
	// @ApiMethod(name = "insertAuthor")
	public Author insertAuthor(Author author) {
		PersistenceManager mgr = getPersistenceManager();
		try {
			if (containsAuthor(author)) {
				throw new EntityExistsException("Object already exists");
			}
			mgr.makePersistent(author);
		} finally {
			mgr.close();
		}
		return author;
	}

	/**
	 * This method is used for updating an existing entity. If the entity does not
	 * exist in the datastore, an exception is thrown.
	 * It uses HTTP PUT method.
	 *
	 * @param author the entity to be updated.
	 * @return The updated entity.
	 */
	// @ApiMethod(name = "updateAuthor")
	public Author updateAuthor(Author author) {
		PersistenceManager mgr = getPersistenceManager();
		try {
			if (!containsAuthor(author)) {
				throw new EntityNotFoundException("Object does not exist");
			}
			mgr.makePersistent(author);
		} finally {
			mgr.close();
		}
		return author;
	}

	/**
	 * This method removes the entity with primary key id.
	 * It uses HTTP DELETE method.
	 *
	 * @param id the primary key of the entity to be deleted.
	 */
	// @ApiMethod(name = "removeAuthor")
	public void removeAuthor(@Named("id") String id) {
		PersistenceManager mgr = getPersistenceManager();
		try {
			Author author = mgr.getObjectById(Author.class, Author.generateKeyFromID(id));
			mgr.deletePersistent(author);
		} finally {
			mgr.close();
		}
	}

	private boolean containsAuthor(Author author) {
		PersistenceManager mgr = getPersistenceManager();
		boolean contains = true;
		try {
			mgr.getObjectById(Author.class, author.getKey());
		} catch (javax.jdo.JDOObjectNotFoundException ex) {
			contains = false;
		} finally {
			mgr.close();
		}
		return contains;
	}

	private static PersistenceManager getPersistenceManager() {
		return PMF.get().getPersistenceManager();
	}

}
