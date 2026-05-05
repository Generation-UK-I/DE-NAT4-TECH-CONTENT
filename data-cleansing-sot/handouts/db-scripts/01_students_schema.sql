CREATE TABLE IF NOT EXISTS students (
    id INT NOT NULL,
    name VARCHAR(50),
    age INT,
    branch VARCHAR(50),
    start_date DATE,
    teacher VARCHAR(50),
    tel VARCHAR(20),
    PRIMARY KEY (id)
);

TRUNCATE TABLE students;
