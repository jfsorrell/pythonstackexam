from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, form):
        errors = []

        if len(form['first_name']) < 3:
            errors.append('First name must be at least 3 characters long')
        if len(form['last_name']) < 3:
            errors.append('Last name must be at least 3 characters long')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('Email must be valid')
        if len(form['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        try:
            self.get(email=form['email'])
            errors.append('Email already in use')
        except:
            pass

        return errors

    def create_user(self, user_data):
        # hash the user's password
        pw_hash = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())
        # create user
        user = self.create(
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        email=user_data['email'],
        pw_hash=pw_hash
        )
        return user

    def login(self, form):
        # find the user with the given email address
        user_list = self.filter(email=form['email'])
        if len(user_list) > 0:
        # email found
            user = user_list[0]
            if bcrypt.checkpw(form['password'].encode(), user.pw_hash.encode()):
                # email and password match
                return (True, user.id)
            else:
                # password does not match
                return (False, "Email or password incorrect.")
        else:
        # email not found
            return (False, "Email or password incorrect.")

class QuoteManager(models.Manager):
    def validate(self, form):
        errors = []

        if len(form['author']) < 3: 
            errors.append('Quote must have an author')
        if len(form['quote']) < 10:
            errors.append('Quote must have at least 10 characters')
    
        try:
            self.get(quote=form['quote'])
            errors.append('Quote already exists')
        except:
            pass

        return errors
    
    def addquote(self, quote_id, user_id):
            quote = self.get(id=quote_id)
            user = User.objects.get(id=user_id)
            quote.users_added.add(user)
            quote.save()
    

class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  pw_hash = models.CharField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()
  def __str__(self):
    email = self.email
    return email

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="quote")
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    def __str__(self):
        author = self.author
        return author

class Like(models.Model):
    userliked = models.ForeignKey(User, related_name="quotesliked")
    likedquotes = models.ForeignKey(User, related_name="likedusers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    def __str__(self):
        author = self.author
        return author