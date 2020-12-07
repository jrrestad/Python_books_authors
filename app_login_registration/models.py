from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def validatorRegister(self, postData):
        errors = {}
        email = postData['email']
        emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['firstName']) < 2:
            errors['firstName'] = "First name is required"
        if postData['firstName'].isalpha() == False:
            errors['firstName2'] = "First name must contain only alphabetical characters"
        if len(postData['lastName']) < 2:
            errors['lastName'] = "Last name is required"
        if postData['lastName'].isalpha() == False:
            errors['lastName2'] = "Last name must contain only alphabetical characters"
        if not emailRegex.match(postData['email']):
            errors['email'] = "Email must have a valid format <johndoe@email.com>"
        if User.objects.filter(email=email):
            errors['emailInUse'] = "Email is already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirmPassword']:
            errors['passwordMatch'] = "Passwords do not match"
        return errors

    def validatorLogin(self, postData):
        errors = {}
        email = postData['email']
        if not User.objects.filter(email=email):
            errors['email'] = "Email or password was invalid"
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=26)
    lastName = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()