# Generated by Django 4.2.4 on 2023-11-27 13:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("playstyle_compass", "0037_review_disliked_by_review_liked_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="disliked_by",
        ),
        migrations.RemoveField(
            model_name="review",
            name="liked_by",
        ),
        migrations.RemoveField(
            model_name="review",
            name="dislikes",
        ),
        migrations.RemoveField(
            model_name="review",
            name="likes",
        ),
        migrations.AddField(
            model_name="review",
            name="dislikes",
            field=models.ManyToManyField(
                blank=True, related_name="disliked_reviews", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="liked_reviews", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
