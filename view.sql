CREATE OR REPLACE VIEW publisher_book_author AS
	SELECT
		Human.author_name,
		Book.isbn13,
		Book.date_published,
		Publisher.publisher
	FROM
		Book
		JOIN Publisher ON Publisher.publisher = Book.publisher
		JOIN BookAuthor ON Book.isbn13 = BookAuthor.isbn13
		JOIN Human ON BookAuthor.author_name = Human.author_name;
