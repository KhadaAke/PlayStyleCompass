# Generated by Django 4.2.4 on 2023-10-13 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playstyle_compass", "0019_alter_game_release_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="release_date",
            field=models.CharField(max_length=100),
        ),
    ]