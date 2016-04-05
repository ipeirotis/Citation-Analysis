## Citation analysis - Data management

This is the **data management** component of the **citation analysis** project. The
component aims to allow users (1) to retrieve data from [Google Scholar]
(https://scholar.google.gr/), and (2) to manage this data.

### Locally

#### Download and install the prerequisites.

* [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
* [MySQL Community Server 5.5](http://dev.mysql.com/downloads/mysql/5.5.html#downloads)

#### Create the database.

Download [the SQL script](https://drive.google.com/open?id=0B2uT31PEHn4PajN1MmJ0TjJpeUE).

Use the `mysql` client to create a database, and execute the script.

    create database citation_analysis_db;
    use citation_analysis_db;
    source path/to/the/sql/script;

#### Install the dependencies.

	cd src
	pip install -r requirements.txt -t lib/

#### Configure.

Change **SQLALCHEMY_DATABASE_URI** in **src/config.py** to point to the database.

#### Deploy.

	cd src
	dev_appserver.py .

#### Access the application.

Go to http://localhost:8080/index.html.

### Remotely @ Google App Engine

#### Configure.

Change **SQLALCHEMY_DATABASE_URI** in **src/config.py** to point to the remote database.

**IP**: 173.194.242.182

**DATABASE**: citation_analysis_db

**USERNAME**: programize2

**PASSWORD**: scholar123!

#### Deploy.

	cd src
	appcfg.py -A citation-analysis update .

#### Access the project.

Go to https://console.developers.google.com/project/citation-analysis.

#### Access the application.

Go to https://citation-analysis.appspot.com.