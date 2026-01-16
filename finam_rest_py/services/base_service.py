from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from finam_rest_py import Finam


class AsyncBaseService:
    def __init__(self, base_module: Finam):
        self._base_module = base_module

    @property
    def _session(self):
        return self._base_module._get_session()

    @property
    def _account_id(self):
        return self._base_module.get_account()
