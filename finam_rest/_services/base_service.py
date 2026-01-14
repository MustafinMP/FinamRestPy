class BaseService:
    _jwt_token = None
    _base_url = ''

    def __init__(self, base_url: str, account_id: str):
        self._base_url = base_url
        self._account_id = account_id

    def set_account(self, account_id: str) -> None:
        self._account_id = account_id

    def _headers(self) -> dict:
        return {"Authorization": f"{self._jwt_token}", 'Content-Type': 'application/json', 'Accept': 'application/json'}

    @classmethod
    def _set_jwt_token(cls, jwt_token: str) -> None:
        cls._jwt_token = jwt_token
