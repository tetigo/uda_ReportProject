#!/usr/bin/env python2.7

import psycopg2
from functools import wraps


def header(text):
    character = '-'
    size_text = len(text)
    size_total = 60
    left = (size_total - size_text) / 2
    right = left
    if(right + left + size_text < size_total):
        right += size_total - (right + left + size_text)
    print(character * left + text + character * right)


def footer():
    print('-' * 60 + '\n')


def calc_tabs(text):
    tabs = ''
    size = len(text) / 8
    if(size >= 4):
        return '\t'
    elif(4 > size >= 3):
        return '\t\t'
    elif(3 > size >= 2):
        return '\t\t\t'
    elif(2 > size >= 1):
        return '\t\t\t\t'
    else:
        return '\t\t\t\t\t'


def body(self, col0, col1, function):
    print(col0 + calc_tabs(col0) + col1)
    for each in function(self):
        print(str(each[0]) + calc_tabs(str(each[0])) + each[1])


def tags(header0, body0, body1):
    '''
        Parameters to the decorator for it be general purpose
    '''
    def general_decorator(function):
        '''
        General decorator to display all info in a cool format on the screen
        This version is using parameters in the decorator to become general
        '''
        @wraps(function)
        # Returning info from the original method
        def wrap(self):
            header(header0)
            body(self, body0, body1, function)
            footer()
        return wrap
    return general_decorator


class Report(object):
    '''
        A class to get dynamic report about Articles, Authors, Logs
        in a ficticious site.
        Usage:
        Create an instance of Report class and call the methods:
        - get_top3_articles(): get top 3 most visited articles
        - get_top3_authors(): get top 3 authors from top 3 articles
        - get_percent1_error(percent): get date where errors > percent
           from all views
        Observation:
        I decided to use decorators for ease of command line printing and
        the possibility of turn them off easily and fast by just commenting
        the line to be able to reuse the real methods in another purpose.
    '''

    def __init__(self, dbname='news'):
        self.dbname = dbname

    @tags('Articles Info', 'Top 3 Articles Most Accessed', 'Views')
    def get_top3_articles(self):
        '''
            Get top 3 most visited articles
        '''
        try:
            conn = psycopg2.connect(dbname=self.dbname)
            cursor = conn.cursor()
            query = '''
                    select a.title, concat(count(l.path), ' views')
                    from log l
                    inner join articles a on a.slug = substring(l.path, 10)
                    group by a.slug, a.title
                    order by count(l.path) desc
                    limit 3;
                '''
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            conn.close()
            raise e
        finally:
            conn.close()
        return result if result else None

    @tags('Authors Info', 'Name', 'Views')
    def get_top3_authors(self):
        '''
            Get top 3 authors from top 3 articles
        '''
        try:
            conn = psycopg2.connect(dbname=self.dbname)
            cursor = conn.cursor()
            query = '''
                    select au.name, concat(count(l.path), ' views')
                    from log l
                    inner join articles a on a.slug = substring(l.path, 10)
                    inner join authors au on au.id = a.author
                    group by a.slug, au.name
                    order by count(l.path) desc
                    limit 3;
                '''
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            conn.close()
            raise e
        finally:
            conn.close()
        return result if result else None

    @tags('Errors Info', 'Date', 'Percent')
    def get_percent1_error(self):
        '''
            Get date where errors > 1% from all views
        '''
        try:
            conn = psycopg2.connect(dbname=self.dbname)
            cursor = conn.cursor()
            query = '''
                    create or replace view failure as
                        select date(time) date, count(status)
                        from log
                        where status not like '200%'
                        group by date(time)
                        order by date(time);

                    create or replace view success as
                        select date(time) date, count(status)
                        from log
                        where status like '200%'
                        group by date(time)
                        order by date(time);

                    select s.date,
                    concat(round(f.count / s.count::numeric, 8) * 100, ' %')
                    from success s
                    inner join failure f
                    on f.date = s.date
                    where round(f.count / s.count::numeric, 8) * 100 > 1.0
                    order by s.date;
                '''
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            conn.close()
            raise e
        finally:
            conn.close()
        return result if result else None


if __name__ == '__main__':

    report = Report()
    report.get_top3_articles()
    report.get_top3_authors()
    report.get_percent1_error()

    # print(report.get_top3_articles.__module__)
    # print(report.get_top3_articles.__name__)
    # print(report.get_top3_articles.__doc__)

    # print(report.get_top3_authors.__module__)
    # print(report.get_top3_authors.__name__)
    # print(report.get_top3_authors.__doc__)

    # print(report.get_percent1_error.__module__)
    # print(report.get_percent1_error.__name__)
    # print(report.get_percent1_error.__doc__)
