Scholar crawler
===============

Python scripts that crawl [Google Scholar](https://scholar.google.com/)
to harvest citation information.

Python dependencies
-------------------

- `requests` 2.6.0
- `selenium` 2.45.0
- `lxml` 3.4.2
- `pandas` 0.16.0 (for future use)

For the simple web form, used in Google App Engine:

- `Flask` 0.10.1
- `Flask-DebugToolbar` 0.10.0 (for future use)
- `flask-wtf` 0.11
- `jinja2` 2.7.3

To install all dependencies, type:

```shell
pip install -r requirements.txt -t src/lib/
```

Command-line usage
------------------

For the time being, the script only downloads the first three
publications, to avoid excessive downloading from Google.

```shell
python authorCrawler <authorID>
```

For example, to check Panagiotis G. Ipeirotis's profile on Google
Scholar, with url:

```text
https://scholar.google.com/citations?user=PA9La6oAAAAJ&hl=en&oi=ao
```

type:

```shell
python authorCrawler PA9La6oAAAAJ
```

Google App Engine
-----------------

1. Install [Google App Engine SDK](https://cloud.google.com/appengine/downloads) for Python.

2. To locally deploy the application, in this directory type:

    ```shell
    dev_appserver.py src
    ```

3. To deploy the application to the App Engine, in this directory type:

    ```shell
    appcfg.py -A citation-analysis update src
    ```

---

[Programize.com](http://www.programize.com/)
