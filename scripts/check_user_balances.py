import utils.djangoenv

import accounts.models as am
from base.tasks import backend_email

accounts = am.User.active.all()

payout_list = []
list_str = ''

list_ind = 1
for user in accounts:
    if user.balance >= 10:
        list_str += '%3d. %s (%s): $%s\n' % (list_ind, user.real_name, user.email, str(user.balance))
        list_ind += 1

if list_str: backend_email('payout_eligible', 'managers', [list_str])
