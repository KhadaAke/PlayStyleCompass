# Generated by Django 4.2.4 on 2023-09-20 14:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_contactmessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="profile_name",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
