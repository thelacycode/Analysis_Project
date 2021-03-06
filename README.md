# Analysis Project
Fullstack Nano Degree - Project 3

## Project Details
Using news database, ran postgrsql queries to find answers to 3 questions.
[newsdata.sql file link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) 

## Code
* Imports: Flask, render_template, and psycopg2
* .py file: Created method to query data set for each question and route answers to html file
* .html file: Used for loop to list answers for each specific questions

## Additional Views
CREATE VIEW errors(
            SELECT (time::DATE) as day, count(status) as err
            FROM log
            WHERE status = '404 NOT FOUND'
            Group by day;

CREATE VIEW total_status(
            SELECT (time::DATE) as day, count(status) as total
            FROM log
            Group by day;


## To run file
* Must have vagrant virtual machine installed
* Download newsdata.sql file to Analysis Project folder
* Initialize vagrant up and vagrant ssh (command prompt)
* Locate directory of Analysis_Project folder
* Enter python analysis.py
* Open brower to http://localhost:8000/questions

## Screenshoot of finished product
<img src="/Analysis_Project.png" width="400" height="275" />

Project answers text file, **Analysis_Project.txt** 

