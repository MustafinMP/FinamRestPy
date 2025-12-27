class BaseService:
    def __init__(self, jwt_token: str, account_id: str, base_url: str):
        self._account_id = account_id
        self._jwt_token = jwt_token
        self._base_url = base_url

    def set_account(self, account_id: str) -> None:
        self._account_id = account_id

    def _headers(self) -> dict:
        return {"Authorization": f"{self._jwt_token}", 'Content-Type': 'application/json', 'Accept': 'application/json'}

    def _update_jwt(self, new_jwt_token: str) -> None:
        self._jwt_token = new_jwt_token
