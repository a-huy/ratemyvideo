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

# real_name, domain
WELCOME_USER = '''
Hey %s,

Welcome to Rate My Video! We're excited about your interest in using our service.

In order to start using the service, you must download and install our Chrome extension.
You can do so by navigating to the following page:
%sextension/get/

Follow these steps to install the Chrome extension:
1.
2.
3.
4.

Thanks,
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
    }
}
