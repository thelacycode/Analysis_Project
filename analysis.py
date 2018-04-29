from flask import Flask, render_template, url_for
import psycopg2

app = Flask(__name__)

DBNAME = "news"

# HTML_WRAP = '''\
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>DB Forum</title>
#     <style>
#     </style>
#   </head>
#   <body>
#     <h1>Questions</h1>
#     <a href="{{ url_for('answer1.html') }}">{ques1}</a>
#     <a href="{{ url_for('answer2.html') }}">{{ques2}}</a>
#     <a href={{qlink3}}>{{ques3}}</a>
#
#   </body>
# </html>
# '''

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

@app.route('/answer1')
def answer1():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    ques1 = '''select title, count(path) as num 
            FROM articles 
            join log on articles.slug = (REPLACE (log.path, '/article/', '')) 
            group by title order by num desc limit 3; 
            '''
    c.execute(ques1)
    ans1 = c.fetchall()
    db.close()
    return render_template("answer1.html", ans1=ans1)

@app.route('/answer2')
def answer2():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    ques2 = '''select name, count(path) as num 
           FROM articles 
           join log on articles.slug = (REPLACE(log.path, '/article/', '')) 
           join authors on articles.author = authors.id 
           group by name order by num desc limit 5
            '''
    c.execute(ques2)
    ans2 = c.fetchall()
    db.close()
    return render_template("answer2.html", ans2=ans2)

@app.route('/answer3')
def answer3():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    ques3 = '''select errors.day, err, total, err/total as num 
                from errors
                join total_status on errors.day = total_status.day 
                where ((err/total)::decimal) > .01 
                order by day desc;
                '''
    c.execute(ques3)
    ans3 = c.fetchall()
    db.close()
    return render_template("answer3.html", ans3=ans3)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
