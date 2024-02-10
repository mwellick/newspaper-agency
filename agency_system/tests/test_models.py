from django.contrib.auth import get_user_model
from django.test import TestCase
from agency_system.models import Topic, Redactor, Newspaper, Comment, ReplyComment


class ModelTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEquals(str(topic), topic.name)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEquals(
            str(redactor),
            f"{redactor.first_name} {redactor.last_name}"
        )

    def test_newspaper_str(self):
        topic = Topic.objects.create(
            name="test1"
        )
        news = Newspaper.objects.create(
            title="test2",
        )
        news.topic.set([topic])
        self.assertEquals(str(news), f"{news.title}")

    def test_comment_and_test_reply_comment_str(self):
        topic = Topic.objects.create(
            name="test0"
        )
        redactor = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        news_comment = Newspaper.objects.create(
            title="test2",
        )
        comment = Comment.objects.create(
            post_comment=news_comment,
            author=redactor,
            body="qwertyuio"
        )
        reply_comment = ReplyComment.objects.create(
            comment_author=comment,
            reply_author=redactor,
            reply_body="qwerty",
        )
        news_comment.topic.set([topic])
        self.assertEquals(str(comment),
                          f"{redactor} left a comment under '{news_comment.title}' article: '{comment.body}'")

        self.assertEquals(str(reply_comment), f"{redactor} replied on {comment.author} comment: "
                                              f"'{reply_comment.reply_body}'")

    def test_create_redactor(self):
        username = "test"
        password = "test123"
        first_name = "text_first"
        last_name = "test_last"
        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            bio="",
            profile_images="",
            years_of_experience=0
        )
        self.assertEquals(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEquals(redactor.first_name, first_name)
        self.assertEquals(redactor.last_name, last_name)
