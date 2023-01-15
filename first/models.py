from django.contrib.auth.models import User
from django.db import models


class Voting(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=175)
    voting_type = models.IntegerField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)


class VoteVariant(models.Model):
    description = models.CharField(max_length=50)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE, default=1)

    def calculateVotes(self):
        return VoteFact.objects.filter(variant=self).count()

    votes_count = property(calculateVotes)


class VoteFact(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField()
