import utils.djangoenv

import accounts.models as am
from base.tasks import send_email

first_po_users = am.User.active.filter(balance__gte=10, pp_email='')
for user in first_po_users:
    send_email('missing_paypal_email', user.email, [user.real_name.split(' ')[0]], sender='paypal@ratemyvideo.co')
