from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import timedelta
from django.contrib import messages
from .models import Post
from datetime import datetime
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

# function to get Ip Adress
def userIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# function to verify the actial Ip address and the previous one
def checkIp(request):
    user = User.objects.get(username = request.user.username)
    try:
        profile = Profile.objects.filter(user = user)[0]
    except:
        profile = Profile.objects.create(user = user, last_ip=userIP(request))
    last_ip = profile.last_ip
    current_ip = userIP(request)
    if current_ip != last_ip:
        profile.last_ip = current_ip
        profile.save()
        messages.warning(request, 'Pay attenction! your actual Ip address is different from the previous one')

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# home views
@login_required
@cache_page(CACHE_TTL)
def home(request):
    checkIp(request)
    posts = Post.objects.all().order_by('-datetime')
    return render(request, 'api/home.html', {'posts': posts, 'title' : 'Home'})

# views for instruction
def django_project(request):
    return render(request, 'api/django_project.html',{'title' : 'Instructions'})

#json response
def json(request):
    response = []
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=4)
    posts = Post.objects.filter(datetime__range=(one_hour_ago, now))
    for post in posts:
        response.append(
            {
            'author' : f"{post.user.first_name} {post.user.last_name}",
            'datetime' : post.datetime,
            'content' : post.content,
            'Hash' : post.hash,
            'TxId' : post.txId
            }
        )
    return render(request,'api/json.html', {'json': JsonResponse(response),'title' : 'Json'} )

#word research for user
def research(request):
    if request.GET.get('string'):
        string = request.GET.get('string')
    else:
        string = ''
    posts = Post.objects.all()
    words = ''
    for post in posts:
        words += post.content
        words += post.title
    i = words.count(string)
    return render(request, 'api/research.html', {'string' : string , 'i': i, 'title' : 'Research'})
