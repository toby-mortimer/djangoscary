from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def __str__(self):
        return self.user_name

class Competition(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    no_of_rounds = models.IntegerField()
    gates_per_round = models.IntegerField()

    def __str__(self):
        return self.name

class Score(models.Model):
    round = models.IntegerField()
    total_score = models.IntegerField()
    time_taken = models.IntegerField()
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    score = models.ForeignKey(Competition, on_delete=models.CASCADE)

class Ruleset(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Rule(models.Model):
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    point = models.IntegerField()

    def __str__(self):
        return self.name

class Truck(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TruckClass(models.Model):
    type = models.CharField(max_length=20)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

    def __str__(self):
        return self.type