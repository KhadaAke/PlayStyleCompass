# Generated by Django 4.2.4 on 2023-11-09 11:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_userprofile_email_confirmed"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="name_last_update_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
