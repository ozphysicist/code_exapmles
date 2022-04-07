from typing import Dict

import asserts
import requests

from custom_logger import get_logger
from custom_service import Service as ServiceModel


class ServiceAdapter:
    def __init__(
            self,
            service: ServiceModel.Service,
    ) -> None:
        self.__service = service
        self.__log = get_logger(self.__class__.__name__)

    def api__post_process(
            self,
            *,
            taskid: str,
            success: bool = True,
    ) -> requests.Response:
        codes = (200,) if success else (400, 401)
        response = self.__service.process_post(taskid=taskid)
        self.__log.info('В результате запроса вернулся код: %s', response.status_code)
        asserts.assert_in(
            response.status_code,
            codes,
            'Некорректный код ответа. Ожидаемый: {second}, фактический: {first}',
        )
        return response

    def api__post_complete_process(
            self,
            *,
            taskid: str,
            success: bool = True,
    ) -> requests.Response:
        codes = (200,) if success else (400, 401)
        response = self.__service.process_complete_post(taskid=taskid)
        self.__log.info('В результате запроса вернулся код: %s', response.status_code)
        asserts.assert_in(
            response.status_code,
            codes,
            'Некорректный код ответа. Ожидаемый: {second}, фактический: {first}',
        )
        return response
