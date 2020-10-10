from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from login.manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

# Create your models here.

class Standard(models.Model):
    class_no  = models.CharField(_('class'),max_length=256)

    def __str__(self):
        return "class: " + self.class_no

class User(AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField(_('name'), max_length=256)
    email = models.EmailField(_('email address'), unique=True)
    mobile_no = models.CharField(max_length=10, unique=True)
    class_no = models.ForeignKey(Standard, on_delete=models.CASCADE,  null=True)
    location = models.CharField(max_length=256)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Subject(models.Model):
    name = models.CharField(max_length=256, unique=True)
    class_no =  models.ForeignKey(Standard, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Subject)
def slugify_name(sender, instance, *args, **kwargs):
	instance.slug = slugify(instance.name)
