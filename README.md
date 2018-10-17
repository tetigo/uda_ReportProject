
# Site Info Internal Report Project
A class to get dynamic report about Articles, Authors, Logs in a 
ficticious site.
This project is about trainning your python db-api and sql skills 
against a database with over 1.5 million rows.

### Prerequisites
- You must have Python and PostgreSQL installed. 
- Tested with Python version 2.7.12.
- Tested with PostgreSQL version 9.5.14.

### Database Setup
First of all you must have the database installed on your machine.
To create the database and load the data do the following:
1. Download the file **newsdata.zip** from the link below:
- [link](https://github.com/tetigo/uda_ReportProject/raw/master/newsdata.zip)
2. Extract the **newsdata.sql** file from the **newsdata.zip** zip file.
3. Enter the database command line: `psql`
4. Create a database named **news**: `create database news;`
5. Load data to the database: `psql -d news -f newsdata.sql;`

##### Database Setup Extra Steps:
**Follow next extra steps just if you want to play with the views.**
The program **report.py** makes use of 2 views to facilitate a query:
- **total_access**: A view with total of access in a date.
- **failure**: A view with total of incorrect access in a date.
The program itself creates both of them, but if you want to play with 
these views directly in the database you can install them with the 
following extra steps:
1. Download the file **create_views.sql** from the link below:
2. [link](XXXXX dont have the link yet XXXXXXXXX)
3. Put the downloaded file in the same directory where you have extracted
the **newsdata.sql**.
4. In the command line run: `psql -d news -f create_views.sql`

Just that!
Now the database contains 3 tables:
- **authors**: Info about articles authors
- **articles**: Info about the articles
- **log**: Every time that a user access the site, this table gets an input
If you follow the extra steps the database contains 2 views also:
- **total_access**: A view with total of access in a date.
- **failure**: A view with total of incorrect access in a date.

### Database - Example of Use:
In the command line do the following:
- Run `psql` in the command line
- Now you are in the database command line
- Run `\c news` in the command line to connect in the **news** database
- Now you see that the prompt of command line has changed to database's name
- Run `\d` to see all the tables inside this **news** database
- Run `\dv` to see all the views inside this **news** database
- Run `\d authors` to see the columns of a table, in this case **authors**
- Run `select name from authors;` to see authors' names from this table
- Run `select * from failure;` to see all the date/errors from this view
- Run `\q` to exit from PostgreSQL.
That's it! Now it's your turn. =))

Now you are ready to play with the database, tables and views inside it
using SQL or go to the next step where you are going to play with Python.

### Python Report Setup and Running
Like I've said before, you must have Python 2.7.12 installed. 
Before running the program **report.py** make sure that the file 
**create_views.sql** is in the same directory of the program.
The program creates the views automatically before using them and it looks
for the sql file to install it.
If you have both **report.py** and **create_views.sql** in the same folder
you can now test the program running the following in the command line:
`python report.py`
If everything gone ok you can now see 3 reports info on the screen.
That's it!

### Python Report Usage
The **report.py** has a main class called **Report** and 3 methods as follow:
- **get_top3_articles()**: to get top 3 most visited articles
- **get_top3_authors()**: to get top 3 most visited authors
- **get_percent1_error()**: to get date where errors > 1% from all views

### Example of Use
You can create a new Python file and import the report file like below:
Example of a new file called: **example.py**
Edit the new file just created and paste the following:
```
from report import Report

report = Report()
report.get_top3_articles()
report.get_top3_authors()
report.get_percent1_error()
```
Save the file and run it from command line doing this:
`python example.py`

If you do not want to create a new program like above you can run the 
original file *report.py* like teached above in the *Python Report Setup 
and Running* section.
Also I've decided to use decorators for ease of command line printing and 
the possibility of turn them off easily and fast by just commenting the line 
to be able to reuse the real methods in another purpose.
To do that, in the *report.py* comment the next lines using `#` in the
beginning of line just before `@` like so:
- `#@tags('Articles Info', 'Top 3 Articles Most Accessed', 'Views')`
- `#@tags('Authors Info', 'Name', 'Views')`
- `#@tags('Errors Info', 'Date', 'Percent')` 
Now alter the following lines:
```
report.get_top3_articles()
report.get_top3_authors()
report.get_percent1_error()
```
To this:
```
print(report.get_top3_articles())
print(report.get_top3_authors())
print(report.get_percent1_error())
```
Now run the program and see the results:
`python report.py`
You got lists to you use in another purpose if you want to.

### Important Notes
As I used decorators, our methods are wrapped inside it and since the 
wrapper method does not carry the name, module and docstring of the 
original method we got the attributes __name__, __doc__ and __module__ with
info of the wrapper method.
To correct this I've learned the use of **wraps** decorator that is inside
**functools** that comes with Python 2.7.
You can see its use if you look for a line with: **@wraps(function)**
Now you can see the real methods info.
To do so just uncomment (**remove #**) from the lines below and
run again the program.
```
    # print(report.get_top3_articles.__module__)
    # print(report.get_top3_articles.__name__)
    # print(report.get_top3_articles.__doc__)

    # print(report.get_top3_authors.__module__)
    # print(report.get_top3_authors.__name__)
    # print(report.get_top3_authors.__doc__)

    # print(report.get_percent1_error.__module__)
    # print(report.get_percent1_error.__name__)
    # print(report.get_percent1_error.__doc__)
```
In the command line run:
`python report.py`

That's it!

#### Author
Tiago Mendes
<tetigo@gmail.com>

If you wanna help, let me know!
Have fun! =))

