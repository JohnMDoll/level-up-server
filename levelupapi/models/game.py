from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):

    name = models.CharField(max_length=150)
    bio = models.CharField(max_length=50)
    gamer = models.ForeignKey("Gamer", null=True, on_delete=models.CASCADE, related_name="game_creator" )
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name="game_type")