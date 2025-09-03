CREATE TABLE IF NOT EXISTS STUDENT (
    ROLL_NO TEXT PRIMARY KEY,
    NAME TEXT NOT NULL,
    ADDRESS TEXT,
    PHONE TEXT,
    AGE INTEGER
);

INSERT INTO STUDENT (ROLL_NO, NAME, ADDRESS, PHONE, AGE) VALUES
('1' , 'Alice Cara', 'Rome', '*****', 20),
('2' , 'Bob Dylan', 'Milan', '*****', 22),
('3' , 'Charlie Evans', 'Naples', '*****', 19),
('4' , 'Diana Frost', 'Turin', '*****', 21),
('5' , 'Ethan Green', 'Florence', '*****', 23),
('6' , 'Christ Smith', 'Italy', '*****', 24);

SELECT * FROM STUDENT;

SELECT * FROM STUDENT WHERE AGE = 19 AND ADDRESS = 'Naples';

SELECT * FROM STUDENT WHERE AGE = 20 AND ADDRESS = 'Rome';

SELECT * FROM STUDENT WHERE AGE = 21 OR ADDRESS = 'Milan';

SELECT * FROM STUDENT WHERE AGE = 22 OR ADDRESS = 'Turin';

SELECT * FROM STUDENT WHERE AGE = 22 AND (NAME = 'Bob Dylan' OR NAME = 'Diana Frost');


