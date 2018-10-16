
# Site Info Internal Report Project
A class to get dynamic report about Articles, Authors, Logs in a ficticious site.
This project is about trainning your python db-api and sql skills against a database with over 1.5 million rows.

### Prerequisites
- You must have Python and PostgreSQL installed. 
- Tested with Python version 2.7.12.
- Tested with PostgreSQL version 9.5.14.

### Setup
First of all you must have the database installed on your machine.
To create the database and load the data do the following:
1. Enter the database command line: `psql`
2. Create a database named 'news': `create database news;`
3. Load data to the database: `psql -d news -f newsdata.sql;`

Just that!
Now the database contains 3 tables:
- authors: Info about articles authors
- articles: The articles
- log: Every time that a user access the site, this table gets an input

Now you are ready to play with the database and tables inside it using SQL or go to the next step where you are going to play with Python.

### Usage
Create an instance of Report class and call the methods:
- get_top3_articles(): to get top 3 most visited articles
- get_top3_authors(): to get top 3 authors from top 3 articles
- get_percent1_error(): to get date where errors > 1% from all views

### Example
```
report = Report()
report.get_top3_articles()
report.get_top3_authors()
report.get_percent1_error()
```

### Important Notes
- I decided to use decorators for ease of command line printing and the possibility of turn them off easily and fast by just commenting the line to be able to reuse the real methods in another purpose.

- I've created 2 views(success and failure) to facilitate the answer of get_percent1_error() method, but both are included in the main query of the method so you do not have to worry about it. =))

- But if you want, you can extract the views out of the query and install them on the database on your own.

#### Author
Tiago Mendes
<tetigo@gmail.com>

If you wanna help, let me know!
Have fun! =))

