import pytest
from fastapi import status
from sqlalchemy import select

from src.models import sellers, books


# Тест на ручку создания продавца 
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {
        "first_name": "Seller",
        "last_name": "Seller",
        "email": "Seller@mail.ru",
        "password": "password"
    }

    response = await async_client.post("/api/v1/sellers/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data["first_name"] == data["first_name"]
    assert result_data["last_name"] == data["last_name"]
    assert result_data["email"] == data["email"]


# Тест на ручку, возвращающую продавца и список его книг
@pytest.mark.asyncio
async def test_get_seller(db_session, async_client):
    seller = sellers.Seller(first_name="Seller", last_name="Seller", email="Seller@mail.ru", password="password")

    db_session.add(seller)
    await db_session.flush()

    book = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")
    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()
    assert result_data["first_name"] == seller.first_name
    assert result_data["last_name"] == seller.last_name
    assert result_data["email"] == seller.email
    assert result_data["id"] == seller.id
    assert result_data["books"] == [
            {"id": book.id, "author": "Pushkin", "title": "Eugeny Onegin", "year": 2001, "count_pages": 104},
            {"id": book_2.id, "author": "Lermontov", "title": "Mziri", "year": 1997, "count_pages": 104}
        ]


# Тест на ручку, возвращающую список продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller = sellers.Seller(first_name="First", last_name="Seller", email="First_Seller@mail.ru", password="password")
    seller_2 = sellers.Seller(first_name="Second", last_name="Seller", email="Second_Seller@mail.ru", password="password")

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "sellers": [
            {"first_name": "Joe", "last_name": "Peachy", "email": "JoePeachy@email.com", "id": seller.id},
            {"first_name": "Eugin", "last_name": "Arrow", "email": "BabyStep@email.com", "id": seller_2.id}
        ]
    }


# Тест на ручку, обновляющую данные о продавце
@pytest.mark.asyncio
async def test_put_seller(db_session, async_client):
    seller = sellers.Seller(first_name="First", last_name="Seller", email="First_Seller@mail.ru", password="password")

    db_session.add(seller)
    await db_session.flush()

    book = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book, book_2])
    await db_session.flush()

    response = await async_client.put(f"/api/v1/sellers/{seller.id}",
                                      json={"first_name": "Second", "last_name": "Seller", "email": "Second_Seller@mail.ru"})

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(sellers.Seller, seller.id)
    assert res.id == seller.id
    assert res.first_name == "Second"
    assert res.last_name == "Seller"
    assert res.email == "Second_Seller@mail.ru"


# Тест на ручку, удаляющую данные о продавце
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = sellers.Seller(first_name="First", last_name="Seller", email="First_Seller@mail.ru", password="password")

    db_session.add(seller)
    await db_session.flush()

    book = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book, book_2])
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    # Проверка на то, что нет продавцов
    seller = await db_session.execute(select(sellers.Seller))
    res = seller.scalars().all()
    assert len(res) == 0

    # Проверка на то, что нет книг
    for book_id in [book.id, book_2.id]:
        book = await db_session.execute(select(books.Book))
        res = book.scalars().all()
        assert len(res) == 0
        