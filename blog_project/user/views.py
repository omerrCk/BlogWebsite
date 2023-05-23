from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import UpdateProfileForm,UpdateUserForm
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def profile(request):
    user = request.user
    likedPosts = Post.objects.filter(likes=request.user.id)
    print(likedPosts)
    writtenPosts = Post.objects.filter(author = request.user).order_by('-created')
    template = loader.get_template('profile.html')
    context = {
        'user': user,
        'likedPosts': likedPosts,
        'writtenPosts':writtenPosts,
        'edit': bool(True)
    }
    return HttpResponse(template.render(context, request))

def profile_username(request,username):
    user = User.objects.get(username=username)
    likedPosts = Post.objects.filter(likes=user.id)
    writtenPosts = Post.objects.filter(author = user).order_by('-created')
    template = loader.get_template('profile.html')
    context = {
        'user': user,
        'likedPosts': likedPosts,
        'writtenPosts':writtenPosts,
        'edit': bool(False)
    }
    return HttpResponse(template.render(context, request))

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def profile_edit(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})