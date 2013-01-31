from django.conf import settings
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from django.utils.timezone import now
from django.contrib.auth import logout

import urllib
import accounts.lib.invite as invite_lib
import accounts.lib.user as user_lib
import accounts.models as accounts_models
import videos.models as videos_models
from base.contrib import whitelisted

def login_page(request):
    context_vars = { 'status':'out' }
    context_vars['json_vars'] = {
        'APP_ID': settings.FACEBOOK_APP_ID,
        'DOMAIN': settings.DOMAIN,
        'SCOPE': settings.FACEBOOK_SCOPE,
        'CHANNEL': settings.DOMAIN + 'login/channel/'
    }
    if 'error_reason' in request.GET and request.GET['error_reason'] == 'user_denied':
        context_vars['status'] = 'user_denied'
        return render_to_response('login_page.html', context_vars,
            context_instance=RequestContext(request))
    if 'code' not in request.GET or not request.GET['code']:
        return render_to_response('login_page.html', context_vars,
            context_instance=RequestContext(request))
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': settings.DOMAIN + 'login/',
        'code': request.GET.get('code')
    }
    user = invite_lib.get_user_data(args, request)
    if not whitelisted(user['fb_id']): return redirect('invite_required')
    request.session['fb_id'] = user['fb_id']
    context_vars['status'] = 'in'
    context_vars['name'] = user['real_name']
    return render_to_response('login_page.html', context_vars,
        context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return redirect('/')

def channel(request):
    return render(request, 'channel.html', { })

def invite_required(request):
    context_vars = { 'home_url': settings.DOMAIN }
    return render_to_response('invite_required.html', context_vars,
        context_instance=RequestContext(request))

def user_profile(request, fb_id):
    session = request.session
    if 'fb_id' not in session or session['fb_id'] == -1 or session['fb_id'] != fb_id:
            return HttpResponseForbidden()
    user = get_object_or_404(accounts_models.User, fb_id=fb_id)
    user.referral = accounts_models.InviteRequest.objects.filter(fb_id=fb_id)[0].reason
    po_dates = list(accounts_models.Payout.active.filter(user=user).values_list('created_date', flat=True).order_by('-created_date'))
    po_dates += [user.created_date]
    ratings = videos_models.Rating.active.filter(user=user).order_by('-created_date')[:40]
    avg_po_time = user_lib.avg_payout_time(po_dates)
    apt_str = '%dd, %dh' % (avg_po_time.days, avg_po_time.seconds / 3600) if avg_po_time else ''
    tslp = user_lib.time_since_last_payout(po_dates)
    tslp_str = '%dd, %dh' % (tslp.days, tslp.seconds / 3600) if tslp else ''
    json_vars = {
        'fb_id': str(user.fb_id),
    }
    context_vars = {
        'user': user,
        'ratings': ratings,
        'acc_age': (now() - user.created_date).days,
        'avg_po_time': apt_str,
        'tslp': tslp_str,
        'json_vars': json_vars,
    }
    return render_to_response('profile.html', context_vars,
        context_instance=RequestContext(request))

def profile(request):
    session = request.session
    if 'fb_id' not in session or session['fb_id'] == -1: return redirect('/login/')
    user = get_object_or_404(accounts_models.User, fb_id=session['fb_id'])
    if not whitelisted(user.fb_id): return redirect('invite_required')
    return redirect('/accounts/profile/%s' % session['fb_id'])