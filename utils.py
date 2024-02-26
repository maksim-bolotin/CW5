from BD.db_config import db_params
from BD.db_manager import DBManager
from BD.head_hunter import get_hh_data


def create_tables_and_insert_data():
    try:
        # Параметры подключения к базе данных PostgreSQL.
        db_manager = DBManager(**db_params)

        # Создание таблиц
        db_manager.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employers (
                employers_id SERIAL PRIMARY KEY,
                employers_name VARCHAR(255),
                description TEXT
            );
        ''')

        db_manager.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id_vacancies SERIAL PRIMARY KEY,
                title VARCHAR(255),
                salary_from VARCHAR(100),
                salary_to VARCHAR(100),
                description TEXT,
                url TEXT,
                employers_id INT REFERENCES employers(employers_id)
            );
        ''')

        # Список компаний
        companies = ['Яндекс', 'Mail.Ru Group', 'Лаборатория Касперского', 'Luxoft', 'Сбер',
                     'OCS', '3Logic Group', 'Sitronics Group', 'Rubytech', 'Cloud.ru']

        for company in companies:
            data = get_hh_data(company)

            # Проверяем, есть ли такая компания в базе данных
            db_manager.cursor.execute("SELECT employers_id FROM employers WHERE employers_name = %s;", (company,))
            existing_employer_id = db_manager.cursor.fetchone()

            # Если нет, добавляем компанию в базу
            if not existing_employer_id:
                db_manager.cursor.execute("INSERT INTO employers (employers_name) VALUES (%s) RETURNING employers_id;",
                                          (company,))
                employer_id = db_manager.cursor.fetchone()[0]
            else:
                employer_id = existing_employer_id[0]

            # Добавление вакансий в базу данных
            for vacancy in data:
                title = vacancy.get('name', '')
                description = vacancy.get('snippet', {}).get('requirement', '')
                salary_from = vacancy.get('salary', {}).get('from', '')
                salary_to = vacancy.get('salary', {}).get('to', '')
                url = vacancy.get('url', '')

                # Добавление вакансии в базу данных
                db_manager.cursor.execute("""
                    INSERT INTO vacancies (employers_id, title, salary_from, salary_to, url, description)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_vacancies;
                """, (employer_id, title, salary_from, salary_to, url, description))

        # Закрытие соединения с базой данных
        db_manager.close_connection()
    except Exception as e:
        print(f"{e}")
