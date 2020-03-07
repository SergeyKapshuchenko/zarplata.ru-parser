from requests_html import HTMLSession

import csv

from threading import Lock
from concurrent.futures import ThreadPoolExecutor

locker = Lock()


def parse_single_url(url, region):
    base = url.split("api")[0]

    with HTMLSession() as session:
        response = session.get(url).json()['vacancies'][0]

    vacancy_url = response["canonical_url"]

    address = response['contact']['address']

    email = response['contact']['email']
    person = response['contact']['name']
    phones = ", ".join([phone['number'] for phone in response['contact']['phones']])
    company_website = response['contact']['url']

    company_id = response['company']['id']
    company_title = response['company']['title']
    company_url = base + "companies/" + str(company_id)

    categories = "\n".join([i['title'] for i in response['rubrics']])

    with locker:
        with open("data.csv", mode='a') as write_file:
            fieldnames = [
                "Ссылка на айтем", "Регион", "Категории", "ID Юзера/Компании",
                "Название/ИП", "Контактное лицо", "Ссылка на Юзера/Компанию",
                "Телефоны", "Адрес", "Эмейл", "Сайт"
            ]

            writer = csv.DictWriter(write_file, delimiter=';', fieldnames=fieldnames)

            writer.writerow({
                "Ссылка на айтем": vacancy_url,
                "Регион": region,
                "Категории": categories,
                "ID Юзера/Компании": company_id,
                "Название/ИП": company_title,
                "Контактное лицо": person,
                "Ссылка на Юзера/Компанию": company_url,
                "Телефоны": phones,
                "Адрес": address,
                "Эмейл": email,
                "Сайт": company_website
            })

    print("Done for url ", url)


def parse_all():
    urls = []
    regions = []

    with open("vacancies.csv", mode='r') as read_file, open("data.csv", mode="w") as write_file:
        reader = csv.reader(read_file, delimiter=';')

        fieldnames = [
            "Ссылка на айтем", "Регион", "Категории", "ID Юзера/Компании",
            "Название/ИП", "Контактное лицо", "Ссылка на Юзера/Компанию",
            "Телефоны", "Адрес", "Эмейл", "Сайт"
        ]

        writer = csv.DictWriter(write_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            urls.append(row[1])
            regions.append(row[0])

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(parse_single_url, urls, regions)


parse_all()
