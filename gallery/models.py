from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    failed_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(
        null=True,
        blank=True
    )
    def __str__(self):
        return self.username

class UserFile(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE,null=True,blank=True)
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title