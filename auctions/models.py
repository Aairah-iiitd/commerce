from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    type = models.CharField(max_length = 64)
    def __str__(self):
        return f"{self.type}"

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 400)
    start = models.IntegerField()
    url = models.URLField(blank = True)
    close = models.BooleanField(default = False)
    winner = models.ForeignKey(User, on_delete = models.DO_NOTHING, null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "items")
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "created_listings",null = True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    price = models.IntegerField()
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bids")
    bidder = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bids",null = True)

    def __str__(self):
        return f"{self.item.title} for ${self.price}"

class Comment(models.Model):
    comment = models.CharField(max_length = 400)
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")

class Watchlist(models.Model):
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "Watchlist")
    items = models.ManyToManyField(Listing, related_name= "items")
