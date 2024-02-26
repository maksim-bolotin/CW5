from BD.db_manager import DBManager


def main():
    try:
        # Параметры подключения к базе данных PostgreSQL.
        db_params = {'dbname': 'mydatabase', 'user': 'postgres', 'password': 'sqlUSER', 'host': 'localhost'}
        db_manager = DBManager(**db_params)

        # Меню для взаимодействия с пользователем
        while True:
            print("1. Получить список компаний и количество вакансий у каждой компании.")
            print("2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты.")
            print("3. Получить среднюю зарплату по вакансиям.")
            print("4. Получить список вакансий, у которых зарплата выше средней.")
            print("5. Получить список вакансий по ключевому слову.")
            print("0. Выход.")

            choice = input("Выберите опцию: ")
            if choice == '1':

                companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
                for company_count in companies_and_vacancies_count:
                    print(f"Компания: {company_count[0]}, Количество вакансий: {company_count[1]}")

            elif choice == '2':
                all_vacancies = db_manager.get_all_vacancies()
                for vacancy in all_vacancies:
                    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, URL: {vacancy[3]}")

            elif choice == '3':
                avg_salary = db_manager.get_avg_salary()
                print(f"Средняя зарплата по вакансиям: {avg_salary}")

            elif choice == '4':
                vacancies_higher_salary = db_manager.get_vacancies_with_higher_salary()
                for vacancy in vacancies_higher_salary:
                    print(f"Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, URL: {vacancy[3]}")

            elif choice == '5':
                keyword = input("Введите ключевое слово для поиска вакансий: ")
                vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
                for vacancy in vacancies_with_keyword:
                    print(f"Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, URL: {vacancy[3]}")

            elif choice == '0':
                break

            else:
                print("Неверный ввод. Попробуйте еще раз.")

    except Exception as e:
        print(f"{e}")
    finally:
        # Закрытие соединения с базой данных
        db_manager.close_connection()


if __name__ == "__main__":
    main()
