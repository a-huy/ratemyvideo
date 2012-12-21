import datetime

# fb_id, real_name, email, location, age, gender, reason, fb_id, domain
NEW_INVITE_REQUEST = '''
Someone has submitted a request to use the Rate My Video service.

Facebook ID: %s
Name: %s
Email: %s
Location: %s
Age: %d
Gender: %s
Referral: %s

Click below to view their Facebook profile.
http://www.facebook.com/profile.php?id=%s

To review this and other pending requests, access the RMV Admin:
%srmvadmin/invites/
'''

# real_name, domain, email
WELCOME_USER = '''
Hey %s,

Welcome to Rate My Video! We're excited about your interest in using our service.

Rate My Video runs through a Google Chrome extension, so you will need to be running Google Chrome as your web browser (instead of FireFox, Safari, or Internet Explorer).
You can download Google Chrome through the following link:
http://www.google.com/chrome/

Next, you must download and install our Chrome extension.
You can do so by navigating to our home page and clicking on the Install link:
%s

Once you have earned $10, we will contact you via your email address used to login with Facebook (%s) in order to request your PayPal account information so we can send you your MONEY!

We look forward to you helping us find the next viral sensation!

Thanks,
The Rate My Video Team
'''

# real_name
CONFIRM_INVITE = '''
Hello %s,

Thank you for your interest in Rate My Video!
This is an email to confirm that you sent us a request for an invitation to use
our service.

We will process your request as soon as possible!

Thank you,
The Rate My Video Team
'''

# User list
PAYOUT_ELIGIBLE = '''
The following users are eligible for a payout:

Name (Email): Balance
------------------------------
%s

This is an automatically generated email sent every day.
'''

# real_name
MISSING_PAYPAL_EMAIL = '''
Hey %s,

You've made it to your first payout from Rate My Video! Congratulations!

We need your PayPal email address to send you your earnings. Can you please reply to this email with your PayPal account email address and the name that appears on your Facebook profile?

If you prefer, you can also send an email to paypal@ratemyvideo.co with this info.

Once you do this, we will send your earnings as soon as possible. 

Thanks and Happy Rating!
The Rate My Video Team
'''

# This dict maps the type strings to their metadata and template
email_types = {
    'new_invite_request': {
        'template': NEW_INVITE_REQUEST,
        'subject': 'New Invite Request',
    },
    'welcome_user': {
        'template': WELCOME_USER,
        'subject': 'Welcome to Rate My Video!'
    },
    'confirm_invite': {
        'template': CONFIRM_INVITE,
        'subject': 'Rate My Video - Invitation Request Confirmation'
    },
    'payout_eligible': {
        'template': PAYOUT_ELIGIBLE,
        'subject': datetime.datetime.today().strftime('%d-%m-%y') + ' | Daily User Balance Check'
    },
    'missing_paypal_email': {
        'template': MISSING_PAYPAL_EMAIL,
        'subject': 'Rate My Video - Payout Reached!'
    }
}
