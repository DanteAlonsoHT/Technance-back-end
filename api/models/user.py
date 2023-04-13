from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey

def user_directory_path(instance, filename):
  # file will be uploaded to MEDIA_ROOT /profile-image/<filename>
  name = 'profile-image'
  return '{0}/{1}'.format(name, filename)

class UserProfileManager(BaseUserManager):
  def create_user(self, 
                  full_name,
                  preferred_name,
                  email = None,
                  password = None,
                  image_profile = None,
                  ):
    if not full_name:
      raise ValueError("Nombre completo es un campo requerido")

    if not preferred_name:
      raise ValueError("Nombre preferido es un campo requerido")
    
    if email:
      email = self.normalize_email(email)
    
    user = self.model(full_name = full_name,
                      preferred_name = preferred_name,
                      email = email,
                      image_profile = image_profile,
                      )
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, 
                      full_name,
                      preferred_name,
                      email,
                      password,
                      image_profile ='',
                      ):
    user = self.create_user(full_name, preferred_name, email)
    user.is_superuser = True
    user.is_staff = True
    
    user.save(using=self._db)

    return user

class User(AbstractBaseUser, PermissionsMixin):
  full_name = models.CharField(max_length=300, blank=False)
  preferred_name = models.CharField(max_length=100, blank=False)
  email = models.EmailField(max_length=150, blank=False, unique=True)
  image_profile = models.ImageField(
    upload_to=user_directory_path,
    blank=True
  )
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserProfileManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = [
    'full_name',
    'preferred_name',
  ]

  def get_full_name(self):
    return f'{self.full_name}'

  def __str__(self):
    return f'{self.email}'
  
  class Meta:
    app_label = 'api'
