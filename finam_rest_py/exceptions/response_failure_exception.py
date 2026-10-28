class FinamResponseFailureException(Exception):
    def __init__(self, response):
        message = (f'Ошибка запроса к Trade API ({response.status_code} {response.reason_phrase}):'
                   f' {response.json()['message']}')
        super().__init__(message)