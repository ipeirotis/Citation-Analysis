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

Usage
-----

For the time being, only command-line usage is allowed.
Furthermore, the script only downloads the first three
publications, to avoid excessive downloading from Google.

```
python authorCrawler <authorID>
```

For example, to check Panagiotis G. Ipeirotis's profile on Google
Scholar, with url:

```
https://scholar.google.com/citations?user=PA9La6oAAAAJ&hl=en&oi=ao
```

type:

```
python authorCrawler PA9La6oAAAAJ
```

---

(c) [Programize.com](http://www.programize.com/)
