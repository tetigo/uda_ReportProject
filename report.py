#!/usr/bin/env python

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


def calc_spaces(text):
    size = len(text)
    position = 38 - size
    return ' ' * position


def body(self, col0, col1, function):
    print(col0 + calc_spaces(col0) + col1)
    for each in function(self):
        print(str(each[0]) + calc_spaces(str(each[0])) + str(each[1]))


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
        - get_top3_authors(): get top 3 most visited authors
        - get_percent1_error(percent): get date where errors > percent
           from all views
        Observation:
        I decided to use decorators for ease of command line printing and
        the possibility of turn them off easily and fast by just commenting
        the line to be able to reuse the real methods in another purpose.
    '''

    def __init__(self, dbname='news', views='create_views.sql'):
        self.dbname = dbname

        def create_views():
            try:
                with open(views) as file:
                    creating_views = file.read()
                with psycopg2.connect(dbname=self.dbname) as conn:
                    cursor = conn.cursor()
                    cursor.execute(creating_views)
            except Exception as e:
                raise e

        create_views()

    @tags('Articles Info', 'Top 3 Articles Most Accessed', 'Views')
    def get_top3_articles(self):
        '''
            Get top 3 most visited articles
        '''
        try:
            with psycopg2.connect(dbname=self.dbname) as conn:
                cursor = conn.cursor()
                query = '''
                        select art.title, concat(count(log.path), ' views')
                        from log
                        inner join articles art on
                        log.path = '/article/' || art.slug
                        group by art.slug, art.title
                        order by count(log.path) desc
                        limit 3;
                    '''
                cursor.execute(query)
                result = cursor.fetchall()
        except Exception as e:
            raise e

        return result if result else None

    @tags('Authors Info', 'Name', 'Views')
    def get_top3_authors(self):
        '''
            Get top 3 most visited authors
        '''
        try:
            with psycopg2.connect(dbname=self.dbname) as conn:
                cursor = conn.cursor()
                query = '''
                        select auth.name, concat(count(log.path), ' views')
                        from log
                        inner join articles art on
                        log.path = '/article/' || art.slug
                        inner join authors auth on auth.id = art.author
                        group by auth.name
                        order by count(log.path) desc
                        limit 3;
                    '''
                cursor.execute(query)
                result = cursor.fetchall()
        except Exception as e:
            raise e

        return result if result else None

    @tags('Errors Info', 'Date', 'Percent')
    def get_percent1_error(self):
        '''
            Get date where errors > 1% from all views
        '''
        try:
            with psycopg2.connect(dbname=self.dbname) as conn:
                cursor = conn.cursor()
                query = '''
                select tot.date,
                concat(round(fail.count / tot.count::numeric, 8) * 100, ' %')
                from total_access tot
                inner join failure fail
                on fail.date = tot.date
                where round(fail.count / tot.count::numeric, 8) * 100 > 1.0
                order by tot.date;
                '''
                cursor.execute(query)
                result = cursor.fetchall()
        except Exception as e:
            raise e

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
