import scrapy
import csv
import json


class VacancySpider(scrapy.Spider):
    name = 'vacancy_spider'

    def start_requests(self):
        with open('vacancies.csv', mode='r') as f1:
            vacancies = csv.reader(f1)
            vacancies.__next__()

            for vacancy in vacancies:
                yield scrapy.Request(
                    vacancy[1],
                    meta={'region': vacancy[0]}
                )

    def parse(self, response):
        region = response.meta['region']
        base = response.request.url.split("api")[0]

        response = json.loads(response.text)['vacancies'][0]

        vacancy_id = response['id']
        vacancy_url = response["canonical_url"]
        header = response['header']

        city = response['contact']['city']['title']
        address = response['contact']['address']

        email = response['contact']['email']
        person = response['contact']['name']
        phones = ", ".join([phone['number'] for phone in response['contact']['phones']])
        company_website = response['contact']['url']

        company_id = response['company']['id']
        company_title = response['company']['title']
        company_url = base + "companies/" + str(company_id)

        categories = "\n".join([i['title'] for i in response['rubrics']])
        views = response['views']

        yield {
            "Название вакансии": header,
            "Ссылка на айтем": vacancy_url,
            "ID": vacancy_id,
            "Регион": region,
            "Город": city,
            "Категории": categories,
            "Кол-во просмотров": views,
            "ID Юзера/Компании": company_id,
            "Название/ИП": company_title,
            "Контактное лицо": person,
            "Ссылка на Юзера/Компанию": company_url,
            "Телефоны": phones,
            "Адрес": address,
            "Эмейл": email,
            "Сайт": company_website
        }
