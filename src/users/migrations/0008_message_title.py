# Generated by Django 4.2.4 on 2024-01-06 12:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="title",
            field=models.TextField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]