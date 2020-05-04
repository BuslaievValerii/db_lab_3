CREATE OR REPLACE VIEW publisher_book_author AS
	SELECT
		Author.author_name,
		Book.isbn13,
		Book.date_published,
		Publisher.publisher
	FROM
		Book
		JOIN Publisher ON Publisher.publisher = Book.publisher
		JOIN BookAuthor ON Book.isbn13 = BookAuthor.isbn13
		JOIN Author ON BookAuthor.author_name = Author.author_name;
