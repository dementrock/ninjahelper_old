EMAIL_SENDER_ADDRS = 'njmail123@gmail.com'
EMAIL_SENDER_PASSWORD = 'ninjahelper'
ENCRYPT_KEY = '48918daadb5a4cd6bb55cb4f6569d4613e8106c2f9494944b6a3760f6b79eb1df9b7f08b7dfb487fb805e2c2c67902a174f656a747c34357a333647a07b9e4f6'
LOGIN_URL = '/account/login/'
handler404 = 'root.views.error'

DEBUG = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')dpjy@!8i&=((ftb3r#kys9l9n-#t!i70@a$9ye$(&kelpyqnv'

if DEBUG:
    MEDIA_HEADER = '/media'
    ADMIN_MEDIA_PREFIX = '/static/admin'
    WEBSITE_URL = ''
else:
    MEDIA_HEADER = 'http://media.ninjahelper.com'
    ADMIN_MEDIA_PREFIX = 'http://media.ninjahelper.com/admin'
    WEBSITE_URL = 'http://www.ninjahelper.com/'


MAXIMUM_SIZE = 500000
