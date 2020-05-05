import cx_Oracle
import chart_studio

chart_studio.tools.set_credentials_file(username = 'buslaievvalerii', api_key = 'yyHCCCMu11YmxSgCgow7')

import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio.dashboard_objs as dashboard
import re

def fileId_from_url(url):
	raw_fileID = re.findall("~[A-z.]+/[0-9]+", url)[0][1:]
	return raw_fileID.replace('/', ':')

username = "BUSLAIEV"
password = "oracle123"
database = "localhost:1521/xe"

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

query = '''
	SELECT * FROM (
	    SELECT author_name, COUNT(isbn13) AS num_books
	    FROM publisher_book_author
	    GROUP BY author_name
	    ORDER BY num_books DESC
	) WHERE ROWNUM <= 10
'''

cursor.execute(query)

authors = []
books_author = []

for record in cursor.fetchall():
	authors.append(record[0])
	books_author.append(record[1])

bar = go.Bar(x = authors, y = books_author)
bar_scheme = py.plot([bar], filename = 'db_lab_3_1')

query = '''
	SELECT EXTRACT(YEAR FROM TO_DATE(date_published)) AS years, COUNT(isbn13) AS num_books
	FROM publisher_book_author
	GROUP BY EXTRACT(YEAR FROM TO_DATE(date_published))
	ORDER BY EXTRACT(YEAR FROM TO_DATE(date_published))
'''

cursor.execute(query)

years = []
books_year = []

for record in cursor.fetchall():
	years.append(record[0])
	books_year.append(record[1])

trace = go.Scatter(
	x= years,
	y = books_year
)

data = [trace]
plot_scheme = py.plot(data, filename = 'db_lab_3_2')

query = '''
	SELECT * FROM (
	    SELECT publisher AS publish, COUNT (isbn13) AS num_books
	    FROM publisher_book_author
	    GROUP BY publisher
	    ORDER BY num_books DESC
	) WHERE ROWNUM <= 5
'''

cursor.execute(query)

publishers = []
books_publ = []

for record in cursor.fetchall():
	publishers.append(record[0])
	books_publ.append(record[1])

pie = go.Pie(labels = publishers, values = books_publ)
pie_scheme = py.plot([pie], filename = 'db_lab_3_3')

my_board = dashboard.Dashboard()
bar_scheme_id = fileId_from_url(bar_scheme)
plot_scheme_id = fileId_from_url(plot_scheme)
pie_scheme_id = fileId_from_url(pie_scheme)

box_1 = {
	'type' : 'box',
	'boxType' : 'plot',
	'fileId' : bar_scheme_id,
	'title' : 'Запит 1'
}

box_2 = {
	'type' : 'box',
	'boxType' : 'plot',
	'fileId' : plot_scheme_id,
	'title' : 'Запит 2'
}

box_3 = {
	'type' : 'box',
	'boxType' : 'plot',
	'fileId' : pie_scheme_id,
	'title' : 'Запит 3'
}

my_board.insert(box_3)
my_board.insert(box_1, 'above', 1)
my_board.insert(box_2, 'right', 2)

py.dashboard_ops.upload(my_board, 'DB Lab 3')