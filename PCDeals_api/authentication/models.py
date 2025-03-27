from django.db import models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, 
                                        PermissionsMixin) 

class UserManager(BaseUserManager):

    def create_user(self, username, PhoneNumber, email, password=None,first_name=None, last_name=None):
        if username is None:
            raise TypeError('Users should have a username') 
        if email is None:
            raise TypeError('User should have a Email')
        if PhoneNumber is None:
            raise TypeError('User should have a phone number') 
        
        user = self.model(username=username, 
                          first_name=first_name, 
                          last_name=last_name, 
                          PhoneNumber=PhoneNumber, 
                          email=self.normalize_email(email))
        print(f"Creating user: username={username}, email={email}, PhoneNumber={PhoneNumber}, first_name={first_name}, last_name={last_name}, password={password}")
        user.set_password(password) 
        user.save()  
        return user 
    
    def create_superuser(self, username, email, PhoneNumber, 
                         password=None):
        if password is None:
            raise TypeError('Password should not be none')  
        
        first_name = "Admin"
        last_name = "User"

        user=self.create_user(username, first_name = first_name, last_name= last_name, email = email, 
                              PhoneNumber = PhoneNumber, password = password)
        user.is_superuser = True
        user.is_staff=True
        user.save()
        return user 

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, unique=True, db_index=True, null=True)
    last_name = models.CharField(max_length=255, unique=True, db_index=True, null=True)
    PhoneNumber = models.IntegerField(unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_sponsorised = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','PhoneNumber', 'first_name', 'last_name']

    objects = UserManager() 

    def __str__(self):
        return self.email 
    
    def tokens(self):
        return ''