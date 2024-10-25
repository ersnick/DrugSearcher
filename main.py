import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs

# Настраиваем логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем обработчики для вывода в файл и консоль
file_handler = logging.FileHandler('parse_drug.log')
console_handler = logging.StreamHandler()

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

letters = [
    'a', 'b', 'v', 'g', 'd', 'e', 'zh', 'z', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
    'f', 'h', 'ts', 'ch', 'sh', 'eh', 'yu', 'ya'
]


def parse_drug(url):
    try:
        # Загружаем страницу
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        logger.info(f"Successfully fetched page: {url}")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch page: {url}, error: {e}")

    soup = bs(response.content, 'lxml')
    drug_name = soup.find(class_="products-table-name")
    print(drug_name)


def parse_links():
    base_url = 'https://www.vidal.ru'
    for letter in letters:
        links = []
        url = base_url + "/drugs/products/p/rus-" + letter

        logger.info(f"Parsing drugs starting with letter '{letter}'")

        try:
            # Загружаем страницу
            response = requests.get(url)
            response.raise_for_status()  # Проверяем успешность запроса
            logger.info(f"Successfully fetched page: {url}")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page: {url}, error: {e}")
            continue

        # Парсим количество препаратов, чтобы получить количество страниц
        soup = bs(response.content, 'lxml')
        number_of_page = int(soup.find(class_="block-head").contents[1].contents[0])//100 + 1

        for i in range(1, 2):
            paginated_url = f"{url}?p={i}"

            try:
                # Загружаем страницу
                response = requests.get(paginated_url)
                response.raise_for_status()  # Проверяем успешность запроса
                logger.info(f"Successfully fetched page: {paginated_url}")
            except requests.RequestException as e:
                logger.error(f"Failed to fetch page: {paginated_url}, error: {e}")
                continue

            # Парсим HTML с помощью bs4
            soup = bs(response.content, 'lxml')

            # Находим все элементы с классом "no-underline"
            try:
                elements = soup.find_all(class_='products-table')[0].find_all(class_='products-table-name')
                for element in elements:
                    link = element.find_all(class_='no-underline')[0].attrs['href']
                    links += [urljoin(base_url, link)]
                logger.info(f"Found {len(elements)} links on page {i} for letter '{letter}'")
            except Exception as e:
                logger.error(f"Error parsing page {paginated_url}: {e}")
                continue

        logger.info(f"Total links found for letter '{letter}': {len(links)}")

        for link in links:
            parse_drug(link)


if __name__ == '__main__':
    parse_links()
