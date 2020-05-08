DECLARE
	books_num INTEGER := 15;
	v_title Book.book_title%Type;

BEGIN
	-- Так як в таблиці Book наявні FOREIGN KEYS,
	-- заповнимо таблиці Publisher та Language тестовими даними
	INSERT INTO Language (language_code) VALUES ('eng');
	INSERT INTO Publisher (publisher) VALUES ('Publisher 1');

	v_title := 'Book ';

	FOR i IN 1..books_num LOOP
		INSERT INTO
			Book (isbn13, book_title, num_pages, date_published, publisher, language_code)
		VALUES
			(i, v_title||i, 100, TO_DATE('01/01/2001', 'dd/mm/yyyy'), 'Publisher 1', 'eng');
	END LOOP;
END;