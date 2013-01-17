from decimal import *
import datetime
import re

from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from django.core.cache import cache

import videos.models as videos_models
import accounts.models as accounts_models
import base.contrib
import base.cache_keys as keys
from base.decorators import pagecache
import rmvadmin.lib.views as views_lib
from rmvadmin.forms import CSVForm

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
    col_filter = request.GET.get('filter', 'id')
    filter_rev = True if 'rev' in request.GET else False
    videos_all = videos_models.Video.active.all()
    ratings = videos_models.Rating.active.all()
    try:
        num_per_page = int(request.GET.get('num', len(videos_all)))
    except ValueError: num_per_page = len(users_all)
    page = request.GET.get('page')

    getcontext()
    for vid in videos_all:
        rating_matches = filter(lambda x: x.video_id == vid.id, ratings)
        vid.count = len(rating_matches)
        if len(rating_matches) == 0: vid.avg_rating = 0
        else: vid.avg_rating = \
            round(Decimal(sum([x.rating for x in rating_matches])) / Decimal(len(rating_matches)), 3)

    videos_all = sorted(videos_all, key=lambda x: getattr(x, col_filter), reverse=filter_rev)
    paginator = Paginator(videos_all, num_per_page)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger: videos = paginator.page(1)
    except EmptyPage: videos = paginator.page(paginator.num_pages)

    context_vars = {
        'videos': videos,
        'filter': col_filter,
        'rev': filter_rev,
        'num': num_per_page
    }
    return render_to_response('list_videos.html', context_vars,
        context_instance=RequestContext(request))

@login_required
def list_users(request):
    col_filter = request.GET.get('filter', 'id')
    filter_rev = True if 'rev' in request.GET else False
    users_all = accounts_models.User.active.all()
    try:
        num_per_page = int(request.GET.get('num', len(users_all)))
    except ValueError: num_per_page = len(users_all)
    page = request.GET.get('page')
    inv_requests = accounts_models.InviteRequest.objects.all().order_by('-created_date')
    for user in users_all:
        invites = filter(lambda x: x.fb_id == user.fb_id, inv_requests)
        user.referral = invites[0].reason if invites else 'None'
        user.tslr = base.contrib.time_since_last_rating(user.pk)
    users_all = sorted(users_all, key=lambda x: getattr(x, col_filter), reverse=filter_rev)
    paginator = Paginator(users_all, num_per_page)
    try:
        users = paginator.page(page)
    except PageNotAnInteger: users = paginator.page(1)
    except EmptyPage: videos = paginator.page(paginator.num_pages)

    if 'export' in request.GET:
        return views_lib.export_users_list_to_xlsx(users.object_list)

    json_vars = {
        'filter': str(col_filter),
        'rev': 'true' if filter_rev else 'false'
    }

    context_vars = {
        'json_vars': json_vars,
        'users': users,
        'filter': col_filter,
        'rev': filter_rev,
        'num': num_per_page,
        'total_active': len(filter(lambda x: x.rated > 0, users_all)),
        'total_payout': len(filter(lambda x: x.balance >= settings.MINIMUM_PAYOUT_AMOUNT, users_all)),
        'total_users': len(users_all),
        'daily_count': views_lib.get_daily_user_count(),
        'minimum_payout': settings.MINIMUM_PAYOUT_AMOUNT
    }
    return render_to_response('list_users.html', context_vars,
        context_instance=RequestContext(request))

@login_required
def user_info(request, fb_id):
    try:
        user = accounts_models.User.active.get(fb_id=fb_id)
        user.referral = accounts_models.InviteRequest.objects.filter(fb_id=fb_id)[0].reason
    except accounts_models.User.DoesNotExist:
        return redirect(list_users)
    except IndexError: user.referral = 'None'
    videos_all = videos_models.Video.objects.all()
    queue = videos_models.Queue.active.filter(user_id=user.id)
    ratings = videos_models.Rating.active.filter(user_id=user.id).order_by('-created_date')
    votes = videos_models.Vote.active.filter(user_id=user.id)
    acc_age = now() - user.created_date

    for vid in queue:
        video = filter(lambda x: x.id == vid.video_id, videos_all)[0]
        vid.title = video.title
        vid.yt_id = video.yt_id
        vid.reward = video.reward

    for entry in ratings:
        video = filter(lambda x: x.id == entry.video_id, videos_all)[0]
        entry.title = video.title
        entry.yt_id = video.yt_id
        vote = filter(lambda x: x.video_id == entry.video_id, votes)
        if vote: entry.liked = 't' if vote[0].like else 'f'

    json_vars = {
        'verified': str(user.verified),
        'fb_id': str(user.fb_id)
    }
    context_vars = {
        'user': user,
        'queue': queue,
        'ratings': ratings,
        'votes': votes,
        'acc_age': acc_age.days,
        'json_vars': json_vars
    }
    return render_to_response('user_info.html', context_vars,
        context_instance=RequestContext(request))

@pagecache('rmvadmin:edit:user:%s')
@login_required
def edit_user(request, fb_id):
    try:
        user = accounts_models.User.active.get(fb_id=fb_id)
    except accounts_models.User.DoesNotExist: return redirect(list_users)
    context_vars = {
        'json_vars': { 'fb_id': str(user.fb_id) },
        'user': user
    }
    return render_to_response('edit_user.html', context_vars,
        context_instance=RequestContext(request))

@pagecache('rmvadmin:payout:%s')
@login_required
def payout(request, fb_id):
    try:
        user = accounts_models.User.active.get(fb_id=fb_id)
        payouts = accounts_models.Payout.active.filter(user=user).order_by('-created_date')
    except accounts_models.User.DoesNotExist: return redirect(list_users)
    context_vars = {
        'user': user,
        'payouts': payouts,
        'json_vars': { 'fb_id': str(user.fb_id) }
    }
    return render_to_response('payout.html', context_vars,
        context_instance=RequestContext(request))

@login_required
def add_video(request):
    return render_to_response('add_video.html', { },
        context_instance=RequestContext(request))

@login_required
def whitelist(request):
    return render_to_response('whitelist.html', { },
        context_instance=RequestContext(request))

@login_required
def invites(request):
    inv_requests = accounts_models.InviteRequest.active.all()
    context_vars = {
        'invite_requests': inv_requests
    }
    return render_to_response('invites.html', context_vars,
        context_instance=RequestContext(request))

@login_required
def user_stats(request, fb_id):
    try:
        user = accounts_models.User.active.get(fb_id=fb_id)
    except accounts_models.User.DoesNotExist: return redirect(list_users)
    ratings = videos_models.Rating.active.filter(user_id=user.id)
    ratings_dates = views_lib.count_by_date(ratings.values_list('created_date', flat=True))
    ratings_sums = views_lib.sum_by_date(ratings.values_list('created_date', 'video__reward'))
    json_vars = {
        'rdates': ratings_dates,
        'rsums': ratings_sums
    }
    context_vars = {
        'json_vars': json_vars,
        'user': user
    }
    return render_to_response('user_stats.html', context_vars,
        context_instance=RequestContext(request))

@login_required
def site_stats(request):
    now_ts = now()
    date_today = '%s-%s-%s' % (now_ts.month, now_ts.day, now_ts.year)
    rdates_key = keys.RMV_RATING_DATES % date_today
    rsums_key = keys.RMV_RATING_SUMS % date_today
    udates_key = keys.RMV_USER_DATES % date_today
    ustates_key = keys.RMV_USER_STATES % date_today

    ratings = cache.get(rdates_key)
    if not ratings:
        values = videos_models.Rating.active.values_list('created_date', flat=True)
        ratings = views_lib.count_by_date(values)
        cache.set(rdates_key, ratings)

    users_dates = cache.get(udates_key)
    if not users_dates:
        values = accounts_models.User.active.values_list('created_date', flat=True)
        users_dates = views_lib.count_by_date(values)
        cache.set(udates_key, users_dates)

    users_states = cache.get(ustates_key)
    if not users_states:
        values = accounts_models.User.active.values_list('location', flat=True)
        users_states = views_lib.count_by_state(values)
        cache.set(ustates_key, users_states)

    ratings_sums = cache.get(rsums_key)
    if not ratings_sums:
        values = videos_models.Rating.active.values_list('created_date', 'video__reward')
        ratings_sums = views_lib.sum_by_date(values)
        cache.set(rsums_key, ratings_sums)

    json_vars = {
        'rdates': ratings,
        'udates': users_dates,
        'ustates': users_states,
        'rsums': ratings_sums
    }
    context_vars = {
        'json_vars': json_vars
    }
    return render_to_response('site_stats.html', context_vars,
        context_instance=RequestContext(request))

@login_required
def masspay_csv(request):
    po_users = accounts_models.User.active.filter(balance__gte=settings.MINIMUM_PAYOUT_AMOUNT)
    return views_lib.export_masspay_csv(po_users)

@login_required
def mass_payout(request):
    po_dict = None
    users = []
    error_msgs = []
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            po_dict = views_lib.process_csv(request.FILES['csvfile'])
    else: form = CSVForm()
    if po_dict:
        users = accounts_models.User.active.filter(fb_id__in=po_dict.keys())
        for user in users:
            try: user.po_amount = po_dict[user.fb_id]
            except KeyError:
                error_msgs.append('There was an error processing payout information for %s' % user.real_name)
                user.po_amount = 0
    context_vars = {
        'form': form,
        'po_users': users,
        'error_msgs': error_msgs
    }
    return render_to_response('upload_masspay.html', context_vars,
        context_instance=RequestContext(request))