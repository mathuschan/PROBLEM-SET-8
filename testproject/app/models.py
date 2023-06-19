from django.db import models
from django.db.models import Sum
from datetime import datetime

class Artist(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    year_born = models.IntegerField()
    year_died = models.IntegerField(null=True)
    image = models.ImageField(upload_to='artists', default='default.jpg')

    def is_alive(self):
        return self.year_died is None

    def is_older_than(self, number_of_years):
        return self.year_born <= datetime.now.year() - 100
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Museum(models.Model):
    name = models.CharField(max_length=120)
    address = models.TextField()

    def inventory_value(self):
        return self.paintings.aggregate(Sum('value'))['value__sum']
    
    def number_of_paintings(self):
        return self.paintings.count()
    
    def number_of_paintings_on_display(self):
        return self.paintings.filter(is_on_display=True).count()

    def most_expensive_painting(self):
        return self.paintings.order_by('-value').first()
    
    def __str__(self) -> str:
        return self.name


class Painting(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(default='')
    creation_year = models.IntegerField()
    image = models.ImageField(upload_to='paintings/', default='paintings/default.jpg')
    value = models.IntegerField(default=0)
    is_on_display = models.BooleanField(default=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='paintings')
    museum = models.ForeignKey(Museum, on_delete=models.SET_NULL, null=True, related_name='paintings')

    def is_valid_value(self):
        return 0 <= self.value <= 1_000_000_000

    def __str__(self):
        return f'{self.title} by {self.artist}'
