CREATE TABLE book (
    isbn13          NUMBER(13) NOT NULL,
    book_title      VARCHAR(100),
    num_pages       INTEGER,
    date_published  DATE,
    publisher       VARCHAR(24) NOT NULL,
    language_code   VARCHAR(12) NOT NULL
);

ALTER TABLE book ADD CONSTRAINT book_pk PRIMARY KEY ( isbn13 );

CREATE TABLE bookauthor (
    isbn13       NUMBER(13) NOT NULL,
    author_name  VARCHAR(24) NOT NULL
);

ALTER TABLE bookauthor ADD CONSTRAINT bookauthor_pk PRIMARY KEY ( isbn13,
                                                                  author_name );

CREATE TABLE human (
    author_name VARCHAR(24) NOT NULL
);

ALTER TABLE human ADD CONSTRAINT human_pk PRIMARY KEY ( author_name );

CREATE TABLE language (
    language_code VARCHAR(12) NOT NULL
);

ALTER TABLE language ADD CONSTRAINT language_pk PRIMARY KEY ( language_code );

CREATE TABLE publisher (
    publisher VARCHAR(24) NOT NULL
);

ALTER TABLE publisher ADD CONSTRAINT publisher_pk PRIMARY KEY ( publisher );

CREATE TABLE review (
    isbn13          NUMBER(13) NOT NULL,
    curr_date       DATE NOT NULL,
    ratings_count   INTEGER,
    reviews_count   INTEGER,
    average_rating  FLOAT
);

ALTER TABLE review ADD CONSTRAINT review_pk PRIMARY KEY ( isbn13,
                                                          curr_date );

ALTER TABLE book
    ADD CONSTRAINT book_language_fk FOREIGN KEY ( language_code )
        REFERENCES language ( language_code );

ALTER TABLE book
    ADD CONSTRAINT book_publisher_fk FOREIGN KEY ( publisher )
        REFERENCES publisher ( publisher );

ALTER TABLE bookauthor
    ADD CONSTRAINT bookauthor_book_fk FOREIGN KEY ( isbn13 )
        REFERENCES book ( isbn13 );

ALTER TABLE bookauthor
    ADD CONSTRAINT bookauthor_human_fk FOREIGN KEY ( author_name )
        REFERENCES human ( author_name );

ALTER TABLE review
    ADD CONSTRAINT review_book_fk FOREIGN KEY ( isbn13 )
        REFERENCES book ( isbn13 );