import utils.djangoenv

import accounts.models as am
from base.contrib import backend_email

accounts = am.User.active.all()

payout_list = []
list_str = ''

for user in accounts:
    if user.balance > 10:
        list_str += user.real_name + ' (' + user.email + '): $' + str(user.balance) + '\n'

if list_str: backend_email('payout_eligible', 'managers', [list_str])
