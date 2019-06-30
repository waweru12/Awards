from .models import Project,DesignRating,UsabilityRating,ContentRating
from django import forms
from django.forms import ModelForm, Textarea, IntegerField


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']


class ContentForm(forms.ModelForm):
    class Meta:
        model = ContentRating
        fields = ['rating','user']


class UsabilityForm(forms.ModelForm):
    class Meta:
        model = UsabilityRating
        fields = ['rating','user']


class DesignForm(forms.ModelForm):
    class Meta:
        model = DesignRating
        fields = ['rating','user']
