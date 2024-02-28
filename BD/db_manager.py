import psycopg2
from BD.db_config import db_params


class DBManager:
    def __init__(self):
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
        try:
            query = """
                SELECT employers_name, 
                       ROUND(AVG(CAST(salary_from AS NUMERIC)), 0) AS avg_salary_from, 
                       ROUND(AVG(CAST(salary_to AS NUMERIC)), 0) AS avg_salary_to 
                FROM vacancies 
                     JOIN employers ON vacancies.employers_id = employers.employers_id
                WHERE salary_from IS NOT NULL 
                  AND salary_to IS NOT NULL
                GROUP BY employers_name 
                ORDER BY avg_salary_from DESC;
            """
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # вывод результатов
            for row in result:
                print(f"Company: {row[0]}, Avg Salary From: {row[1]}, Avg Salary To: {row[2]}")
                return row[1]
        except psycopg2.Error as e:
            print(f"Ошибка при получении средних зарплат по компаниям: {e}")

    def get_vacancies_with_higher_salary(self):
        try:
            # Получаем среднюю зарплату по всем вакансиям
            avg_salary = self.get_avg_salary()

            if avg_salary is not None:
                # Получаем список вакансий с зарплатой выше средней
                vacancies_query = """
                    SELECT employers.employers_name, vacancies.title, vacancies.salary_from, vacancies.url
                    FROM employers
                    INNER JOIN vacancies ON employers.employers_id = vacancies.employers_id
                    WHERE CAST(vacancies.salary_from AS NUMERIC) > %s
                    ORDER BY vacancies.salary_from DESC;
                """
                self.cursor.execute(vacancies_query, (avg_salary,))
                return self.cursor.fetchall()

        except psycopg2.Error as e:
            print(f"Ошибка получения списка вакансий с зарплатой выше средней: {e}")

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
