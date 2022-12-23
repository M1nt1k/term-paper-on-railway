from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email: 
            raise ValueError("Вы не ввели Email")
        if not password: 
            raise ValueError("Вы не ввели пароль")
        user = self.model(
            email=self.normalize_email(email),
            # password=password
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
    password = models.CharField(max_length=100)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    third_name = models.CharField(max_length=100)
    
    is_active = models.BooleanField(default=True) # Статус активации
    is_staff = models.BooleanField(default=False) # Статус админа


    USERNAME_FIELD = 'email' # Идентификатор для обращения 
    REQUIRED_FIELDS = [] # Список имён полей для Superuser
 
    objects = MyUserManager() # Добавляем методы класса MyUserManager

    def __str__(self) -> str:
        return self.email
