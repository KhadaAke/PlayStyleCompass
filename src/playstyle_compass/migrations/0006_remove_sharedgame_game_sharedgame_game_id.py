# Generated by Django 4.2.4 on 2024-01-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playstyle_compass", "0005_sharedgame_game"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sharedgame",
            name="game",
        ),
        migrations.AddField(
            model_name="sharedgame",
            name="game_id",
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
