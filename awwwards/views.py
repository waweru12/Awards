from django.shortcuts import render, redirect
from .models import Project, UsabilityRating, ContentRating, DesignRating, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import NewProjectForm, DesignForm, UsabilityForm, ContentForm
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
    return render(request, 'profile.html', { "user":user, "profile":profile3, "profile":profile})

@login_required(login_url='/accounts/login')
def add_usability(request, project_id):
    rati = UsabilityRating.objects.filter(project_id=project_id)
    project = Project.objects.get(pk=project_id)
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = UsabilityForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project = project
            rating.user = request.user
            rating.save()
        return redirect('homePage')
    else:
        form = UsabilityForm()

    return render(request, 'operable.html',locals())

@login_required(login_url='/accounts/login')
def add_design(request, project_id):
    rato = DesignRating.objects.filter(project_id=project_id)
    project = Project.objects.get(pk=project_id)
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = DesignForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project = project
            rating.user_name = request.user
            rating.save()
        return redirect('homePage')
    else:
        form = DesignForm()
    return render(request, 'outline.html',locals())

@login_required(login_url='/accounts/login')
def add_content(request,  project_id):
    rates = ContentRating.objects.filter(project_id=project_id)
    project = Project.objects.get(pk=project_id)
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project = project

            rating.user_name = request.user
            rating.save()

        return redirect('homePage')
    else:
        form = ContentForm()

    return render(request, 'text.html',locals())

@login_required(login_url='/accounts/login')
def search_results(request):
    profile= Profile.objects.all()
    project= Project.objects.all()
    if 'Project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_project = Project.search_by_profile(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',locals())

    else:
        message = "You haven't searched for any term"
        return render(request,'search.html',{"message":message})


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
