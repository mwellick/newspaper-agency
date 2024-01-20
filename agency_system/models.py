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
        return f"{self.username}"


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments_author",
                               null=True)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} left a comment under {self.post_comment.title}: {self.body}"

    class Meta:
        ordering = ["-date_added"]


class ReplyComment(models.Model):
    comment_author = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_replies")
    reply_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author_replies")
    reply_body = models.TextField()
    reply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.reply_author} replied on {self.comment_author.author} comment "
                f"(comment reply id:{self.comment_author.id}|comment:{self.comment_author.post_comment.id})")
