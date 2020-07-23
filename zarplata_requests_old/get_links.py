import csv
from requests_html import HTMLSession

with open("new_regions.csv", mode='r') as read_file, open("vacancies.csv", mode="w") as write_file:
    reader = csv.reader(read_file)
    writer = csv.writer(write_file)

    for row in reader:
        region = row[0]
        url = row[1]
        offset = 0
        vacancy_url = url.split("collapsed_vacancies")[0]

        print(url)

        while offset < 9900:

            with HTMLSession() as session:
                response = session.get(url)

            vacancies = response.json()['vacancies']

            if vacancies:
                for vacancy in vacancies:
                    try:
                        vacancy_id = vacancy['publication']['vacancy_id']
                        writer.writerow([region, vacancy_url + f'vacancies/{vacancy_id}?rubric_filter_mode=new'])
                    except BaseException as e:
                        print('error', e)
            else:
                break

            url = url.replace(f"offset={offset}", f"offset={offset + 100}")

            offset += 100
