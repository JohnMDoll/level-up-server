from django.db import models


class Game(models.Model):

    name = models.CharField(max_length=150)
    gamer = models.ForeignKey("Gamer", null=True, on_delete=models.CASCADE, related_name="games_created" )
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name="games")
    maker = models.CharField(max_length=150, default="Old Mother Hubbard")
    number_of_players = models.PositiveSmallIntegerField(default=3)
    skill_level = models.PositiveSmallIntegerField(default=5)
