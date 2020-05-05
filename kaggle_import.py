import csv
import cx_Oracle

username = "BUSLAIEV"
password = "oracle123"
database = "localhost:1521/xe"

connection = cx_Oracle.connect(username, password, database)

line_num = 0
author_unique = []
publisher_unique = []
language_unique = []
book_author_dict = {"author" : ["books"]}

with open("books.csv", errors = 'ignore') as file:
	header = file.readline()
	reader = csv.reader(file)

	for row in reader:
		v_language_code = row[6]
		if (v_language_code != 'jpn' and v_language_code != 'ara' and v_language_code != 'rus' and len(v_language_code) < 13):

			v_book_title = row[1]
			v_authors = row[2].split('/')
			v_average_rating = row[3]
			v_isbn13 = row[5]
			v_num_pages = row[7]
			v_ratings_count = row[8]
			v_reviews_count = row[9]
			v_publication_date = row[10]
			if len(v_publication_date) < 10:
				new_publication_date = '01/01/'+v_publication_date[-4:]
			v_publication_date = new_publication_date
			v_publisher = row[11]

			line_num += 1
			
			cursor_publisher = connection.cursor()
			if v_publisher not in publisher_unique:
				publisher_unique.append(v_publisher)
				insert_query = '''INSERT INTO Publisher (publisher) VALUES (:publisher)'''
				cursor_publisher.execute(insert_query, publisher = v_publisher)
			cursor_publisher.close()

			cursor_language = connection.cursor()
			if v_language_code not in language_unique:
				language_unique.append(v_language_code)
				insert_query = '''INSERT INTO Language (language_code) VALUES (:language_code)'''
				cursor_language.execute(insert_query, language_code = v_language_code)
			cursor_language.close()

			cursor_book = connection.cursor()
			insert_query = '''INSERT INTO Book (isbn13, book_title, num_pages, date_published, publisher, language_code)
			VALUES (:isbn13, :book_title, :num_pages, TO_DATE(:date_published, 'mm/dd/yyyy'), :publisher, :language_code)'''
			cursor_book.execute(insert_query, isbn13 = v_isbn13, book_title = v_book_title, num_pages = int(v_num_pages), date_published = v_publication_date, publisher = v_publisher, language_code = v_language_code)
			cursor_book.close()

			for v_author in v_authors:
				cursor_author = connection.cursor()

				if v_author not in author_unique:
					author_unique.append(v_author)
					book_author_dict[v_author] = [v_isbn13]
					insert_human = '''INSERT INTO Human (author_name) VALUES (:author_name)'''
					cursor_author.execute(insert_human, author_name = v_author)
					insert_bookauthor = '''INSERT INTO BookAuthor (isbn13, author_name) VALUES (:isbn13, :author_name)'''
					cursor_author.execute(insert_bookauthor, isbn13 = v_isbn13, author_name = v_author)

				if v_isbn13 not in book_author_dict[v_author]:
					book_author_dict[v_author].append(v_isbn13)
					insert_bookauthor = '''INSERT INTO BookAuthor (isbn13, author_name) VALUES (:isbn13, :author_name)'''
					cursor_author.execute(insert_bookauthor, isbn13 = v_isbn13, author_name = v_author)
				cursor_author.close()

			cursor_review = connection.cursor()
			insert_query = '''INSERT INTO Review (isbn13, curr_date, ratings_count, reviews_count, average_rating)
			VALUES (:isbn13, TO_DATE(:curr_date, 'mm-dd-yyyy'), :ratings_count, :reviews_count, :average_rating)'''
			cursor_review.execute(insert_query, isbn13 = v_isbn13, curr_date = '05-05-2020', ratings_count = int(v_ratings_count), reviews_count = int(v_reviews_count), average_rating = float(v_average_rating))
			cursor_review.close()

connection.commit()
connection.close()
print("inserted ", line_num, " lines")
