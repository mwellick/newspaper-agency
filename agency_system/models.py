from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="published_newspapers"
    )
    news_images = models.ImageField(null=True, blank=True, upload_to="news_images/",
                                    verbose_name="Header Image (800x450)")

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    post_comment = models.ForeignKey(Newspaper, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post_comment.title} - {self.name}"
