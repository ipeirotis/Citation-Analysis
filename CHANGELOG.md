##### [ Version 6 ] - 05.04.2016

* Database connection pool is used.
* Authors and publications task queues are separated.
* Task queue configurations are modified.
* The out-date limit for authors is set to 60 days.
* The out-date limit for publications is set to 1 year.
* The universities are sorted based on their ID.
* An ADD CHILD button is added to each organization in the tree view. When
  the user clicks on that button, the parent of the new organization is already
  pre-populated.
* Authors are refreshed in the background.
* Publications are refreshed in the background.
* The number of authors that belong to each organization is shown in the tree
  view.
* Optimize the queries behind GET ROOT ORGANIZATIONS.

##### [ Version 5 ] - 20.03.2016

* When crawling an author page, the title, the year of publication, and the
  total citations for the author's publications are also fetched.
* Organizations list contains only root organizations (i.e. universities).
* A TREE button is added to each root organization that has children. When the
  user clicks on that button, a tree-like list with all the descendants of that
  organization (i.e. schools, departments...) appears.

##### [ Version 4 ] - 29.02.2016

* Authors are associated with an organization (instead of a university and/or
  a department).
* An author can have a website.
* A publication can have a type, a title, a year of publication, total
  citations, last retrieval date, and citations per year.
* Organization's children are clickable.
* Publications API is implemented.

##### [ Version 3 ] - 05.02.2016

* Task retry limit is set.
* UI is modified.
* If a query for an out-of-date author is made, return 200 and the out-of-date
  information, re-fetch the information about the author from Google Scholar,
  and enqueue it.
* Pagination is supported.
* Authors are sorted by name.
* Organizations are sorted by name.

##### [ Version 2 ] - 24.01.2016

* Authors UI is implemented.
* Organizations UI is implemented.
* Authors are merged.

##### [ Version 1 ] - 27.12.2015

* Authors API is implemented.
* Organizations API is implemented.