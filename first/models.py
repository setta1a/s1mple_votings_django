from django.db import models

# Create your models here.

class DiscreteVotings(models.Model):
    theme = models.CharField(max_length=100)
    first_option = models.CharField(max_length=50)
    second_option = models.CharField(max_length=50)
    first_option_count = models.IntegerField()
    second_option_count = models.IntegerField()