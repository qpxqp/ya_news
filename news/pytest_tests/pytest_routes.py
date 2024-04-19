import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from news.models import Comment

URLS = (
    (lf('home_path'), None),
    (lf('login_path'), None),
    (lf('logout_path'), None),
    (lf('signup_path'), None),
    (lf('detail_path'), lf('news')),
    (lf('edit_path'), lf('comment')),
    (lf('delete_path'), lf('comment')),
)
ONLY_COMMENTS_URLS = URLS[5:]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, comment_or_news',
    URLS
)
def test_pages_availability_for_anonymous_user(
    client, login_path, name, comment_or_news
):
    if isinstance(comment_or_news, Comment):
        login_url = reverse(login_path)
        url = reverse(name, args=(comment_or_news.id,))
        expected_url = f'{login_url}?next={url}'
        response = client.get(url)
        assertRedirects(response, expected_url)
    else:
        if comment_or_news:
            url = reverse(name, args=(comment_or_news.id,))
        else:
            url = reverse(name)

        response = client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, comment_or_news',
    URLS
)
def test_pages_availability_for_author(
    author_client, name, comment_or_news
):
    if comment_or_news:
        url = reverse(name, args=(comment_or_news.id,))
    else:
        url = reverse(name)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, comment_object',
    ONLY_COMMENTS_URLS
)
def test_pages_availability_for_not_author(
    not_author_client, name, comment_object
):
    url = reverse(name, args=(comment_object.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
