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
You can do so by navigating to the following page:
%sextension/get/

Follow these steps to install the Chrome extension manually:
1. There is an icon in the top right corner of the Chrome browser that has 3 bars.
   Click this icon to access the browser menu.
2. Select Tools >> Extensions.
   Alternatively, you can reach the extensions menu by typing "chrome://extensions"
   (without the quotation marks) in the address bar and pressing Enter.
3. Right click on the .crx extension file you just downloaded
   (it should show up at the bottom in the download bar) and click on "Show in Folder".
   If you are using Mac OS, it should say "Show in Finder" instead.
   Drag the file onto the Extensions page.
4. Review the list of permissions in the dialog that appears and click Install.

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
    }
}
