from django.db import models

# Create your models here.
class Team(models.Model):
    CONFERENCES = (
        ('E', "Eastern Conference"),
        ('W', "Western Conference")
    )
    DIVISIONS = (
        ('Atlantic', 'Atlantic Division'),
        ('Central', 'Central Division'),
        ('Southeast', 'Southeast Division'),
        ('Southwest', 'Southwest Division'),
        ('Northwest', 'Northwest Divison'),
        ('Pacific', 'Pacific Division')
    )

    name = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    conference = models.CharField(choices=CONFERENCES, max_length=1)
    division = models.CharField(choices=DIVISIONS, max_length=9)
    arena = models.CharField(max_length=32)
    owner = models.CharField(max_length=32)
    # executive = models.CharField(max_length=32)
    owner = models.CharField(max_length=32)
    founded = models.IntegerField()
