import json
import psycopg2


class DBManager:
    """
    Класс для работы с данными в БД.
    """
    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        self.cursor = self.conn.cursor()

    def insert_vacancies_from_json(self, company, json_filename):
        with open(json_filename, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)

        for vacancy in vacancies:
            title = vacancy.get('name', '')
            description = vacancy.get('description', '')
            salary_from = vacancy.get('salary_from', '')
            salary_to = vacancy.get('salary_to', '')
            url = vacancy.get('url', '')

            self.cursor.execute("SELECT employers_id FROM employers WHERE employers_name = %s;", (company,))
            employer_id = self.cursor.fetchone()
            if not employer_id:
                self.cursor.execute("INSERT INTO employers (employers_name) VALUES (%s) RETURNING employers_id;", (company,))
                employer_id = self.cursor.fetchone()[0]
            else:
                employer_id = employer_id[0]
            self.cursor.execute("""
                INSERT INTO vacancies (employers_id, title, salary_from, salary_to, url, description)
                VALUES (%s, %s, %s, %s, %s, %s);
                """, (employer_id, title, salary_from, salary_to, url, description))

    def get_companies_and_vacancies_count(self):
        # получает список всех компаний и количество вакансий у каждой компании.
        try:
            query = """
                SELECT employers.employers_name, COUNT(vacancies.id_vacancies) as vacancy_count
                FROM employers
                LEFT JOIN vacancies ON employers.employers_id = vacancies.employers_id
                GROUP BY employers.employers_name;
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"ошибка получения списка компаний и количества вакансий: {e}")

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
            query = ""
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except psycopg2.Error as e:
            print(f"ошибка получения средней зарплаты по вакансиям: {e}")

    def get_vacancies_with_higher_salary(self):
        # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        try:
            avg_salary = self.get_avg_salary()
            query = ""
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
