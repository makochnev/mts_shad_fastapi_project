from typing import List

from pydantic import BaseModel

from .books import ReturnedBookFromSeller

__all__ = ["IncomingSeller", "ReturnedSeller", "BaseSeller", "ReturnedSellerBooks", "ReturnedSellerWithoutPass", "ReturnedAllSellersWithoutPass"]


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


class IncomingSeller(BaseSeller):
    password: str


class ReturnedSeller(BaseSeller):
    id: int


# Класс для возврата данных продавца без пароля
class ReturnedSellerWithoutPass(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


# Класс для возврата массива объектов "Продавец" без паролей
class ReturnedAllSellersWithoutPass(BaseModel):
    sellers: List[ReturnedSellerWithoutPass]


# Класс для возврата данных продавца без пароля, но со списком книг, принадлежащих ему
class ReturnedSellerBooks(ReturnedSellerWithoutPass):
    books: List[ReturnedBookFromSeller]

