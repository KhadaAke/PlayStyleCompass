# Generated by Django 4.2.4 on 2023-09-22 15:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_userprofile_profile_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email_confirmed",
            field=models.BooleanField(default=False),
        ),
    ]
