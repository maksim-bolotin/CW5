import requests


def get_hh_data(employer_name):
    """
    Функция подключения к "api.hh.ru".
    """
    url = 'https://api.hh.ru/vacancies'
    params = {'employer_name': employer_name}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json().get('items', [])
            return data
    except requests.exceptions.RequestException as e:
        print(f"{e}")
        return None
