# api/models.py
from django.db import models
from django.contrib.auth.hashers import make_password

class UserInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # store hashed password

  # Default created datetime
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # Ensure password is hashed before saving
        if not self.password.startswith("pbkdf2_"):  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
