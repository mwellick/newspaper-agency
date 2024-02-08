from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from agency_system.models import Topic

TOPIC_LIST_URL = reverse("agency_system:topic-list")
TOPIC_DETAIL_URL = "agency_system:topic-detail"
TOPIC_CREATE_URL = reverse("agency_system:topic-create")
TOPIC_UPDATE_URL = "agency_system:topic-update"
TOPIC_DELETE_URL = "agency_system:topic-delete"


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
        self.assertEquals(list(filtered_search), list(res.context["topic"]))
