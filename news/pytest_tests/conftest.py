from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import News, Comment

NEWS_TITLE = 'Заголовок новости'
NEWS_TEXT = 'Текст новости'
COMMENTS_TEXT = 'Текст комментария'
COMMENTS_COUNT = 5
COMMENTS_SLEEP_TIME = 2


@pytest.fixture
def login_path():
    return 'users:login'


@pytest.fixture
def logout_path():
    return 'users:logout'


@pytest.fixture
def signup_path():
    return 'users:signup'


@pytest.fixture
def home_path():
    return 'news:home'


@pytest.fixture
def detail_path():
    return 'news:detail'


@pytest.fixture
def delete_path():
    return 'news:delete'


@pytest.fixture
def edit_path():
    return 'news:edit'


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
    all_news = [
        News(title=NEWS_TITLE + f'{index}',
             text=NEWS_TEXT,
             date=datetime.today() - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


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
def comment_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': COMMENTS_TEXT
    }


@pytest.fixture
def url_users_login(login_path):
    return reverse(login_path)


@pytest.fixture
def url_users_logout(logout_path):
    return reverse(logout_path)


@pytest.fixture
def url_users_signup(signup_path):
    return reverse(signup_path)


@pytest.fixture
def url_news_home(home_path):
    return reverse(home_path)


@pytest.fixture
def url_news_detail(detail_path, news):
    return reverse(detail_path, args=(news.id,))


@pytest.fixture
def url_comment_edit(edit_path, comment):
    return reverse(edit_path, args=(comment.id,))


@pytest.fixture
def url_comment_delete(delete_path, comment):
    return reverse(delete_path, args=(comment.id,))
