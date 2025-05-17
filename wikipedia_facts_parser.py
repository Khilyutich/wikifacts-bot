import requests
from bs4 import BeautifulSoup


class WikipediaFactsParser:
    def __init__(self):
        self.archive_url = 'https://ru.wikipedia.org/wiki/Проект:Знаете_ли_вы/Архив_рубрики'
        self.facts = []
        self.current_index = -1
        self.latest_month_url = None

    def fetch_latest_month(self):
        response = requests.get(self.archive_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        year_blocks = soup.find_all('ul')[1]

        for block in year_blocks:
            links = block.find_all('a')
            if links:
                for link in reversed(links):
                    latest_month_link = link['href']
                    latest_month_title = link['title']
                    if "(страница отсутствует)" not in latest_month_title:
                        full_url = f"https://ru.wikipedia.org{latest_month_link}"
                        month_response = requests.get(full_url, timeout=10)
                        if month_response.status_code == 200:
                            self.latest_month_url = full_url
                            return

    def fetch_facts(self):
        if not self.latest_month_url:
            self.fetch_latest_month()

        response = requests.get(self.latest_month_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        fact_blocks = soup.find_all('div', {'class': 'mw-parser-output'})[0]
        lists = fact_blocks.find_all('ul')

        self.facts = []
        for lst in lists:
            for fact in lst.find_all('li'):
                if not any(char.isdigit() for char in fact.text[:5]):
                    self.facts.append(fact.text.strip())
        self.current_index = -1

    def get_next_fact(self):
        self.current_index += 1
        if self.current_index < len(self.facts):
            return self.facts[self.current_index]
        else:
            self.current_index = -1
            return "Больше фактов нет."