from django.db import models

# Create your models here.
"""
Model to save user messages(that comes from contact page) in database
"""
class Message(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False)
    subject = models.CharField(max_length=400, blank=False)
    message = models.TextField(max_length=800, blank=False)

    def __str__(self):
        return self.name

"""
Model to save user search history
"""
class UserSearchHistory(models.Model):
    username = models.TextField(max_length=50)
    word = models.TextField(max_length=50)
    time = models.DateTimeField()

    def __str__(self):
        return self.username