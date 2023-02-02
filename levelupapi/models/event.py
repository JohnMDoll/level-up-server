from django.db import models


class Event(models.Model):

    description = models.CharField(max_length=500)
    date = models.DateField(auto_now=False, auto_now_add=False)
    attendees = models.ManyToManyField("Gamer", related_name="events_attending" )
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="organizer_events" )
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="game_events")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value