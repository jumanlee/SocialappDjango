from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# Create your models here.

class AppUserManager(BaseUserManager):
    #code based on Django's main project github (guide)'s instructions: https://github.com/django/django/blob/main/django/contrib/auth/models.py#L128
    def create_user(self, email, username, firstname, lastname, password, **extra_fields):
        if not email:
            raise ValueError('Please provide an appropriate email address')

        #Normalize ensures that the email address is in a consistent format by lowercasing the domain name and removing any spaces or other characters. This can be useful in preventing errors when searching or sorting data by email address. It's from BaseUserManager.
        email = self.normalize_email(email)

        # is_staff is a built-in boolean attribute of the Django User model
        extra_fields.setdefault("is_staff", False)

        extra_fields.setdefault("is_superuser", False)

        # self.model refers to the user model that is being managed by the manager class. this model is the AppUser model below, which references objects = AppUserManager().
        appuser = self.model(email=email, username=username, firstname=firstname, lastname=lastname, **extra_fields)

        appuser.set_password(password)

        appuser.save()

        return appuser

    #code taken from Django's main project github (guide)'s instructions: https://github.com/django/django/blob/main/django/contrib/auth/models.py#L128 Basically BaseUserManager does not have any method called create_superuser, so its necessary to add this, otherwise would have error when doing python manage.py createsuperuser to create super user. Please see: https://stackoverflow.com/questions/54989276/user-manager-object-has-no-attribute-create-superuser
    def create_superuser(self, email, username, firstname, lastname, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, firstname, lastname, password, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)

    objects = AppUserManager()

    #  email is not included in REQUIRED_FIELDS because it is already defined as the USERNAME_FIELD, 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname']
    EMAIL_FIELD = 'email'

    # same as __unicode__(self) is used in Python 2.x. We overwrite the string dunder method
    def __str__(self):
        return self.email

    # this default get username allows you to get username, this is provided by default django
    # get_username()

    # The __str__(self) and __unicode__(self) methods are special methods in Python that allow you to define how an object should be represented as a string. These methods are called implicitly when the object is used in a context that requires a string representation, such as when it is printed or concatenated with other strings.

    # The get_full_name() method, on the other hand, is not a special method in Python. It is a method defined by Django's AbstractBaseUser model that is used to return a string representing the user's full name. However, since get_full_name() is not a special method, it will not be called implicitly when the object is used in a context that requires a string representation. Instead, you would need to call it explicitly (e.g. user.get_full_name()).
    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"


class Friendship(models.Model):
    #[self]one to one field cuz one appuser can only have one entry appuser. Note that one row/entry represents one "friend list" for the relevant appuser
    appuser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appiuser")

    #[self]appfriends links to all the appuser's friends, which are also in the AppUser class. A many-to-many relationship in Django is typically represented as a join table in the database. This join table has two foreign key columns that reference the two models involved in the relationship. In this case, the join table has two foreign key columns that reference the Friendship model and the AppUser model, respectively. When you add a AppUser instance to the appfriends field of a Friendship instance, Django automatically creates a new row in the join table that links the two instances. Similarly, when you remove a User instance from the appfriends field, Django removes the corresponding row from the join table. When you access the appfriends field of a Friendship instance, Django automatically performs a database query to retrieve all of the User instances that are linked to that Friendship instance through the join table. This is many to many because one friendlist instance can be associated to many AppUser class instances. And one AppUser class instance can be associated with many friendlist instances. 
    appfriends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="appfriends")

    def __str__(self):
        return self.appuser.email

    def username(self):
        return self.appuser.username

class AddRequest(models.Model):
    #[self] foreignkey rather one to one cuz one AppUser instance can have many userfrom entries (more like one to many) in the table.
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_from")

    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_to")

    date_time = models.DateTimeField(auto_now_add=True)

    ongoing = models.BooleanField(blank=False, default=True, null=False)

    def __str__(self):
        return user_from.email



