from django.db import models


class Score(models.Model):
    player_id = models.PositiveIntegerField(primary_key=True)
    score = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
