from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from agency_system.models import Topic, Redactor, Newspaper, Comment, ReplyComment

# URLs for managing topics
TOPIC_LIST_URL = reverse("agency_system:topic-list")
TOPIC_DETAIL_URL = "agency_system:topic-detail"
TOPIC_CREATE_URL = reverse("agency_system:topic-create")
TOPIC_UPDATE_URL = "agency_system:topic-update"
TOPIC_DELETE_URL = "agency_system:topic-delete"

# URLs for managing redactors
REDACTOR_LIST_URL = reverse("agency_system:redactor-list")
REDACTOR_DETAIL_URL = "agency_system:redactor-detail"
REDACTOR_CREATE_URL = reverse("agency_system:redactor-create")
REDACTOR_UPDATE_URL = "agency_system:redactor-update"
REDACTOR_DELETE_URL = "agency_system:redactor-delete"

# URLs for managing newspapers
NEWSPAPER_LIST_URL = reverse("agency_system:newspaper-list")
NEWSPAPER_DETAIL_URL = "agency_system:newspaper-detail"
NEWSPAPER_CREATE_URL = reverse("agency_system:newspaper-create")
NEWSPAPER_UPDATE_URL = "agency_system:newspaper-update"
NEWSPAPER_DELETE_URL = "agency_system:newspaper-delete"

# URLs for managing comments
COMMENT_URL = "agency_system:newspaper-detail"
COMMENT_CREATE_URL = "agency_system:comment-create"
COMMENT_UPDATE_URL = "agency_system:comment-update"
COMMENT_DELETE_URL = "agency_system:comment-delete"

# URLs for managing replies for comments
COMMENT_AND_REPLIES_DETAIL = "agency_system:comment-and-replies"
REPLY_COMMENT_CREATE_URL = "agency_system:reply-comment-create"
REPLY_COMMENT_UPDATE_URL = "agency_system:reply-update"
REPLY_COMMENT_DELETE_URL = "agency_system:reply-delete"


class PublicTopicTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.topic = Topic.objects.create(
            name="test_topic"
        )

    def test_login_required_topic_list(self):
        url = TOPIC_LIST_URL
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_topic_detail(self):
        url = reverse(TOPIC_DETAIL_URL, kwargs={"pk": self.topic.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_topic_create(self):
        url = TOPIC_CREATE_URL
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_topic_update(self):
        url = reverse(TOPIC_UPDATE_URL, kwargs={"pk": self.topic.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_topic_delete(self):
        url = reverse(TOPIC_DELETE_URL, kwargs={"pk": self.topic.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test123",
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(
            name="test_topic"
        )

    def test_retrieve_topic_list(self):
        res = self.client.get(TOPIC_LIST_URL)
        topics = self.topic.__class__.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(topics), list(res.context["topic_list"]))
        self.assertTemplateUsed(res, "agency_system/topic_list.html")

    def test_topic_detail_access(self):
        res = self.client.get(reverse(TOPIC_DETAIL_URL, kwargs={"pk": self.topic.id}))
        topics = self.topic.__class__.objects.get(pk=self.topic.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(topics, res.context["topic"])
        self.assertTemplateUsed(res, "agency_system/topic_detail.html")

    def test_topic_create_access(self):
        res = self.client.get(TOPIC_CREATE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "agency_system/topic_form.html")

    def test_topic_update_access(self):  # only for superuser usage test
        res = self.client.get(reverse(TOPIC_UPDATE_URL, kwargs={"pk": self.topic.id}))
        topics = self.topic.__class__.objects.get(pk=self.topic.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(topics, res.context["topic"])
        self.assertTemplateUsed(res, "agency_system/topic_form.html")

    def test_topic_delete_access(self):  # only for superuser usage test
        res = self.client.get(reverse(TOPIC_DELETE_URL, kwargs={"pk": self.topic.id}))
        topics = self.topic.__class__.objects.get(pk=self.topic.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(topics, res.context["topic"])
        self.assertTemplateUsed(res, "agency_system/topic_confirm_delete.html")

    def test_topic_search_form_by_name(self):
        searched_name = "test_topic"
        res = self.client.get(TOPIC_LIST_URL, name=searched_name)
        self.assertEqual(res.status_code, 200)
        filtered_search = self.topic.__class__.objects.filter(name__startswith=searched_name)
        self.assertEqual(list(filtered_search), list(res.context["topic_list"]))


class PublicRedactorTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.redactor = get_user_model().objects.create_user(
            username="test2",
            password="test456"
        )

    def test_login_required_redactor_list(self):
        res = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_redactor_detail(self):
        res = self.client.get(REDACTOR_DETAIL_URL, kwargs={"pk": self.redactor.id})
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_redactor_update(self):
        res = self.client.get(REDACTOR_UPDATE_URL, kwargs={"pk": self.redactor.id})
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_redactor_delete(self):
        res = self.client.get(REDACTOR_DELETE_URL, kwargs={"pk": self.redactor.id})
        self.assertNotEqual(res.status_code, 200)


class RedactorCreateTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("agency_system:redactor-create")
        self.success_url = reverse("agency_system:registration-success")

    def test_create_account(self):
        form_data = {
            "username": "testuser123",
            "first_name": "name",
            "last_name": "surname",
            "email": "test_email@example.com",
            "years_of_experience": 0,
            "password1": "testpsw1",
            "password2": "testpsw1",
        }
        res = self.client.post(self.url, form_data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.success_url)
        self.assertTrue(get_user_model().objects.filter(username="testuser123"))


class RedactorChangePassword(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="testpsw1"
        )
        self.client.force_login(self.user)
        self.url = reverse("agency_system:password-update", kwargs={"pk": self.user.id})
        self.success_url = reverse("agency_system:password-changed")

    def test_user_change_psw_and_login_with_new_psw(self):
        form_data = {
            "old_password": "testpsw1",
            "new_password1": "testpsw2",
            "new_password2": "testpsw2",
        }
        res = self.client.post(self.url, form_data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.success_url)
        self.assertTrue(self.client.login(username=self.user.username, password="testpsw2"))


class PrivateRedactorTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test2",
            password="test456"
        )
        self.client.force_login(self.user)
        self.url = reverse("agency_system:password-update", kwargs={"pk": self.user.id})
        self.success_url = reverse("agency_system:password-changed")

    def test_retrieve_redactor_list(self):
        res = self.client.get(REDACTOR_LIST_URL)
        redactor_list = Redactor.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(redactor_list), list(res.context["redactor_list"]))
        self.assertTemplateUsed(res, "agency_system/redactor_list.html")

    def test_redactor_detail_access(self):
        res = self.client.get(reverse(REDACTOR_DETAIL_URL, kwargs={"pk": self.user.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.user.id, res.context["redactor"].id)
        self.assertTemplateUsed(res, "agency_system/redactor_detail.html")

    def test_redactor_update_access(self):
        res = self.client.get(reverse(REDACTOR_UPDATE_URL, kwargs={"pk": self.user.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.user.id, res.context["redactor"].id)
        self.assertTemplateUsed(res, "registration/edit_profile.html")

    def test_redactor_delete_access(self):
        res = self.client.get(reverse(REDACTOR_DELETE_URL, kwargs={"pk": self.user.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.user.id, res.context["redactor"].id)
        self.assertTemplateUsed(res, "agency_system/redactor_confirm_delete.html")
        del_res = self.client.delete(reverse(REDACTOR_DELETE_URL, kwargs={"pk": self.user.id}))
        self.assertRedirects(del_res, reverse("login"), status_code=302)

    def test_redactor_search_form_by_username(self):
        searched_name = "test2"
        res = self.client.get(REDACTOR_LIST_URL, name=searched_name)
        self.assertEqual(res.status_code, 200)
        filtered_search = self.user.__class__.objects.filter(username__startswith=searched_name)
        self.assertEqual(list(filtered_search), list(res.context["redactor_list"]))
        self.assertEqual(res.status_code, 200)


class PublicNewspaperTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.topic = Topic.objects.create(
            name="test_topic"
        )
        self.newspaper = Newspaper.objects.create(
            title="test_news",
            topic=self.topic,
        )

    def test_login_required_newspaper_list(self):
        url = NEWSPAPER_LIST_URL
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_newspaper_detail(self):
        url = reverse(NEWSPAPER_DETAIL_URL, kwargs={"pk": self.newspaper.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_newspaper_create(self):
        url = NEWSPAPER_CREATE_URL
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_newspaper_update(self):
        url = reverse(NEWSPAPER_UPDATE_URL, kwargs={"pk": self.newspaper.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_newspaper_delete(self):
        url = reverse(NEWSPAPER_DELETE_URL, kwargs={"pk": self.newspaper.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateNewspaperTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpsw1",
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(
            name="test_topic",
        )
        self.newspaper = Newspaper.objects.create(
            title="test_news",
            topic=self.topic,
            content="qwerty",
        )
        self.newspaper.publishers.add(self.user)

    def test_newspaper_retrieve_list(self):
        res = self.client.get(NEWSPAPER_LIST_URL)
        news_list = Newspaper.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(news_list), list(res.context["newspaper_list"]))
        self.assertTemplateUsed(res, "agency_system/newspaper_list.html")

    def test_newspaper_detail_access(self):
        res = self.client.get(reverse(NEWSPAPER_DETAIL_URL, kwargs={"pk": self.newspaper.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.newspaper.publishers.filter(id=self.user.id).exists())
        self.assertTemplateUsed(res, "agency_system/newspaper_detail.html")

    def test_newspaper_create_access(self):
        res = self.client.get(NEWSPAPER_CREATE_URL)
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res,"agency_system/newspaper_form.html")

    def test_newspaper_update_access(self):
        res = self.client.get(reverse(NEWSPAPER_UPDATE_URL, kwargs={"pk": self.newspaper.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.newspaper.publishers.filter(id=self.user.id).exists())
        self.assertTemplateUsed(res, "agency_system/newspaper_update.html")

    def test_newspaper_delete_access(self):
        res = self.client.get(reverse(NEWSPAPER_DELETE_URL, kwargs={"pk": self.newspaper.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.newspaper.publishers.filter(id=self.user.id).exists())
        self.assertTemplateUsed(res, "agency_system/newspaper_confirm_delete.html")

    def test_newspaper_search_form_by_title(self):
        searched_name = "test_news"
        res = self.client.get(NEWSPAPER_LIST_URL, name=searched_name)
        self.assertEqual(res.status_code, 200)
        filtered_search = self.newspaper.__class__.objects.filter(title__icontains=searched_name)
        self.assertEqual(list(filtered_search), list(res.context["newspaper_list"]))


class PublicCommentAndRepliesTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.topic = Topic.objects.create(
            name="test_topic",
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpsw1",
        )
        self.news = Newspaper.objects.create(
            title="test_news",
            topic=self.topic
        )
        self.comment = Comment.objects.create(
            post_comment=self.news,
            author=self.user
        )

    def test_login_required_create_comment(self):
        url = COMMENT_CREATE_URL
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_comment_and_replies_detail(self):
        url = COMMENT_AND_REPLIES_DETAIL
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_edit_comment(self):
        url = reverse(COMMENT_UPDATE_URL, kwargs={"pk": self.comment.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_delete_comment(self):
        url = reverse(COMMENT_DELETE_URL, kwargs={"pk": self.comment.id})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCommentAndReplyTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpsw1"

        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(
            name="test_topic"
        )
        self.news = Newspaper.objects.create(
            title="test_news",
            topic=self.topic
        )
        self.news.publishers.add(self.user)
        self.comment = Comment.objects.create(
            post_comment=self.news,
            author=self.user,
            body="qwerty",
        )
        self.reply_comment = ReplyComment.objects.create(
            comment_author=self.comment,
            reply_author=self.comment.author,
            reply_body="qwertyuiop",
        )

    def test_comment_update_access(self):
        res = self.client.get(reverse(COMMENT_UPDATE_URL, kwargs={"pk": self.comment.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.comment.author, self.user)
        form_data = {
            "body": "qwerty123"
        }
        res = self.client.post(reverse(COMMENT_UPDATE_URL, kwargs={"pk": self.comment.id}), form_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(reverse(COMMENT_UPDATE_URL, kwargs={"pk": self.comment.id}),
                         f"/comments/{self.user.id}/update")

    def test_comment_delete_access(self):
        res = self.client.get(reverse(COMMENT_DELETE_URL, kwargs={"pk": self.comment.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.comment.author, self.user)
        self.assertTemplateUsed(res, "agency_system/comment_confirm_delete.html")
        res = self.client.post(reverse(COMMENT_DELETE_URL, kwargs={"pk": self.comment.id}))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(reverse(NEWSPAPER_DETAIL_URL, kwargs={"pk": self.news.id}), f"/newspapers/{self.news.id}/")

    def test_reply_comment_access(self):
        res = self.client.get(reverse(REPLY_COMMENT_CREATE_URL,
                                      kwargs={
                                          "pk": self.news.id,
                                          "comment_id": self.reply_comment.comment_author.id
                                      }))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.reply_comment.reply_author, self.user)
        self.assertTemplateUsed(res, "agency_system/comment_reply_form.html")
        form_data = {
            "reply_body": "qwerty!"
        }
        res = self.client.post(reverse(REPLY_COMMENT_CREATE_URL,
                                       kwargs={
                                           "pk": self.news.id,
                                           "comment_id": self.reply_comment.comment_author.id
                                       }), form_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(reverse(NEWSPAPER_DETAIL_URL, kwargs={"pk": self.news.id}), f"/newspapers/{self.news.id}/")

    def test_reply_comment_update_access(self):
        res = self.client.get(reverse(REPLY_COMMENT_UPDATE_URL, kwargs={"pk": self.reply_comment.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.reply_comment.reply_author, self.user)
        self.assertTemplateUsed(res, "agency_system/reply_update.html")
        fields = {
            "reply_body": "qwerty12345"
        }
        res = self.client.post(reverse(REPLY_COMMENT_UPDATE_URL, kwargs={"pk": self.reply_comment.id}), fields)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(reverse(COMMENT_AND_REPLIES_DETAIL, kwargs={"pk": self.comment.id}),
                         f"/comments/{self.comment.id}/replies")

    def test_reply_comment_delete_access(self):
        res = self.client.get((reverse(REPLY_COMMENT_DELETE_URL, kwargs={"pk": self.reply_comment.id})))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.reply_comment.reply_author, self.user)
        self.assertTemplateUsed(res, "agency_system/reply_confirm_delete.html")
        res = self.client.post((reverse(REPLY_COMMENT_DELETE_URL, kwargs={"pk": self.reply_comment.id})))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(reverse(COMMENT_AND_REPLIES_DETAIL, kwargs={"pk": self.comment.id}),
                         f"/comments/{self.comment.id}/replies")
