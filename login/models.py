from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from tutor.models import Tutor 
from student.models import Student


class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        user_type=None,
        tutor=None,
        student=None,
        # username=None,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password):
    return self._create_user(email, password, False, False)

  def create_superuser(self, email, password):
    user=self._create_user(email, password, True, True)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, null=True, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    # username = models.EmailField(max_length=254,null=True,unique=True)

    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []



    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
    # Source: https://medium.com/@ksarthak4ever/django-custom-user-model-allauth-for-oauth-20c84888c318