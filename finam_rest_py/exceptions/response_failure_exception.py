class FinamResponseFailureException(Exception):
    def __init__(self, status_code, reason, text):
        message = f'Ошибка запроса к Trade API ({status_code} {reason}): {text}'
        super().__init__(message)