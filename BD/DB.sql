-- Создание базы данных
CREATE DATABASE mydatabase;

-- Создание таблицы работодателей
create table employers (
        employers_id int PRIMARY KEY,
        employers_name varchar(255) NOT NULL
        );

-- Создание таблицы вакансий с ссылкой на таблицу работодателей
create table vacancies (
        id_vacancies int primary key,
        title varchar(255),
        salary_from VARCHAR(100),
        salary_to VARCHAR(100),
        description VARCHAR(255),
        url VARCHAR(100),
        employers_id int references employers(employers_id)
        );
