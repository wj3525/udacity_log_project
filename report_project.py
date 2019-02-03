import psycopg2
import sys


def returnDbCursor():
    """Return PY-DB cursor"""

    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        return c
    except Exception as e:
        print "Unable to connect to database."
        print e
        return None


def top_3_Report(c):
    """ Report Top 3 articles of all time"""

    c.execute('''
        SELECT
            articles.title,
            count(*)
        FROM
            log,
            articles
        WHERE
            log.path = '/article/' || articles.slug
        GROUP BY articles.title
        ORDER BY count(*) DESC
        LIMIT 3;
    ''')

    records = c.fetchall()
    try:
        return ['%s --- %s' % (record[0], record[1]) for record in records]
    except Exception as e:
        print "Did not return records."
        print e
        sys.exit(1)


def errors_by_dayOver1Percent(c):
    """Print out days where erros over 1%"""

    c.execute('''
        WITH all_requests AS (
            SELECT
                DATE(time) AS day,
                count(*) AS request_count
            FROM log
            GROUP BY DATE(time)
            ORDER BY DATE(time)
        ), bad_requests AS (
                SELECT
                    DATE(time) AS day,
                    count(*) AS request_count
                FROM log
                WHERE status != '200 OK'
                GROUP BY DATE(time)
                ORDER BY DATE(time)
        ), errors_by_day AS (
            SELECT
                all_requests.day,
                CAST(bad_requests.request_count as float) /
                CAST(all_requests.request_count as float) * 100
            AS error_percent
            FROM
                all_requests,
                bad_requests
            WHERE
                all_requests.day = bad_requests.day
        )
        SELECT * FROM errors_by_day WHERE error_percent > 1;
    ''')

    records = c.fetchall()
    try:
        returnList = []
        for record in records:
            returnList.append('%s --- %s' % (record[0].strftime('%m/%d/%Y'),
                                             round(record[1], 3)))
        return returnList

    except Exception as e:
        print "Something went wrong with the query."
        print e
        sys.exit(1)


if __name__ == '__main__':

    cur = returnDbCursor()

    if cur:
        top3Articles = top_3_Report(cur)
        for article in top3Articles:
            print article

        errors_by_dayReport = errors_by_dayOver1Percent(cur)
        for day in errors_by_dayReport:
            print day

        cur.close()
    else:
        print "Could not connect to database."
        sys.exit(1)
