from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    profile_pic = models.ImageField(upload_to = 'images/')
    bio = models.CharField(max_length=250)
    
    def __str__(self):
        return self.bio

          
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, search_term):
        userprofile = Profile.objects.filter(user__icontains = search_term)
        return userprofile

class Project(models.Model):
    image = models.ImageField(upload_to = 'images/')
    project_name = models.CharField(max_length =10)
    project_url = models.CharField(max_length =50)
    user= models.ForeignKey(User,on_delete=models.CASCADE)

    def save_project(self):
        self.save()
    
   
    @classmethod
    def get_all_projects(cls):
        project = cls.objects.all()
        return project

    @classmethod
    def find_project_id(cls, id):
        project_result = cls.objects.get(project_id=id)
        return project_result
# START OF THE CLASSES FOR RATING 

class DesignRating(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10')
    )
    project = models.ForeignKey('Project')
    user = models.ForeignKey(User)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)
    
class UsabilityRating(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10')
    )
    project = models.ForeignKey('Project')
    user = models.ForeignKey(User)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)
    

class ContentRating(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10')
    )
    project = models.ForeignKey('Project')
    user = models.ForeignKey(User)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)
    

