from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

NEWS_TITLE = 'Заголовок новости'
NEWS_TEXT = 'Текст новости'
COMMENTS_TEXT = 'Текст комментария'
COMMENTS_COUNT = 5
COMMENTS_SLEEP_TIME = 2

LOGIN_PATH = 'users:login'
LOGOUT_PATH = 'users:logout'
SIGNUP_PATH = 'users:signup'
HOME_PATH = 'news:home'
DETAIL_PATH = 'news:detail'
DELETE_PATH = 'news:delete'
EDIT_PATH = 'news:edit'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title=NEWS_TITLE,
        text=NEWS_TEXT
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text=COMMENTS_TEXT
    )


@pytest.fixture
def news_for_home_page():
    News.objects.bulk_create(
        News(title=NEWS_TITLE + f'{index}',
             text=NEWS_TEXT,
             date=datetime.today() - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comments_for_news(author, news):
    now = timezone.now()
    for index in range(COMMENTS_COUNT):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=COMMENTS_TEXT + f'{index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment_data():
    return {
        'text': COMMENTS_TEXT
    }


@pytest.fixture
def url_users_login():
    return reverse(LOGIN_PATH)


@pytest.fixture
def url_users_logout():
    return reverse(LOGOUT_PATH)


@pytest.fixture
def url_users_signup():
    return reverse(SIGNUP_PATH)


@pytest.fixture
def url_news_home():
    return reverse(HOME_PATH)


@pytest.fixture
def url_news_detail(news):
    return reverse(DETAIL_PATH, args=(news.id,))


@pytest.fixture
def url_comment_edit(comment):
    return reverse(EDIT_PATH, args=(comment.id,))


@pytest.fixture
def url_comment_delete(comment):
    return reverse(DELETE_PATH, args=(comment.id,))
