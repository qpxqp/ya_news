from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf


URL_USERS_LOGIN = lf('url_users_login')
URL_USERS_LOGOUT = lf('url_users_logout')
URL_USERS_SIGNUP = lf('url_users_signup')
URL_NEWS_HOME = lf('url_news_home')
URL_NEWS_DETAIL = lf('url_news_detail')
URL_COMMENT_EDIT = lf('url_comment_edit')
URL_COMMENT_DELETE = lf('url_comment_delete')

CLIENT = lf('client')
AUTHOR_CLIENT = lf('author_client')
NOT_AUTHOR_CLIENT = lf('not_author_client')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (URL_USERS_LOGIN, CLIENT, HTTPStatus.OK),
        (URL_USERS_LOGOUT, CLIENT, HTTPStatus.OK),
        (URL_USERS_SIGNUP, CLIENT, HTTPStatus.OK),
        (URL_NEWS_HOME, CLIENT, HTTPStatus.OK),
        (URL_NEWS_DETAIL, CLIENT, HTTPStatus.OK),
        (URL_COMMENT_EDIT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_COMMENT_DELETE, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_COMMENT_EDIT, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_COMMENT_DELETE, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_all_users(
    reverse_url, parametrized_client, status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (URL_COMMENT_EDIT, URL_COMMENT_DELETE)
)
def test_redirect_for_anonymous_user(
    url, client, url_users_login
):
    expected_url = f'{url_users_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
