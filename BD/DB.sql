-- Создание базы данных
CREATE DATABASE mydatabase;

-- Создание таблицы работодателей
create table employers (
employers_id int primary key,
employers_name varchar(255),
description TEXT);


-- Создание таблицы вакансий с ссылкой на таблицу работодателей
create table vacancies (
id_vacancies serial primary key,
title varchar(255),
salary_from VARCHAR(100),
salary_to VARCHAR(100),
description text,
url text,
employers_id int references employers(employers_id));
);
