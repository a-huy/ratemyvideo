from decimal import *
from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import videos.models as videos_models

@login_required
def home(request):
    return render_to_response('home.html', { },
        context_instance=RequestContext(request))

def rmv_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.POST['next'])
    return render_to_response('login.html', { }, 
        context_instance=RequestContext(request))

def rmv_logout(request):
    logout(request)
    return redirect('/')

@login_required
def list_videos(request):
    videos_all = videos_models.Video.active.all().order_by('id')
    num_per_page = request.GET.get('num', len(videos_all))
    page = request.GET.get('page')
    paginator = Paginator(videos_all, num_per_page)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger: videos = paginator.page(1)
    except EmptyPage: videos = paginator.page(paginator.num_pages)

    ratings = videos_models.Rating.active.all()
    counts = { }
    avg_ratings = { }
    for rating in ratings:
        vid = rating.video_id
        video_matches = filter(lambda x: x.id == vid, videos)
        yt_id = '' if not video_matches else video_matches[0].yt_id
        counts[yt_id] = 1 if yt_id not in counts else counts[yt_id] + 1
    getcontext()
    for vid in videos:
        rating_matches = filter(lambda x: x.video_id == vid.id, ratings)
        if len(rating_matches) == 0: continue
        avg_ratings[vid.yt_id] = \
            Decimal(sum([x.rating for x in rating_matches])) / Decimal(len(rating_matches))
    context_vars = {
        'videos': videos,
        'counts': counts,
        'avg_ratings': avg_ratings
    }
    return render_to_response('list_videos.html', context_vars,
        context_instance=RequestContext(request))

def add_video(request):
    return render_to_response('add_video.html', { },
        context_instance=RequestContext(request))

@login_required
def edit_whitelist(request):
    return HttpResponse()
