#!/usr/bin/env python3
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

DBNAME = "news"

# create additional table views
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute(
    '''
    CREATE VIEW errors(
        SELECT(time::DATE) as day, count(status) as err
        FROM log
        WHERE status = '404 NOT FOUND'
        Group by day
    )
    ''')

c.execute(
    '''
    CREATE VIEW total_status(
        SELECT (time::DATE) as day, count(status) as total
        FROM log
        Group by day
    )
    ''')

c.commit()
db.close()


# route query pulls to localhost
@app.route('/questions')
def questions():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    ques1 = '''select title, count(path) as num
            FROM articles
            join log on articles.slug = (REPLACE (log.path, '/article/', ''))
            group by title order by num desc limit 3;
            '''
    c.execute(ques1)
    ans1 = c.fetchall()

    ques2 = '''select name, count(path) as num
            FROM articles
            join log on articles.slug = (REPLACE(log.path, '/article/', ''))
            join authors on articles.author = authors.id
            group by name order by num desc limit 5
                '''
    c.execute(ques2)
    ans2 = c.fetchall()

    ques3 = '''select errors.day, err, total, err/total as num
            from errors
            join total_status on errors.day = total_status.day
            where ((err/total)::decimal) > .01
            order by day desc;
                    '''
    c.execute(ques3)
    ans3 = c.fetchall()

    return render_template("questions.html", ans1=ans1, ans2=ans2,
                           ans3=ans3)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
