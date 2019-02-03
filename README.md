# Report Project for Udemy full stack programming

## report_project 

## The reports can be called for two functions

* Return the most viewed articles
* Return days where non 200 HTML codes are returned more than 1 percent of the time.

## The report uses the following two postgres tables that it reports against.

* The articles table

```
Column |           Type           |                       Modifiers
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

```

* The log table
```
Column |           Type           |                    Modifiers
--------+--------------------------+--------------------------------------------------
 path   | text                     |
 ip     | inet                     |
 method | text                     |
 status | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)

```

* The reports can be called as methods and could work the following way

```
vagrant@vagrant:/vagrant$ python
Python 2.7.12 (default, Nov 12 2018, 14:36:49)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import report_project
>>> cursor = report_project.returnDbCursor()
>>> top3Entries = report_project.top_3_Report(cursor)
>>>
>>> for entry in top3Entries:
...   print entry
...
Candidate is jerk, alleges rival --- 338647
Bears love berries, alleges bear --- 253801
Bad things gone, say good people --- 170098
>>>
>>>
>>> errors_over_1_percent = report_project.errors_by_dayOver1Percent(cursor)
>>> for day in errors_over_1_percent:
...   print day
...
07/17/2016 --- 2.263
>>>cursor.close()
```


* The report can be run in place with main and it outputs the following

```
vagrant@vagrant:/vagrant$ python ./report_project.py
Candidate is jerk, alleges rival --- 338647
Bears love berries, alleges bear --- 253801
Bad things gone, say good people --- 170098
07/17/2016 --- 2.263
vagrant@vagrant:/vagrant$
```
