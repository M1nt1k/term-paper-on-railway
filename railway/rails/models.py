from django.conf import settings
from django.db import models
from django.urls import reverse


class Train(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    start_time = models.TimeField()
    end_time = models.TimeField()
    
    start_date = models.DateField()
    end_date = models.DateField()

    start_city = models.ForeignKey('City', related_name='trains_start', on_delete=models.DO_NOTHING)
    end_city = models.ForeignKey('City', related_name='trains_end', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('train', kwargs={'train_slug': self.slug})

class Ticket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    train = models.ForeignKey('Train', related_name='tickets', on_delete=models.DO_NOTHING)
    carriage = models.ForeignKey('Carriage', related_name='tickets', on_delete=models.DO_NOTHING)

    places = models.ForeignKey('Places', related_name='tickets', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.train.name + '-' + str(self.places)

class City(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.name

class Carriage(models.Model):
    pls = [
        ('RS','Плацкарт'),
        ('CP','Купе'),
        ('SW','СВ')
    ]

    train = models.ForeignKey('Train', related_name='carriages', on_delete=models.CASCADE)

    number = models.IntegerField()
    place_type = models.CharField(
        max_length=2,
        choices=pls
    )
    
    def __str__(self) -> str:
        return self.train.name + '-' + str(self.number) + '-' + self.get_place_type_display()
    

class Places(models.Model):
    carriage = models.ForeignKey('Carriage', related_name='places', on_delete=models.CASCADE)
    number = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.number) + '-' + str(self.carriage.number)




