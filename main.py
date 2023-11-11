import csv
import requests
from bs4 import BeautifulSoup


url: str = 'https://quotes.toscrape.com'


def get_html(url:str) -> str:
    html: str = requests.get(url).text
    return html


def get_list(html:str) -> BeautifulSoup:
    soup: BeautifulSoup = BeautifulSoup(html, 'lxml')
    divs: BeautifulSoup = soup.find_all('div', class_='quote')
    return divs


def save(data:dict) -> None:
    with open('file.csv', 'a') as file:
        fields: tuple = ('text', 'author', 'link')
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerow(data)


def make_titles() -> None:
    titles: dict = {
        'text': 'text',
        'author': 'author',
        'link': 'link'
    }
    save(data=titles)


def parsing(divs) -> None:
    for div in divs:
        text: str = div.find('span', class_='text').text.strip()
        author: str = div.find('small', class_='author').text.strip()
        link: str = url + div.find_all('span')[1].find('a').get('href').strip()
        data: dict = {
            'text': text,
            'author': author,
            'link': link
        }
        save(data=data)


def main() -> None:
    make_titles()
    page: int = 1
    while True:
        full_url: str = f'{url}/page/{page}/'
        html: str = get_html(url=full_url)
        divs = get_list(html=html)
        if divs:
            parsing(divs=divs)
            page += 1
        else:
            break


if __name__ == "__main__":
    main()
