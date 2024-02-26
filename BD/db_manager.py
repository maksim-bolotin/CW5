import psycopg2
from BD.db_config import db_params


class DBManager:
    def __init__(self, **db_params):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(**db_params)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        try:
            query = """
                SELECT employers.employers_name, COUNT(vacancies.id_vacancies) as vacancy_count
                FROM employers
                LEFT JOIN vacancies ON employers.employers_id = vacancies.employers_id
                GROUP BY employers.employers_name;
            """
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            print("Query result:", result)
            return result
        except psycopg2.Error as e:
            print(f"Ошибка получения списка компаний и количества вакансий: {e}")
            return None

    def get_all_vacancies(self):
        # получает список всех вакансий с указанием названия компании,
        # названия вакансии и зарплаты и ссылки на вакансию.
        try:
            query = """
                SELECT employers.employers_name, vacancies.title, vacancies.salary_from, vacancies.url
                FROM employers
                INNER JOIN vacancies ON employers.employers_id = vacancies.employers_id;
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"ошибка получения списка вакансий: {e}")

    def get_avg_salary(self):
        # получает среднюю зарплату по вакансиям.
        try:
            query = """
                SELECT AVG(CAST(salary_from AS NUMERIC)) AS avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL;
            """
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except psycopg2.Error as e:
            print(f"ошибка получения средней зарплаты по вакансиям: {e}")

    def get_vacancies_with_higher_salary(self):
        # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        try:
            avg_salary = self.get_avg_salary()
            query = """
                SELECT employers.employers_name, vacancies.title, vacancies.salary_from, vacancies.url
                FROM employers
                INNER JOIN vacancies ON employers.employers_id = vacancies.employers_id
                WHERE vacancies.salary_from > {avg_salary};
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"ошибка получения списка вакансий, у которых зарплата выше средней: {e}")

    def get_vacancies_with_keyword(self, keyword):
        # получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        try:
            query = f"SELECT * FROM vacancies WHERE LOWER(title) LIKE LOWER('%{keyword}%');"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"ошибка получения списка вакансий, в названии которых содержатся переданные в метод слова: {e}")

    def close_connection(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
