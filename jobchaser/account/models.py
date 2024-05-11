from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField
from datetime import date
from django.utils.timezone import now
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, firstName, middleName, lastName,location, dob, education=None,work=None, password=None, confirmPassword=None, **extra_fields):        
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstName=firstName, middleName=middleName, lastName=lastName,location=location, dob=dob, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        # Create education record
        if education:
            Education.objects.create(user=user, **education)
        if work:
            WorkExperience.objects.create(user=user,**education)    
        
        return user

    def create_superuser(self, email, firstName,middleName, lastName,location,yoe,phone,dob,gender,password=None):
        # creates and saves a superuser
        user = self.create_user(email,password=password,firstName=firstName,middleName=middleName,lastName=lastName,location=location,yoe=yoe,phone=phone,dob=dob,gender=gender)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self.db)
        return user

class Education(models.Model):
    user = models.ForeignKey('User', related_name='user_educations', on_delete=models.CASCADE) #forword reference
    degree = models.CharField(max_length=100)
    specialisation = models.CharField(max_length=100)
    start = models.DateField(default=timezone.now)
    end = models.DateField(default=timezone.now)
    school = models.CharField(max_length=100)

class WorkExperience(models.Model):
    STILL_WORK_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    user = models.ForeignKey('User', related_name='user_workexperience', on_delete=models.CASCADE) #forword reference
    organisation=models.CharField(max_length=100)
    topSkill =models.CharField(max_length=100)
    current = models.CharField(max_length=3, choices=STILL_WORK_CHOICES, default="NA")
    start= models.DateField(default=timezone.now)
    end= models.DateField(default=timezone.now,null=True,blank=True)
    
class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    email = models.EmailField(unique=True,max_length=255)
    firstName = models.CharField(max_length=30)
    middleName = models.CharField(max_length=30, default=' ')
    lastName = models.CharField(max_length=30)
    yoe = models.PositiveIntegerField(default=0)
    moe = models.PositiveIntegerField(default=0)
    skill = models.CharField(max_length=200)
    about = models.TextField()
    phone = models.CharField(max_length=12)
    location = models.CharField(max_length=200,default='null')
    dob = models.DateField(default=date(1900, 1, 1))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='NA')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_age = models.PositiveIntegerField(blank=True, null=True)  # Database field for age
    #education = models.ForeignKey(Education, related_name='user_education', on_delete=models.SET_NULL, blank=True, null=True)
    education = models.ManyToManyField(Education, related_name='users')
    work = models.ManyToManyField(WorkExperience,related_name='workexusers')
 
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'yoe','moe','skill','dob','gender']

    def __str__(self):
        return self.email
    
    
    def save(self, *args, **kwargs):
        # Calculate and save age field before saving
        self.user_age = self.calculate_age
          # Increment yoe if moe is greater than or equal to 6
        if self.moe >= 6:
            self.yoe += 1
        super().save(*args, **kwargs)
        
    @property
    def calculate_age(self):
        today = now().date()
        dob = self.dob
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





