from django.db import models

# Create your models here.
class Dictionary(models.Model):
    word = models.TextField(max_length=50)
    meaning = models.TextField(max_length=500)
    no_of_searches = models.IntegerField(default=0)
    example_1 = models.TextField(max_length=500, blank=True)
    example_2 = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.word