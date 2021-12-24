#models.py
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin
from django.utils.translation import gettext_lazy as _


# custom usermodel
class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError(_("Your must provide an email address"))
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email,password,**extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    isAuthorized = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff=models.BooleanField(_('is_staff'), default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['isAuthorized']



#admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdminConfig(UserAdmin):
    search_fields = ('email',)
    ordering = ('-start_date',)
    list_display = ('email','is_superuser','isAuthorized')
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Permissions',{'fields':('is_staff','is_superuser','isAuthorized')}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
        ('Permissions',{'fields':('is_staff','is_superuser','isAuthorized')}),
    )

admin.site.register(User,UserAdminConfig)