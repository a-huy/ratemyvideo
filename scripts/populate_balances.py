import utils.djangoenv

import accounts.models as am

accounts = am.User.objects.all()

dry_run = True

if raw_input('Dry Run? (Y|n): ') == 'n': dry_run = False

print 'Number of pending updates: %d' % len(accounts)

for user in accounts:
    print 'Updating user %s (%s)...' % (user.real_name, user.fb_id)
    user.balance = user.earned
    try:
        if not dry_run: user.save()
    except Exception as exn:
        print exn
        continue
    print 'Success!'

