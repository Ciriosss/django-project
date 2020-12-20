from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, PostForm
from datetime import datetime
from api.utils import sendTransaction
from api.models import Post
from django.db.models import Count
import hashlib
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

def userIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#views for registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Congratulations {}! your account has been created successfully, now you are able to log-in'.format(username))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render (request, 'users/register.html', {'form' : form, 'title' : 'Registration'})

#section for admin-users
def adminArea(request):

    users = User.objects.all()
    u_posts = User.objects.annotate(total_posts=Count('post'))
    return render(request, "users/adminArea.html", {'users': users, 'u_posts': u_posts, 'title' : 'Admin Area' })

#views for login
@login_required
def profile(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.datetime = datetime.now()
            post.hash = hashlib.sha256(post.content.encode('utf-8')).hexdigest()
            post.txId = sendTransaction(post.hash)
            if form.hack_control():
                post.save()
                return redirect('home')
            else:
                messages.warning(request, 'Sorry you cannot publish a post with the word hack')
                return redirect('profile')
    else:
        post_form = PostForm()
    user_posts = Post.objects.filter(user = request.user.id).order_by('-datetime')
    return render(request, 'users/profile.html', {'post_form': post_form, 'user_posts': user_posts, 'title' : 'Profile'})

#private page for each user
def user_id(request, id):

    user = get_object_or_404( User, id = id)
    user_posts = Post.objects.filter(user = user.id)
    return render(request, "users/user_id.html", {'user':user, 'user_posts': user_posts, 'title' : 'User Page'})
