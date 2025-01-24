from urllib.parse import urlparse, ParseResult
import logging
from typing import Optional
import requests


logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')


class BaseAPIRequester:
    def __init__(self, base_url: str):
        correct_url: ParseResult = urlparse(base_url)
        if correct_url.scheme == '' or correct_url.netloc == '':
            raise ValueError(f'Не корректный URL был предоставлен: {base_url}')
        self.__base_url: str = base_url

    def get(
            self,
            end_url: str = '',
            params: dict = dict()
            ) -> Optional[requests.Response]:
        full_url: str = self.__base_url.rstrip('/') + '/' + end_url.lstrip('/')
        if not isinstance(params, dict):
            logging.info(
                f'<Был передан не правильный тип данных {type(params)} для ' +
                'атрибута params, требуется dict>. Будет выполнен запрос' +
                ' без параметров')
            params = {}
        try:
            response: requests.Response = requests.get(
                full_url,
                timeout=10,
                params=params
                )
            response.raise_for_status()
        except requests.HTTPError:
            logging.error('<Произошла ошибка HTTP>')
            return None
        except requests.ConnectionError:
            logging.error('<Произошла ошибка подключения>')
            return None
        except requests.Timeout:
            logging.error('<Время ожидания запроса истекло>')
            return None
        except requests.RequestException as e:
            logging.error(
                '<При обработке вашего запроса' +
                f' возникло неоднозначное исключение: {e}>'
                )
            return None
        else:
            logging.info('<Запрос успешно выполнен>')
            return response


class SWAPIRequester(BaseAPIRequester):
    def __init__(self, base_url: str = 'https://swapi.dev/api/'):
        super().__init__(base_url)

    def get_catalog_swapi(self) -> tuple[str]:
        response: Optional[requests.Response] = self.get()
        if response is None:
            return '',
        try:
            response_json = response.json()
        except requests.JSONDecodeError:
            logging.error('<Не удалось расшифровать текст в json>')
            return '',
        else:
            logging.info('<Расшифровка прошла успешно>')
            return tuple(response_json.keys())

    def get_all_items(self, end_url: str) -> list[dict]:
        available_catalog: tuple[str] = self.get_catalog_swapi()
        all_category: list[dict] = []
        next_url: Optional[str] = end_url + '/'
        if end_url not in available_catalog:
            logging.info(
                f'<Данной категории: {available_catalog} среди доступных>'
                )
            next_url = None
        while next_url:
            response = self.get(next_url)
            if response is None:
                logging.error('<Запрос не выполнился>')
                break
            try:
                response_json = response.json()
            except requests.JSONDecodeError:
                logging.error('<Не удалось расшифровать текст в json>')
                break

            part = response_json.get('results', [])
            all_category.extend(part)

            next_link = response_json.get('next')
            if next_link:
                base_url: str = self.__base_url
                next_url = next_link.replace(base_url, '')
            else:
                next_url = None
        return all_category
