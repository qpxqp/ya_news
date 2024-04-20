import pytest
from django.conf import settings
from pytest_lazyfixture import lazy_fixture as lf

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'parametrized_client, form_availability',
    (
        (lf('author_client'), True),
        (lf('client'), False),
    )
)
def test_pages_contains_form(
    parametrized_client, form_availability, url_news_detail
):
    response = parametrized_client.get(url_news_detail)
    assert ('form' in response.context) is form_availability
    if form_availability:
        assert isinstance(response.context['form'], CommentForm)


@pytest.mark.usefixtures('news_for_home_page')
def test_news_count_on_homepage(client, url_news_home):
    response = client.get(url_news_home)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('news_for_home_page')
def test_news_order(client, url_news_home):
    response = client.get(url_news_home)
    news_on_homepage = response.context['object_list']
    all_dates = [news.date for news in news_on_homepage]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.usefixtures('comments_for_news')
def test_comments_order(author_client, url_news_detail):
    response = author_client.get(url_news_detail)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps
