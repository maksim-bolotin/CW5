from BD.db_manager import DBManager
from BD.head_hunter import get_hh_data


def create_tables_and_insert_data():
    try:
        # Параметры подключения к базе данных PostgreSQL.
        db_manager = DBManager()

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
        companies = ['Mail.Ru Group', 'Лаборатория Касперского', 'Luxoft', 'Сбер',
                     'OCS', '3Logic Group', 'Sitronics Group', 'Rubytech', 'Cloud.ru']

        for company in companies:
            data = get_hh_data(company)

            # Проверка, что данные о вакансиях получены
            if data:
                employer_id = data[0]['employer']['id']
                # Добавление компании в базу данных
                db_manager.cursor.execute("INSERT INTO employers VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                                          (employer_id, company))
                for vacancy in data:
                    id_vacancies = vacancy['id']
                    title = vacancy.get('name', '')
                    snippet = vacancy.get('snippet', {})
                    description = snippet.get('requirement', '') if snippet else ''
                    salary = vacancy.get('salary', {})
                    salary_from = salary.get('from', 0) if salary else 0
                    salary_to = salary.get('to', 0) if salary else 0
                    url = vacancy.get('alternate_url', '')

                    # Добавление вакансии в базу данных
                    db_manager.cursor.execute(
                        "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                        (id_vacancies, title, salary_from, salary_to, description, url, employer_id))
            else:
                print(f"Нет данных для компании {company}")

        # Закрытие соединения с базой данных
        db_manager.close_connection()

    except Exception as e:
        print(f"{e}")
