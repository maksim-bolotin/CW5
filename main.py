from BD.db_manager import DBManager
from BD.head_hunter import get_hh_data


def main():
    # параметры подключения к базе данных PostgreSQL.
    try:
        db_params = {'dbname': 'mydatabase', 'user': 'postgres',
                     'password': 'sqlUSER', 'host': 'localhost'}
    # список компаний.
        companies = ['Яндекс', 'Mail.Ru Group', 'Лаборатория Касперского', 'Luxoft', 'Сбер',
                     'OCS', '3Logic Group', 'Sitronics Group', 'Rubytech', 'Cloud.ru']

        db_manager = DBManager(**db_params)
        for company in companies:
            data = get_hh_data(company)
            if data:
                db_manager.insert_vacancies_from_json(company, f'{company}_vacancies.json', )

        # Закрытие соединения с базой данных
        db_manager.close_connection()
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
