# Generated by Django 4.2.7 on 2024-02-11 09:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agency_system", "0017_remove_newspaper_topic_newspaper_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="topic_images",
            field=models.ImageField(
                blank=True, null=True, upload_to="popular_topics_images/"
            ),
        ),
    ]
