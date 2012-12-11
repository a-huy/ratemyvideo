import utils.djangoenv

import accounts.models as am

users = am.User.objects.all()

dry_run = True

if raw_input('Dry Run? (Y|n): ') == 'n': dry_run = False

print 'Number of pending updates: %d' % len(users)

for user in users:
    print 'Updating user %s (%s)...' % (user.real_name, user.fb_id)
    user.pp_email = user.email
    try:
        if not dry_run: user.save()
    except Exception as exn:
        print exn
        continue
    print 'Success!'

