from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            bio="",

        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="user",
            password="admin123",
            bio="",
            years_of_experience=0,
            profile_images=""
        )

    def test_redactor_info_listed(self):
        url = reverse("admin:agency_system_redactor_changelist")
        result = self.client.get(url)
        self.assertContains(result, self.redactor.profile_images)
        self.assertContains(result, self.redactor.years_of_experience)

    def test_redactor_detail_info_listed(self):
        url = reverse("admin:agency_system_redactor_change", args=[self.redactor.id])
        result = self.client.get(url)
        self.assertContains(result, self.redactor.bio)
        self.assertContains(result, self.redactor.profile_images)
        self.assertContains(result, self.redactor.years_of_experience)

    def test_add_redactor_info(self):
        url = reverse("admin:agency_system_redactor_add")
        result = self.client.get(url)
        self.assertContains(result, self.redactor.bio)
        self.assertContains(result, self.redactor.profile_images)
        self.assertContains(result, self.redactor.years_of_experience)
