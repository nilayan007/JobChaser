from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField
from datetime import date
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name,middle_name, last_name,date_of_birth, password=None,password2=None ,**extra_fields):
        # creates and saves a user with the given email,name and age and all 
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), first_name=first_name,middle_name=middle_name,last_name=last_name,date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name,middle_name, last_name,year_of_experience,phone,date_of_birth,gender,password=None):
        # creates and saves a superuser
        user = self.create_user(email,password=password,first_name=first_name,middle_name=middle_name,last_name=last_name,year_of_experience=year_of_experience,phone=phone,date_of_birth=date_of_birth,gender=gender)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self.db)
        return user

class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    email = models.EmailField(unique=True,max_length=255)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, default=' ')
    last_name = models.CharField(max_length=30)
    year_of_experience = models.PositiveIntegerField()
    skills = models.CharField(max_length=200)
    about = models.TextField()
    phone = models.CharField(max_length=12)
    date_of_birth = models.DateField(default=date(1900, 1, 1))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='NA')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_age = models.PositiveIntegerField(blank=True, null=True)  # Database field for age
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'year_of_experience','phone','date_of_birth','gender']

    def __str__(self):
        return self.email
    
    
    def save(self, *args, **kwargs):
        # Calculate and save age field before saving
        self.user_age = self.calculate_age
        super().save(*args, **kwargs)
        
    @property
    def calculate_age(self):
        today = now().date()
        dob = self.date_of_birth
        age = today.year - dob.year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1
        return age
        

    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True
  
