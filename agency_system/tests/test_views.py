from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from agency_system.models import Topic, Redactor

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
        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(topics), list(res.context["topic_list"]))
        self.assertTemplateUsed(res, "agency_system/topic_list.html")

    def test_topic_detail_access(self):
        res = self.client.get(reverse(TOPIC_DETAIL_URL, kwargs={"pk": self.topic.id}))
        topics = self.topic.__class__.objects.get(pk=self.topic.id)
        self.assertEquals(res.status_code, 200)
        self.assertEquals(topics, res.context["topic"])
        self.assertTemplateUsed(res, "agency_system/topic_detail.html")

    def test_topic_create_access(self):
        res = self.client.get(TOPIC_CREATE_URL)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "agency_system/topic_form.html")

    def test_topic_update_access(self):  # only for superuser usage test
        res = self.client.get(reverse(TOPIC_UPDATE_URL, kwargs={"pk": self.topic.id}))
        topics = self.topic.__class__.objects.get(pk=self.topic.id)
        self.assertEquals(res.status_code, 200)
        self.assertEquals(topics, res.context["topic"])
        self.assertTemplateUsed(res, "agency_system/topic_form.html")

    def test_topic_delete_access(self):  # only for superuser usage test
        res = self.client.get(reverse(TOPIC_DELETE_URL, kwargs={"pk": self.topic.id}))
        topics = self.topic.__class__.objects.get(pk=self.topic.id)
        self.assertEquals(res.status_code, 200)
        self.assertEquals(topics, res.context["topic"])
        self.assertTemplateUsed(res, "agency_system/topic_confirm_delete.html")

    def test_topic_search_form_by_name(self):
        searched_name = "test_topic"
        res = self.client.get(TOPIC_LIST_URL, name=searched_name)
        self.assertEquals(res.status_code, 200)
        filtered_search = self.topic.__class__.objects.filter(name__startswith=searched_name)
        self.assertEquals(list(filtered_search), list(res.context["topic_list"]))


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
        self.assertEquals(res.status_code, 200)
