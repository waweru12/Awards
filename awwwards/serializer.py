from rest_framework import serializers
from .models import Profile,Project

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'bio')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('user', 'project_name')
