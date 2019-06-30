from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    profile_photo = models.ImageField(upload_to = 'images/',blank=True)
    bio = models.TextField(max_length = 50,null = True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.comment

    def save_profile(self):
        self.save()

    @classmethod
    def search_profile(cls, search_term):
        userprofile = Profile.objects.filter(user__icontains = search_term)
        return userprofile

