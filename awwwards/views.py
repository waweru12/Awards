from django.shortcuts import render, redirect
from .models import Project, Profile, Rating
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import  ProfileForm, NewProjectForm, RatingForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly

@login_required(login_url='/accounts/login/')
def home(request):
    projects = Project.get_all_projects()

    return render(request, 'index.html', {"projects": projects})


@login_required(login_url='/accounts/login/')
def upload(request):
    current_user = request.user
    # try:
    #     current_profile = Profile.objects.get(user_id=id)
    # except ObjectDoesNotExist:
    #     return redirect(update_profile, current_user.id)

    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect(home)

    else:
        form = NewProjectForm()
    return render(request, 'new-project.html', {"form": form, "user": current_user})


@login_required(login_url="/accounts/login/")
def profile(request,id):

    current_user = request.user
    user = User.objects.get(id=id)
    profile = Profile.objects.all()
    try:
      profile3 = Profile.objects.filter(name_id=id)
    except ObjectDoesNotExist:
      return redirect() 
    return render(request, 'profile.html', {"user":user, "profile":profile3, "profile":profile})

@login_required(login_url='/accounts/login')
def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profiles = User.objects.filter(username__icontains=search_term)
        profile = Profile.objects.all()
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message, "profile":searched_profiles, "profile":profile})
    else:
        message = "You haven't searched for any term."
        return render(request, 'search.html', {"message":message})

@login_required(login_url='/accounts/login/')
def rating(request, id):
    current_user = request.user
    rating = Rating.objects.filter(project_id=id)
    profile = Profile.objects.all()
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        print('noo')
        form = RatingForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project = project
            rating.user = current_user
            rating.name_id = current_user.id
            rating.save()
        return redirect(home)

    else:
        form = RatingForm()
        print('xyz')
    return render(request, 'review.html', {"form": form, 'user': current_user, 'profile':profile, 'project':project, 'rating':rating})

class ProjectList(APIView):
   def get(self, request, format=None):
       all_project = Project.objects.all()
       serializers = ProfileSerializer(all_profile, many=True)
       return Response(serializers.data)

   def post(self, request, format=None):
       serializers = ProjectSerializer(data=request.data)
       if serializers.is_valid():
           serializers.save()
           return Response(serializers.data, status=status.HTTP_201_CREATED)
       return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
   permission_classes = (IsAdminOrReadOnly,)


class ProjectDescription(APIView):
   permission_classes = (IsAdminOrReadOnly,)

   def get_project(self, pk):
       try:
           return Project.objects.get(pk=pk)
       except Project.DoesNotExist:
           return Http404

   def get(self, request, pk, format=None):
       project = self.get_project(pk)
       serializers = ProjectSerializer(project)
       return Response(serializers.data)

   def put(self, request, pk, format=None):
       project = self.get_project(pk)
       serializers = ProjectSerializer(project, request.data)
       if serializers.is_valid():
           serializers.save()
           return Response(serializers.data)

       else:
           return Response(serializers.errors,
                           status=status.HTTP_400_BAD_REQUEST)

   def delete(self, request, pk, format=None):
       project = self.get_project(pk)
       project.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)

# Profile serializer
class ProfileList(APIView):
   def get(self, request, format=None):
       all_profile = Profile.objects.all()
       serializers = ProfileSerializer(all_profile, many=True)
       return Response(serializers.data)

   def post(self, request, format=None):
       serializers = ProfileSerializer(data=request.data)
       if serializers.is_valid():
           serializers.save()
           return Response(serializers.data, status=status.HTTP_201_CREATED)
       return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
   permission_classes = (IsAdminOrReadOnly,)


class ProfileDescription(APIView):
   permission_classes = (IsAdminOrReadOnly,)
   def get_profile(self, pk):
       try:
           return Profile.objects.get(pk=pk)
       except Profile.DoesNotExist:
           return Http404

   def get(self, request, pk, format=None):
       profile = self.get_profile(pk)
       serializers = ProfileSerializer(profile)
       return Response(serializers.data)


   def put(self, request, pk, format = None):
       profile = self.get_profile(pk)
       serializers = ProfileSerializer(profile, request.data)
       if serializers.is_valid():
           serializers.save()
           return Response(serializers.data)

       else:
           return Response(serializers.errors,
                           status = status.HTTP_400_BAD_REQUEST)

   def delete(self, request, pk, format=None):
       profile = self.get_profile(pk)
       profile.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)
