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
            ) -> Optional[dict]:
        full_url: str = self.__base_url.rstrip('/') + '/' + end_url.lstrip('/')
        if not isinstance(params, dict):
            logging.info(
                f'<Был передан не правильный тип данных {type(params)} для ' +
                'атрибута params, требуется dict>. Будет выполнен запрос' +
                ' без параметров')
            params = dict()
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
            return response.json()


obj = BaseAPIRequester('https://swapi.dev/api/')
print(obj.get('people/'))
