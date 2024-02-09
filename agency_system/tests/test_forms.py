from django.contrib.auth import get_user_model
from django.test import TestCase

from agency_system.forms import (RedactorCreationForm,
                                 RedactorEditForm,
                                 PasswordChangingForm,
                                 CommentForm,
                                 ReplyCommentForm,
                                 TopicSearchForm,
                                 RedactorSearchForm,
                                 NewspaperSearchForm)
from agency_system.models import Comment, Newspaper, Topic


class FormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test2"
        )
        self.topic = Topic.objects.create(
            name="Test topic"
        )
        self.news = Newspaper.objects.create(
            title="Qwerty",
            content="test_content",
            published_date="Jan. 9, 2024, 12:02 p.m.",
            news_images=""
        )
        self.news.topic.add(self.topic)
        self.comment = Comment.objects.create(author=self.user, body="test comment", post_comment=self.news)
        self.reply_user = get_user_model().objects.create_user(
            username="test2",
            password="testpsw4"
        )

    def test_redactor_creation_form_is_valid(self):
        form_data = {
            "username": "testuser123",
            "first_name": "name",
            "last_name": "surname",
            "email": "test_email@example.com",
            "years_of_experience": 0,
            "password1": "testpsw1",
            "password2": "testpsw1",

        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_redactor_edit_form_is_valid(self):
        form_data = {
            "username": "testuser123",
            "profile_image": "",
            "first_name": "name",
            "last_name": "surname",
            "email": "test_email@example.com",
            "years_of_experience": 0,
            "password1": "testpsw1",
            "password2": "testpsw1",

        }
        form = RedactorEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_password_changing_form(self):
        form_data = {
            "old_password": "test2",
            "new_password1": "testpsw2",
            "new_password2": "testpsw2"
        }
        form = PasswordChangingForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_comment_form(self):
        form_data = {
            "body": "qwertyui"
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_comment_associated_with_newspaper(self):
        form_data = {
            "body": "qwertyui"
        }
        form = CommentForm(data=form_data)
        comment = form.save(commit=False)
        comment.post_comment = self.news
        comment.save()
        self.assertEqual(comment.post_comment, self.news)

    def test_reply_comment_form(self):
        form_data = {
            "reply_body": "test_reply"
        }
        form = ReplyCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_reply_associated_with_comment(self):
        form_data = {
            "reply_body": "test_reply"

        }
        form = ReplyCommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        reply_comment = form.save(commit=False)
        reply_comment.reply_author = self.reply_user
        reply_comment.comment_author = self.comment
        reply_comment.save()
        self.assertEqual(reply_comment.comment_author, self.comment)

    def test_topic_search_form(self):
        form_data = {
            "name": "search_topic"
        }
        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_search_form(self):
        form_data = {
            "username": "search_user"
        }
        form = RedactorSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_news_search_form(self):
        form_data = {
            "title": "search_title"
        }
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
