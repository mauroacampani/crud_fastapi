from src.books.schemas import BookCreateModel

books_prefix = f"/api/v1/books"

def test_get_all_books(test_client, fake_book_service, fake_session):

    response = test_client.get(
        url = f"{books_prefix}"
    )

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)



def test_get_book_by_uid(test_client, test_book, fake_book_service, fake_session):

    response = test_client.get(
        url = f"{books_prefix}/{test_book.uid}"
    )

    assert fake_book_service.get_books_called_once()
    assert fake_book_service.get_books_called_once_with(test_book.uid, fake_session)



def test_create_book(test_client, fake_book_service, fake_session):
    data = {
        "title":"Test Title",
        "author" : "ad6fca94-4ebb-4040-9b32-04f6a5a80d90",
        "publisher": "Test Publications",
        "published_date":"2024-12-10",
        "language": "English",
        "page_count": 215
    }

    response = test_client.post(
        url = f"{books_prefix}/"
    )

    data_book = BookCreateModel(**data)

    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(data_book, fake_session)


def test_update_book_by_uid(test_client, fake_book_service,test_book, fake_session):
    response = test_client.put(f"{books_prefix}/{test_book.uid}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid, fake_session)



def test_get_user_book_submissions(test_client, test_book, fake_book_service, fake_session):

    response = test_client.get(
        url = f"{books_prefix}/{test_book.author}"
    )

    assert fake_book_service.get_user_book_submissions_called_once()
    assert fake_book_service.get_user_book_submissions_called_once_with(test_book.uid, fake_session)



def test_delete_book_by_uid(test_client, fake_book_service, test_book, fake_session):
    response = test_client.delete(f"{books_prefix}/{test_book.uid}")


    # Verificar que el servicio mock se llamó correctamente
    fake_book_service.delete_books.assert_called_once()
    fake_book_service.delete_books.assert_called_once_with(test_book.uid, fake_session)