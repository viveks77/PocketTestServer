from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,mobile_no, **extra_fields):
        
        if not email:
            raise ValueError(_("Email is required"))

        user = self.model( email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.mobile_no = mobile_no
        user.save()
        return user

    def create_user(self, email, password, mobile_no, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user( email, password,mobile_no, **extra_fields)

    
    def create_superuser(self,  email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)
        mobile_no =  0000000000
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have staff priviliages'))

        return self.create_user( email, password, mobile_no, **extra_fields)