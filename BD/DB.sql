-- Создание базы данных
CREATE DATABASE mydatabase;

-- Создание таблицы работодателей
CREATE TABLE employers (
    employers_id int PRIMARY KEY,
    employers_name varchar(50) NOT NULL,
    description TEXT
);

-- Создание таблицы вакансий с ссылкой на таблицу работодателей
CREATE TABLE vacancies (
    id_vacancies int PRIMARY KEY,
    employers_id int REFERENCES employers(employers_id),
    title varchar(100) NOT NULL,
    url varchar(100) NOT NULL,
    salary_from varchar(100),
    salary_to varchar(100),
    description TEXT
);
