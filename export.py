import cx_Oracle
import csv

username = "BUSLAIEV"
password = "oracle123"
database = "localhost:1521/xe"

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

tables = ['Review', 'BookAuthor', 'Human', 'Book', 'Language', 'Publisher']

for table in tables:
	with open(table+'.csv', 'w') as file:
		query = "SELECT * FROM " + table
		cursor.execute(query)
		row = cursor.fetchone()

		header = []
		for i in range(len(cursor.description)):
			column = cursor.description[i]
			header.append(column[0])

		custom_writer = csv.writer(file, delimiter = ',')
		custom_writer.writerow(header)

		while row:
			custom_writer.writerow(row)
			row = cursor.fetchone()

cursor.close()
connection.close()