from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, age, password=None,password2=None ,**extra_fields):
        # creates and saves a user with the given email,name and age and all 
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name, age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, age,year_of_experience,phone,password=None):
        # creates and saves a superuser
        user = self.create_user(email,password=password,first_name=first_name,last_name=last_name,age=age,year_of_experience=year_of_experience,phone=phone)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self.db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True,max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    year_of_experience = models.PositiveIntegerField()
    skills = models.CharField(max_length=200)
    about = models.TextField()
    phone = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'year_of_experience','phone']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True
