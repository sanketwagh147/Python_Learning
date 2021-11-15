-- CREATE TABLE students(
--     student_id SERIAL PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     homeroom_number INTEGER,
--     phone VARCHAR(20) UNIQUE NOT NULL,
--     email VARCHAR(115) UNIQUE,
--     grad_year INTEGER
-- )

-- CREATE TABLE teachers(
--     teacher_id SERIAL PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     homeroom_number INTEGER,
--     phone VARCHAR(20) UNIQUE NOT NULL,
--     email VARCHAR(115) UNIQUE,
--     department VARCHAR(45)
-- )

-- INSERT INTO students
-- (first_name,
-- last_name, 
-- homeroom_number,
-- phone,
-- grad_year)
-- VALUES 
-- ('Mark',
-- 'Watney',
-- 5,
-- '7755551234',
-- 2035);


INSERT INTO teachers(
    first_name,
    last_name, 
    homeroom_number,
    email,
    phone,
    department
)
VALUES (
    'Jonas',
    'Salk',
     5,
    'jsalk@school.org',
    '7755554321',
    'Biology'
)