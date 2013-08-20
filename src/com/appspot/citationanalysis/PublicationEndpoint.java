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
public class PublicationEndpoint {

	/**
	 * This method lists all the entities inserted in datastore.
	 * It uses HTTP GET method and paging support.
	 *
	 * @return A CollectionResponse class containing the list of all entities
	 * persisted and a cursor to the next page.
	 */
	@SuppressWarnings({ "unchecked", "unused" })
	@ApiMethod(name = "listPublication")
	public CollectionResponse<Publication> listPublication(
			@Nullable @Named("cursor") String cursorString,
			@Nullable @Named("limit") Integer limit) {

		PersistenceManager mgr = null;
		Cursor cursor = null;
		List<Publication> execute = null;

		try {
			mgr = getPersistenceManager();
			Query query = mgr.newQuery(Publication.class);
			if (cursorString != null && cursorString != "") {
				cursor = Cursor.fromWebSafeString(cursorString);
				HashMap<String, Object> extensionMap = new HashMap<String, Object>();
				extensionMap.put(JDOCursorHelper.CURSOR_EXTENSION, cursor);
				query.setExtensions(extensionMap);
			}

			if (limit != null) {
				query.setRange(0, limit);
			}

			execute = (List<Publication>) query.execute();
			cursor = JDOCursorHelper.getCursor(execute);
			if (cursor != null)
				cursorString = cursor.toWebSafeString();

			// Tight loop for fetching all entities from datastore and accomodate
			// for lazy fetch.
			for (Publication obj : execute)
				;
		} finally {
			mgr.close();
		}

		return CollectionResponse.<Publication> builder().setItems(execute)
				.setNextPageToken(cursorString).build();
	}

	/**
	 * This method gets the entity having primary key id. It uses HTTP GET method.
	 *
	 * @param id the primary key of the java bean.
	 * @return The entity with primary key id.
	 */
	@ApiMethod(name = "getPublication")
	public Publication getPublication(@Named("id") Long id) {
		PersistenceManager mgr = getPersistenceManager();
		Publication publication = null;
		try {
			publication = mgr.getObjectById(Publication.class, id);
		} finally {
			mgr.close();
		}
		return publication;
	}

	/**
	 * This inserts a new entity into App Engine datastore. If the entity already
	 * exists in the datastore, an exception is thrown.
	 * It uses HTTP POST method.
	 *
	 * @param publication the entity to be inserted.
	 * @return The inserted entity.
	 */
	@ApiMethod(name = "insertPublication")
	public Publication insertPublication(Publication publication) {
		PersistenceManager mgr = getPersistenceManager();
		try {
			if (containsPublication(publication)) {
				throw new EntityExistsException("Object already exists");
			}
			mgr.makePersistent(publication);
		} finally {
			mgr.close();
		}
		return publication;
	}

	/**
	 * This method is used for updating an existing entity. If the entity does not
	 * exist in the datastore, an exception is thrown.
	 * It uses HTTP PUT method.
	 *
	 * @param publication the entity to be updated.
	 * @return The updated entity.
	 */
	@ApiMethod(name = "updatePublication")
	public Publication updatePublication(Publication publication) {
		PersistenceManager mgr = getPersistenceManager();
		try {
			if (!containsPublication(publication)) {
				throw new EntityNotFoundException("Object does not exist");
			}
			mgr.makePersistent(publication);
		} finally {
			mgr.close();
		}
		return publication;
	}

	/**
	 * This method removes the entity with primary key id.
	 * It uses HTTP DELETE method.
	 *
	 * @param id the primary key of the entity to be deleted.
	 */
	@ApiMethod(name = "removePublication")
	public void removePublication(@Named("id") Long id) {
		PersistenceManager mgr = getPersistenceManager();
		try {
			Publication publication = mgr.getObjectById(Publication.class, id);
			mgr.deletePersistent(publication);
		} finally {
			mgr.close();
		}
	}

	private boolean containsPublication(Publication publication) {
		PersistenceManager mgr = getPersistenceManager();
		boolean contains = true;
		try {
			mgr.getObjectById(Publication.class, publication.getKey());
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
