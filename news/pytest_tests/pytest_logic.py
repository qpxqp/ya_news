from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, comment_data, url_news_detail, url_users_login
):
    count_comments = Comment.objects.count()
    response = client.post(url_news_detail, data=comment_data)
    assertRedirects(response, f'{url_users_login}?next={url_news_detail}')
    assert Comment.objects.count() == count_comments


@pytest.mark.django_db
def test_user_can_create_comment(
    news, author_client, author, comment_data, url_news_detail
):
    count_comments = Comment.objects.count()
    response = author_client.post(url_news_detail, data=comment_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    assert Comment.objects.count() == count_comments + 1

    new_comment = Comment.objects.last()
    assert new_comment.news == news
    assert new_comment.author == author
    assert new_comment.text == comment_data['text']


def test_create_comment_with_bad_words(
    author_client, url_news_detail
):
    count_comments = Comment.objects.count()
    bad_words_data = {'text': f'{choice(BAD_WORDS)}.'}
    response = author_client.post(url_news_detail, data=bad_words_data)
    assert Comment.objects.count() == count_comments
    assertFormError(response, form='form', field='text', errors=WARNING)


def test_author_can_edit_comment(
    author_client, comment, comment_data, url_comment_edit, url_news_detail
):
    count_comments = Comment.objects.count()
    response = author_client.post(url_comment_edit, data=comment_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    assert Comment.objects.count() == count_comments
    new_comment = Comment.objects.get(pk=comment.id)
    assert new_comment.text == comment_data['text']
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news


def test_not_author_can_not_edit_comment(
    not_author_client, comment, comment_data, url_comment_edit
):
    count_comments = Comment.objects.count()
    response = not_author_client.post(url_comment_edit, data=comment_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == count_comments
    new_comment = Comment.objects.get(pk=comment.id)
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news


def test_author_can_delete_comment(
        author_client, url_comment_delete, url_news_detail
):
    count_comments = Comment.objects.count()
    response = author_client.post(url_comment_delete)
    assertRedirects(response, f'{url_news_detail}#comments')
    assert Comment.objects.count() == count_comments - 1


def test_not_author_can_not_delete_comment(
        not_author_client, url_comment_delete
):
    count_comments = Comment.objects.count()
    response = not_author_client.post(url_comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == count_comments
