import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs
from models import Drug, SessionLocal, init_db, ActiveIngredient

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
    session = SessionLocal()
    try:
        # Проверяем, существует ли уже препарат с таким URL
        drug = session.query(Drug).filter_by(url=url).first()

        if not drug:
            # Если препарат не найден, создаем новый экземпляр
            drug = Drug(url=url)
            logger.info(f"Создаем новый препарат с URL: {url}")
        else:
            logger.info(f"Препарат с URL {url} уже существует, обновляем данные.")

        # Загружаем страницу
        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info(f"Successfully fetched page: {url}")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page: {url}, error: {e}")
            return

        soup = bs(response.content, 'lxml')

        # название препарата
        try:
            drug.name = soup.find(class_="products-table-name").text.strip('\n').strip()
        except Exception as e:
            logger.warning(f"Ошибка {e} при попытке спарсить название препарата")
            return

        # Описание типа препарата и состава
        try:
            drug.description = ""
            drug_descriptions = soup.find(class_='block-content composition').find_all('p')
            for drug_desc in drug_descriptions:
                drug.description += drug_desc.text.strip() + '\n'
        except Exception as e:
            drug.description = None
            logger.warning(f"Ошибка {e} при попытке спарсить описание состава")

        # Код ATX
        try:
            drug.atx_code = soup.find(id='atc_codes').find(class_='no-underline').text.strip('\n').strip()
        except Exception as e:
            drug.atx_code = None
            logger.warning(f"Ошибка {e} при попытке спарсить код ATX")

        more_info_element = soup.find(class_='more-info')

        # Фармокологическое действие
        try:
            drug.influence = more_info_element.find(id='influence').find(class_='block-content').text.strip()
        except Exception as e:
            drug.influence = None
            logger.warning(f"Ошибка {e} при попытке спарсить фармакологическое действие")

        # Фармакокинетика
        try:
            drug.kinetics = more_info_element.find(id='kinetics').find(class_='block-content').text.strip()
        except Exception as e:
            drug.kinetics = None
            logger.warning(f"Ошибка {e} при попытке спарсить фармакокинетику")

        # Показания препарата
        try:
            drug.indication = more_info_element.find(id='indication').find(class_='block-content').text.strip()
        except Exception as e:
            drug.indication = None
            logger.warning(f"Ошибка {e} при попытке спарсить показания препарата")

        # Режим дозирования
        try:
            drug.dosage = more_info_element.find(id='dosage').find(class_='block-content').text.strip()
        except Exception as e:
            drug.dosage = None
            logger.warning(f"Ошибка {e} при попытке спарсить режим дозирования")

        # Побочное действие
        try:
            drug.side_effects = more_info_element.find(id='side_effects').find(class_='block-content').text.strip()
        except Exception as e:
            drug.side_effects = None
            logger.warning(f"Ошибка {e} при попытке спарсить побочные действия")

        # Противопоказания к применению
        try:
            drug.contra = more_info_element.find(id='contra').find(class_='block-content').text.strip()
        except Exception as e:
            drug.contra = None
            logger.warning(f"Ошибка {e} при попытке спарсить противопоказания")

        # Применение при беременности и кормлении грудью
        try:
            drug.preg_lact = more_info_element.find(id='preg_lact').find(class_='block-content').text.strip()
        except Exception as e:
            drug.preg_lact = None
            logger.warning(f"Ошибка {e} при попытке спарсить применение при беременности и кормлении грудью")

        # Применение при нарушениях функции печени
        try:
            drug.hepato = more_info_element.find(id='hepato').find(class_='block-content').text.strip()
        except Exception as e:
            drug.hepato = None
            logger.warning(f"Ошибка {e} при попытке спарсить применение при нарушениях функции печени")

        # Применение при нарушениях функции почек
        try:
            drug.renal = more_info_element.find(id='renal').find(class_='block-content').text.strip()
        except Exception as e:
            drug.renal = None
            logger.warning(f"Ошибка {e} при попытке спарсить применение при нарушениях функции почек")

        # Применение у детей
        try:
            drug.child = more_info_element.find(id='child').find(class_='block-content').text.strip()
        except Exception as e:
            drug.child = None
            logger.warning(f"Ошибка {e} при попытке спарсить применение у детей")

        # Применение у пожилых пациентов
        try:
            drug.old_use = more_info_element.find(id='old').find(class_='block-content').text.strip()
        except Exception as e:
            drug.old_use = None
            logger.warning(f"Ошибка {e} при попытке спарсить применение у пожилых пациентов")

        # Особые указания
        try:
            drug.special = more_info_element.find(id='special').find(class_='block-content').text.strip()
        except Exception as e:
            drug.special = None
            logger.warning(f"Ошибка {e} при попытке спарсить особые указания")

        # Передозировка
        try:
            drug.over_dosage = more_info_element.find(id='over_dosage').find(class_='block-content').text.strip()
        except Exception as e:
            drug.over_dosage = None
            logger.warning(f"Ошибка {e} при попытке спарсить передозировку")

        # Лекарственное взаимодействие
        try:
            drug.interaction = more_info_element.find(id='interaction').find(class_='block-content').text.strip()
        except Exception as e:
            drug.interaction = None
            logger.warning(f"Ошибка {e} при попытке спарсить лекарственное взаимодействие")

        # Условия хранения препарата
        try:
            drug.storage_conditions = more_info_element.find(id='storage_conditions').find(
                class_='block-content').text.strip()
        except Exception as e:
            drug.storage_conditions = None
            logger.warning(f"Ошибка {e} при попытке спарсить условия хранения препарата")

        # Срок годности препарата
        try:
            drug.storage_time = more_info_element.find(id='storage_time').find(class_='block-content').text.strip()
        except Exception as e:
            drug.storage_time = None
            logger.warning(f"Ошибка {e} при попытке спарсить срок годности препарата")

        # Условия реализации
        try:
            drug.pharmacy_conditions = more_info_element.find(id='pharm').find(class_='block-content').text.strip()
        except Exception as e:
            drug.pharmacy_conditions = None
            logger.warning(f"Ошибка {e} при попытке спарсить условия реализации")

        session.merge(drug)  # Используем merge, чтобы обновить или добавить, если записи не было
        session.commit()

        # Повторно извлекаем drug с его id
        drug = session.query(Drug).filter_by(url=url).first()

        # Парсим и добавляем или обновляем состав в таблице active_ingredients
        try:
            structure_table = soup.find(class_='block-content composition').find('table')
            # Удаляем старые активные компоненты, если они есть, чтобы записать новые
            session.query(ActiveIngredient).filter(ActiveIngredient.drug_id == drug.id).delete()

            for row in structure_table.find_all('tr'):
                cols = row.find_all(['td', 'th'])
                cols = [ele.text.strip() for ele in cols]

                if len(cols) > 1 and cols[0]:  # Проверяем, что есть название и дозировка
                    ingredient_name = cols[0]
                    ingredient_dosage = cols[1]

                    active_ingredient = ActiveIngredient(
                        drug_id=drug.id,
                        name=ingredient_name,
                        dosage=ingredient_dosage
                    )

                    session.add(active_ingredient)
            session.commit()

        except Exception as e:
            logger.warning(f"Ошибка {e} при попытке спарсить состав препарата")
            session.rollback()

    except Exception as e:
        logger.error(f"Ошибка {e} при обработке препарата {url}")
        session.rollback()

    finally:
        session.close()


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
        number_of_page = int(soup.find(class_="block-head").contents[1].contents[0])//100 + 2

        for i in range(1, number_of_page):
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
    init_db()
    logger.info("База данных успешно инициализирована.")
    parse_links()
    # parse_drug('https://www.vidal.ru/drugs/mezym_20_000__35446')
