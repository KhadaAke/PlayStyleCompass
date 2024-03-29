# Generated by Django 4.2.4 on 2024-01-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playstyle_compass", "0007_game_franchise"),
    ]

    operations = [
        migrations.CreateModel(
            name="Franchise",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("overview", models.TextField()),
                ("games", models.CharField(max_length=200)),
                ("image", models.TextField()),
            ],
            options={
                "db_table": "Franchises",
            },
        ),
        migrations.RenameField(
            model_name="game",
            old_name="franchise",
            new_name="franchises",
        ),
    ]
