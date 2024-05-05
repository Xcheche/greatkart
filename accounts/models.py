from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


# Custom user manager to handle user creation
class MyAccountManager(BaseUserManager):
  # Method to create a regular user
    def create_user(self, first_name, last_name, username, email, password=None):
         # Check if email is provided
        if not email:
            raise ValueError('User must have an email address')
# Check if username is provided
        if not username:
            raise ValueError('User must have an username')
        
  # Create a new user instance
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
 # Set the password and save the user

        user.set_password(password)
        user.save(using=self._db)
        return user
 # Method to create a superuser
    def create_superuser(self, first_name, last_name, username, email, password):
        # Create a regular user first
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            )
 # Set superuser attributes
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
   # Custom user model     
class Account(AbstractBaseUser):
      # Define user fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

# Set the email field as the username field for authentication
    USERNAME_FIELD = 'email'
    # Additional fields required for user creation
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  # Use custom user manager for user creation
    objects = MyAccountManager()

  # Method to get full name of user
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

   
 # Method to represent user as a string (useful for debugging)
    def __str__(self):
        return self.email

 # Check if user has a specific permission (always returns True for superusers)
    def has_perm(self, perm, obj=None):
        return self.is_admin

 # Check if user has permissions to access a given app (always returns True for superusers)
    def has_module_perms(self, add_label):
        return True