import json
import requests


def get_hh_data(employer_name):
    url = 'https://api.hh.ru/vacancies'
    params = {'employer_name': employer_name}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json().get('items', [])
            with open(f'{employer_name}_vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return data
    except requests.exceptions.RequestException as e:
        print(f"{e}")
    return None
