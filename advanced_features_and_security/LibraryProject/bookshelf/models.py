from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length = 100)
    published_year = models.IntegerField()
    
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, date_of_birth=None, profile_photo=None, **extra_fields):
        if not email:
            raise ValueError("You have not entered a valid email")
        
        email =self.normalize_email(email)
        user = user.model(username=username,
                          email=email,
                          date_of_birth=date_of_birth,
                          profile_photo=profile_photo,
                          **extra_fields)
    
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
    
        return self.create_user(email, password, **extra_fields)
        
    def create_superuser(self, username, email, password, **extra_fields):
       extra_fields.setdefault('is_staff', True)
       extra_fields.setdefault('is_superuser', True)
       return super().create_superuser(username, email, password, **extra_fields)
   
class User(AbstractBaseUser, PermissionsMixin):
    email =models.EmailField(blank=True, default='', unique=True)
    name =models.CharField(max_length=255, blank=True, default='')
    
    is_active =models.BooleanField(default=True)
    is_superuser =models.BooleanField(default=False)
    is_staff =models.BooleanField(default=False)
    
    date_joined =models.DateTimeField(default=timezone.now)
    last_login =models.DateTimeFieldt(blank=True, null=True)
    
    objects =CustomUserManager()
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELD =[]
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
