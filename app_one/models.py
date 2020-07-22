from django.db import models
from datetime import date, timedelta, datetime
import re
import os

from django.conf import settings

def images_path():
    return os.path.join(settings.STATIC_URL, 'uploads')

EMAIL_RE = re.compile(r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,'
                      r'3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')


# Create your models here.
class UserManager(models.Manager):
    def validate(self, post):
        errors = {}
        if not len(post["first_name"]) > 0:
            errors["first_name"] = "First name should not be empty!"
        if not len(post["last_name"]) > 0:
            errors["last_name"] = "Last name should not be empty!"
        if not EMAIL_RE.match(post['email']):
            errors["email"] = "Email is not valid"
        if not len(post["password"]) > 7:
            errors["password"] = "Password should be at least 8 characters!"
        elif not len(post["password"]) > 0:
            errors["password"] = "Password should not be empty!"
        if not len(post["confirm_password"]) > 0:
            errors["confirm_password"] = "Confirm password should not be empty!"
        elif post["password"] != post["confirm_password"]:
            errors["confirm_password"] = "Password/Confirm password are not equal"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    hash_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __int__(self):
        print(User.first_name);


class FoodType(models.Model):
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecipeManager(models.Manager):
    def validate(self, post):
        errors = {}
        if not len(post["recipe_name"]) > 0:
            errors["recipe_name"] = "Recipe name should not be empty!"
        if not len(post["ingredients"]) > 0:
            errors["ingredients"] = "Ingredients should not be empty!"
        if not len(post["recipe_description"]) > 0:
            errors["recipe_description"] = "Description should not be empty!"
        if not len(post["food_type"]) > 0:
            errors["food_type"] = "Food type should not be empty!"
        if not FoodType.objects.filter(id=int(post["food_type"])).exists():
            errors["food_type"] = "Please choose a valid food type"
        return errors

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=50)
    ingredients = models.TextField()
    recipe_description = models.TextField()
    food_type = models.ForeignKey(FoodType, related_name="recipes", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RecipeManager()

    def __str__(self):
        return self.recipe_name + " " + self.ingredients