from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField
from datetime import date
from django.utils.timezone import now
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, middle_name, last_name, date_of_birth, education_data=None,work_experince_data=None, password=None, password2=None, **extra_fields):        
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, middle_name=middle_name, last_name=last_name, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        # Create education record
        if education_data:
            Education.objects.create(user=user, **education_data)
        if work_experince_data:
            WorkExperience.objects.create(user=user,**education_data)    
        
        return user

    def create_superuser(self, email, first_name,middle_name, last_name,year_of_experience,phone,date_of_birth,gender,password=None):
        # creates and saves a superuser
        user = self.create_user(email,password=password,first_name=first_name,middle_name=middle_name,last_name=last_name,year_of_experience=year_of_experience,phone=phone,date_of_birth=date_of_birth,gender=gender)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self.db)
        return user

class Education(models.Model):
    user = models.ForeignKey('User', related_name='user_educations', on_delete=models.CASCADE) #forword reference
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(default=timezone.now)
    institution = models.CharField(max_length=100)

class WorkExperience(models.Model):
    STILL_WORK_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    user = models.ForeignKey('User', related_name='user_workexperience', on_delete=models.CASCADE) #forword reference
    organisation=models.CharField(max_length=100)
    top_skills =models.CharField(max_length=100)
    still_work = models.CharField(max_length=3, choices=STILL_WORK_CHOICES, default="NA")
    
    
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
    year_of_experience = models.PositiveIntegerField(default=0)
    month_of_experience = models.PositiveIntegerField(default=0)
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
    #education = models.ForeignKey(Education, related_name='user_education', on_delete=models.SET_NULL, blank=True, null=True)
    educations = models.ManyToManyField(Education, related_name='users')
    workexperience = models.ManyToManyField(WorkExperience,related_name='workexusers')
 
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'year_of_experience','month_of_experience','phone','date_of_birth','gender']

    def __str__(self):
        return self.email
    
    
    def save(self, *args, **kwargs):
        # Calculate and save age field before saving
        self.user_age = self.calculate_age
          # Increment year_of_experience if month_of_experience is greater than or equal to 6
        if self.month_of_experience >= 6:
            self.year_of_experience += 1
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





