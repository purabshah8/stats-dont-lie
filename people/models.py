from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from teams.models import Team
# Create your models here.

class Person(models.Model):
    last_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    dob = models.DateField()
    class Meta:
        abstract = True

class Player(Person):
    shooting_hand_choices = (
        ('Left', 'Left'),
        ('Right', 'Right')
    )
    height = models.IntegerField()
    weight = models.IntegerField()
    shooting_hand = models.CharField(choices=shooting_hand_choices, max_length=5)
    team = models.ForeignKey(Team, models.SET_NULL, null=True)
    draft_year = models.IntegerField(null=True)
    draft_position = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(60)])
    draft_team = models.ForeignKey(Team, models.SET_NULL, null=True)
    number = models.IntegerField()

class Referee(Person):
    first_year = models.IntegerField()
    number = models.IntegerField()

class Executive(Person):
    team = models.ForeignKey(Team, models.SET_NULL, null=True)