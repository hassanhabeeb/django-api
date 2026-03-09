from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# FIX: You must import Group to use it as a variable in the ManyToManyField
from django_acl.models import Group, AbstractDateFieldMix

from django_acl.utils.helper import acl_has_perms
from breathline.models import AbstractDateTimeFieldBaseModel

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, replica_db=None, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))

        user = self.model(username=username, replica_db=replica_db, **extra_fields)
        if password:
            user.set_password(password.strip())
            
        user.save(using=replica_db)
        return user

    def create_superuser(self, username, password, replica_db=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_admin', True)
     
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        
        return self.create_user(username, password, replica_db, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin, AbstractDateFieldMix):
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self.original_password = self.password

    class GenderType(models.TextChoices):
        male    = 'Male'
        female  = 'Female'
        other   = 'Other'

    email                        = models.EmailField(_('email'), unique = True, max_length = 255, blank = True, null = True)
    username                     = models.CharField(_('username'), max_length = 300, unique = True, blank = True, null = True)
    password                     = models.CharField(_('password'), max_length=255, blank = True, null = True, editable=False)
    slug                         = models.SlugField(_('slug'),  max_length=255, unique=True, blank = True, null = True)
    date_joined                  = models.DateTimeField(_('date_joined'),  auto_now_add = True, blank = True, null = True)
    last_login                   = models.DateTimeField(_('last_login'), blank = True, null = True)
    last_logout                  = models.DateTimeField(_('last_logout'),  blank = True, null = True)
    last_active                  = models.DateTimeField(_('last_active'),  blank = True, null = True)
    last_password_reset          = models.DateTimeField(_('last_password_reset'),  blank = True, null = True)
    is_verified                  = models.BooleanField(default = False)
    is_admin                     = models.BooleanField(default = False)
    is_staff                     = models.BooleanField(default = False)
    is_superuser                 = models.BooleanField(default = False)
    is_logged_in                 = models.BooleanField(default = False)
    failed_login_attempts        = models.IntegerField(_('Failed Login Attempts'),  blank = True, null = True)
    is_active                    = models.BooleanField(_('Is Active'), default=True)
    is_password_already_updated  = models.BooleanField(_('Is Password Already Updated'),default=False,blank=True,null=True)
    is_invited_by_admin          = models.BooleanField(_('Is Invited By Admin'),default=False,blank=True,null=True) 
    is_password_reset_required   = models.BooleanField(default=False)
    name                         = models.CharField(_('name'), max_length=255, blank = True, null = True)
    first_name                   = models.CharField(_('First Name'),max_length=225,null=True,blank=True)
    last_name                    = models.CharField(_('last_name'),max_length=225,null=True,blank=True) 
    profile_image                = models.FileField(_('Profile Image'),null=True,blank=True)
    replica_db                   = models.CharField(max_length=20, choices=[('replica_1', 'Replica 1'), ('replica_2', 'Replica 2')],blank = True, null = True)
    
    # FIX: Using the Group model imported from django_acl
    user_groups                  = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_name="custom_user_groups", # Changed to avoid conflict with default
        related_query_name="user",
    )
    
    phonenumber                  = models.CharField(_('Phone Number'),max_length=15,null=True,blank=True,unique=True)
    gender                       = models.CharField(_('Gender'), choices=GenderType.choices, null=True, blank=True, default= GenderType.other)
 
    USERNAME_FIELD = 'username'
    objects = UserManager()
    
    def __str__(self):
        return self.username or self.email or str(self.pk)

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def has_acl_perms(self, perm, obj = None):
        return acl_has_perms(self, perm, obj=obj)
    
    def _password_has_been_changed(self):
        return self.original_password != self.password

class GeneratedAccessToken(AbstractDateFieldMix):
    token = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.token

class ErrorLog(AbstractDateTimeFieldBaseModel):
    error_message = models.TextField()
    user_id = models.IntegerField(null=True, blank=True)
 
    class Meta:
        verbose_name = "Error Log"
        verbose_name_plural = "Error Logs"
