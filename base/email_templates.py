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

<a href="http://www.facebook.com/profile.php?id=%s">Click here to view their Facebook profile.</a>

To review this and other pending requests, access the RMV Admin.

<a href="%srmvadmin/invites/">Quick Link to Invite Requests List</a>
'''
# This dict maps the type strings to their metadata and template
email_types = {
    'new_invite_request': { 
        'template': NEW_INVITE_REQUEST,
        'subject': 'New Invite Request',
    }
}
