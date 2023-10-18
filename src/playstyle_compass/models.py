"""Defines models."""

from django.db import models
from django.contrib.auth.models import User


class GamingPreferences(models.Model):
    """Represents a user's gaming preferences."""

    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class UserPreferences(models.Model):
    """Represents user-specific gaming preferences."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gaming_history = models.TextField(blank=True)
    favorite_genres = models.CharField(max_length=255, blank=True)
    platforms = models.CharField(max_length=255, blank=True)
    favorite_games = models.CharField(max_length=255, blank=True)

    def add_favorite_game(self, game_id):
        favorite_games_list = self.favorite_games.split(',')
        if str(game_id) not in favorite_games_list:
            favorite_games_list.append(str(game_id))
            self.favorite_games = ','.join(favorite_games_list)
            self.save()

    def remove_favorite_game(self, game_id):
        favorite_games_list = self.favorite_games.split(',')
        if str(game_id) in favorite_games_list:
            favorite_games_list.remove(str(game_id))
            self.favorite_games = ','.join(favorite_games_list)
            self.save()


    def get_favorite_games(self):
        favorite_games_list = self.favorite_games.split(',')
        favorite_games_ids = [int(game_id.strip()) for game_id in favorite_games_list if game_id.strip()]
        return favorite_games_ids


    def __str__(self):
        return self.user.username


class Game(models.Model):
    """Represents a video game."""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    overview = models.TextField()
    genres = models.CharField(max_length=200)
    platforms = models.CharField(max_length=200)
    themes = models.CharField(max_length=200)
    image = models.TextField()
    release_date = models.CharField(max_length=100)   
    developers = models.CharField(max_length=100)
    game_images = models.TextField()
    similar_games = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Games"
        ordering = ["title"]
