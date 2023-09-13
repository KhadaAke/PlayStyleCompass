# Generated by Django 4.2.4 on 2023-09-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playstyle_compass", "0010_game_overview_alter_game_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="developers",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="game",
            name="release_date",
            field=models.CharField(max_length=100),
        ),
    ]
