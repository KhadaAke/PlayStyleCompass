# Generated by Django 4.2.4 on 2023-10-13 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playstyle_compass", "0012_game_game_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="release_date",
            field=models.DateField(),
        ),
    ]