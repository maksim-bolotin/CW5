from BD.db_config import db_params
from BD.db_manager import DBManager
from BD.head_hunter import get_hh_data


def create_tables_and_insert_data():
    try:
        # Параметры подключения к базе данных PostgreSQL.
        db_manager = DBManager(**db_params)

        # Создание таблиц
        db_manager.cursor.execute('''
        create table employers (
        employers_id int PRIMARY KEY,
        employers_name varchar(255) NOT NULL
        );
        ''')

        db_manager.cursor.execute('''
        create table vacancies (
        id_vacancies int primary key,
        title varchar(255),
        salary_from VARCHAR(100), 
        salary_to VARCHAR(100),
        description VARCHAR(255),
        url VARCHAR(100),
        employers_id int references employers(employers_id)
        );
        ''')

        # Список компаний
        companies = ['Яндекс', 'Mail.Ru Group', 'Лаборатория Касперского', 'Luxoft', 'Сбер',
                     'OCS', '3Logic Group', 'Sitronics Group', 'Rubytech', 'Cloud.ru']

        for company in companies:
            data = get_hh_data(company)

            employer_id = data[0]['employer']['id']
            employer_name = company

            # Добавление компании в базу данных
            db_manager.cursor.execute("INSERT INTO employers VALUES (%s, %s);",
                                      (employer_id, employer_name))

            for vacancy in data:
                id_vacancies = vacancy['id']
                title = vacancy['name']
                description = vacancy['snippet']['requirement']
                salary_from = vacancy.get('salary', {}).get('from', 0)
                salary_to = vacancy.get('salary', {}).get('to', 0)
                url = vacancy['alternate_url']

                # Добавление вакансии в базу данных
                db_manager.cursor.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s);",
                                          (id_vacancies, title, salary_from, salary_to, description, url))

        # Закрытие соединения с базой данных
        db_manager.close_connection()
    except Exception as e:
        print(f"{e}")
