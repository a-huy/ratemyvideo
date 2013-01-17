from celery import task
import datetime
import itertools
import random
import base.email_templates as emails
import base.cache_keys as cache_keys
import base.contrib as bc
import accounts.models as am
import videos.models as vm
from accounts.lib.invite import is_inside_us
from django.core.mail import send_mail, mail_admins, mail_managers, BadHeaderError
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now

# Send an email with a specified template
@task()
def send_email(template_name, recipient, email_args, sender=settings.SERVER_EMAIL):
    if template_name not in emails.email_types:
        raise LookupError('Email template type not supported')
    template = emails.email_types[template_name]['template']
    try:
        send_mail(emails.email_types[template_name]['subject'],
                       template % tuple(email_args), sender, [recipient])
    except TypeError:
        raise TypeError('One or more email arguments are invalid')
    except BadHeaderError:
       raise BadHeaderError('Invalid header found.')

# Send an email to the admins, managers, or both
@task()
def backend_email(template_name, group_type, email_args):
    if template_name not in emails.email_types:
        raise LookupError('Email template type not supported')
    template = emails.email_types[template_name]['template']
    subject = emails.email_types[template_name]['subject']
    try:
        message = template % tuple(email_args)
        if 'admins' in group_type: mail_admins(subject, message)
        if 'managers' in group_type: mail_managers(subject, message)
    except TypeError:
        raise TypeError('One or more email arguments are invalid')
    except BadHeaderError:
       raise BadHeaderError('Invalid header found.')

@task()
def check_user_balances():
    accounts = am.User.active.filter(balance__gte=settings.MINIMUM_PAYOUT_AMOUNT)
    payout_list = []
    list_str = ''
    for argi, user in enumerate(accounts):
        list_str += '%3d. %s (%s): $%s\n' % (argi + 1, user.real_name, user.email, str(user.balance))
    if list_str: backend_email('payout_eligible', 'managers', [list_str])

@task()
def invalidate_charts():
    yts = now() - datetime.timedelta(days=1)
    yesterday = '%s-%s-%s' % (yts.month, yts.day, yts.year)
    cache.delete(cache_keys.RMV_RATING_DATES % yesterday)
    cache.delete(cache_keys.RMV_RATING_SUMS % yesterday)
    cache.delete(cache_keys.RMV_USER_DATES % yesterday)
    cache.delete(cache_keys.RMV_USER_STATES % yesterday)

@task()
def update_queues():
    def create_entry(user, vid, time, bonuses):
        fields = {
            'user_id': user.id,
            'video_id': vid,
            'expire_date': time.replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1),
            'bonuses': bonuses
        }
        return vm.Queue(**fields)

    DEFAULT_LIMIT = settings.DEFAULT_VIDEO_QUEUE_LIMIT
    accounts = am.User.active.all()
    ratings = vm.Rating.active.all()
    videos = vm.Video.active.all()
    cores = list(videos.filter(tags__contains='core').values_list('id', flat=True))
    verified = list(videos.filter(tags__contains='verified').values_list('id', flat=True))
    rest = list(videos.exclude(tags__contains='verified').values_list('id', flat=True))
    curr_time = now()

    # Clear the table of any expired videos
    vm.Queue.active.filter(expire_date__lte=curr_time).delete()
    # Then, grab all the queue items that remain
    curr_queue = vm.Queue.active.all()

    for user in accounts:
        cache.delete(cache_keys.ACC_USER_QUEUE % user.fb_id)
        USER_LIMIT = 30 if user.verified else DEFAULT_LIMIT
        vid_ids = set(list(ratings.filter(user=user).values_list('video__id', flat=True)) + \
            list(curr_queue.filter(user=user).values_list('video__id', flat=True)))
        pool = [x for x in (rest + (verified if user.verified else [])) if x not in vid_ids]
        random.shuffle(pool)
        queue = []
        bonuses = '' if is_inside_us(user.location) else 'intl'
        for vid in ([x for x in cores if x not in vid_ids] + pool)[:USER_LIMIT]:
            queue.append(create_entry(user, vid, curr_time, bonuses))
        if queue: vm.Queue.objects.bulk_create(queue)

# Calculate time since last rating for all users (so the values will be ready in cache)
@task()
def calc_all_tslr():
    users_all = am.User.active.all()
    for user in users_all: bc.time_since_last_rating(user.pk)