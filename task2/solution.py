import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://ru.wikipedia.org"
START_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"


def get_page_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_animals():
    url = START_URL
    letter_counts = {}

    while url:
        print(f"Processing: {url}")
        soup = get_page_soup(url)

        # Находим все элементы животных на странице
        for li in soup.select("div.mw-category li"):
            animal = li.text.strip()
            if animal:
                first_letter = animal[0].upper()
                if 'А' <= first_letter <= 'Я':
                    letter_counts[first_letter] = letter_counts.get(first_letter, 0) + 1

        # Переход к следующей странице
        next_link = soup.select_one("a:contains('Следующая страница')")
        if next_link:
            url = BASE_URL + next_link["href"]
            time.sleep(0.5)  # чтобы не перегружать сервер
        else:
            url = None

    return letter_counts


def write_to_csv(letter_counts, filename="beasts.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["letter", "count"])
        for letter in sorted(letter_counts.keys()):
            writer.writerow([letter, letter_counts[letter]])


if __name__ == "__main__":
    counts = scrape_animals()
    write_to_csv(counts)
    print("Готово! Данные записаны в beasts.csv")
