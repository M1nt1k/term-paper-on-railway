from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db.models.signals import post_save
from django.dispatch import receiver

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email: 
            raise ValueError("Вы не ввели Email")
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password):
        return self._create_user(email, password)
 
    # Делаем метод для создание админа сайта
    def create_superuser(self, email, password):
        return self._create_user(email, password, is_staff=True, is_superuser=True)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True) # Идентификатор
    email = models.EmailField(max_length=100, unique=True) # Email
    
    is_active = models.BooleanField(default=True) # Статус активации
    is_staff = models.BooleanField(default=False) # Статус админа


    USERNAME_FIELD = 'email' # Идентификатор для обращения 
    REQUIRED_FIELDS = [] # Список имён полей для Superuser
 
    objects = MyUserManager() # Добавляем методы класса MyUserManager

    def __str__(self) -> str:
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    third_name = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(blank=True)

    pass_serial = models.IntegerField()
    pass_number = models.IntegerField()

    def __str__(self) -> str:
        return self.user.email

class Train(models.Model):
    name = models.CharField(max_length=255)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    start_city = models.ForeignKey('City', related_name='trains_start', on_delete=models.DO_NOTHING)
    end_city = models.ForeignKey('City', related_name='trains_end', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name

class Ticket(models.Model):
    profile = models.ForeignKey('Profile', related_name='tickets', on_delete=models.DO_NOTHING)
    train = models.ForeignKey('Train', related_name='tickets', on_delete=models.DO_NOTHING)
    carriage = models.ForeignKey('Carriage', related_name='tickets', on_delete=models.DO_NOTHING)

    places = models.ForeignKey('Places', related_name='tickets', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.train + '-' + str(self.place)

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
        return self.train.name + '-' + str(self.number) + '-' + self.place_type
    

class Places(models.Model):
    carriage = models.ForeignKey('Carriage', related_name='places', on_delete=models.CASCADE)
    # profile = models.ManyToManyField('Profile', related_name='places')
    number = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.number) + '-' + str(self.carriage.number)

class Addons(models.Model):
    addons = [
        (1, 'Питание'),
        (2, 'Вагон-ресторан или кафе'),
        (3, 'ИРС (Информационно-развлекательный сервис'),
        (4, 'Душ в поезде'),
        (5, 'Фирменный'),
        (6, 'Специальные тарифы'),
        (7, 'Места для инвалидов')
    ]
    addon = models.IntegerField(
        choices=addons
    )
    train = models.ForeignKey('Train', related_name='train_addons', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.train.name


