"""
Django settings for vs project.

"""

import os
from django.conf.global_settings import EMAIL_HOST_PASSWORD
from django.conf.locale.en import formats as en_formats
from django.utils.translation import gettext_lazy as _
import dj_database_url
import psycopg2


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '.herokuapp.com']





EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST = ''

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ""

EMAIL_HOST_USER_EVENTS = ''
EMAIL_HOST_PASSWORD_EVENTS = ""
EMAIL_HOST_USER_AUTO = ''
EMAIL_HOST_PASSWORD_AUTO = ""

EMAIL_HOST_IMAP = ''
EMAIL_HOST_IMAP_USER = ''
EMAIL_HOST_IMAP_PASSWORD = ""

EMAIL_HOST_IMAP_EVENTS = ''
EMAIL_HOST_IMAP_USER_EVENTS = ''
EMAIL_HOST_IMAP_PASSWORD_EVENTS = ""



# Application definition

INSTALLED_APPS = [
    'selectable',
    'crispy_forms',
    'widget_tweaks',
    'phone_field',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'material',
    'tinymce',
    'xhtml2pdf',
    'jsignature',
    'website',
    'events',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'vs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'events.context_processors.global_settings',
            ],
            'libraries':{
                'tozero': 'events.templatetags.tozero'
                }
        },
    },
]

WSGI_APPLICATION = 'vs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


LOGIN_REDIRECT_URL = '/events/'
LOGOUT_REDIRECT_URL = '/events/'

DATE_INPUT_FORMATS = ['%Y-%m-%d',      # '2006-10-25'
                      '%m/%d/%Y',       # '10/25/2006'
                      '%m/%d/%y',
                      '%m-%d-%y',
                      '%m-%d-%Y',
                      '%A, %B %d, %Y',
                      '%a, %b %d, %Y']  

TIME_INPUT_FORMATS = ['%I:%M %p',
                      '%I:%M%p',
                      '%I%p'] 

DATE_FORMAT = 'm-d-Y'
SHORT_DATE_FORMAT = 'm-d-Y'

en_formats.DATE_FORMAT = "%d/%m/%Y"    
en_formats.SHORT_DATE_FORMAT = "%d/%m/%Y"

FLAG_EMPTY = "#f8f8f8"
FLAG_STARTED = "#fff176"
FLAG_DONE = "#a5d6a7"
FLAG_LATE = "#ffcdd2"
FLAG_HOLD = "#ffcc80"
FLAG_WHITE = "#bbbbbb"

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'

TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': 'auto',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            autoresize paste spellchecker textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor
            ''',
    'toolbar1': '''
            bold italic underline | fontsizeselect  | forecolor backcolor |
            ''',
    'contextmenu': 'undo redo copy paste pastetext | formats | bold italic underline | fontsizeselect forecolor | link image',
    'menubar': False,
    'paste_as_text': True,
    'statusbar': False,
    #'inline': True,
    #'nothing': True,
    'spellchecker_languages': 'en',
    'preformatted': True,
    'autoresize_bottom_margin': 20,
    'autoresize_max_height': 1200,
    'autoresize_min_height': 150,
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': False,
    'entity_encoding': 'raw',
    'convert_urls:': False,
    'relative_urls': False,
    'remove_script_host': False,
    'content_style': 'body { font-size: 14px; } .mce-item-table, .mce-item-table td {border: none;}',
    }

TINYMCE_SPELLCHECKER = False

JSIGNATURE_WIDTH = 500
JSIGNATURE_HEIGHT = 250

API_SCOPE = ['https://www.googleapis.com/auth/calendar']
JSON_FILE = ''
JSON_PATH = os.path.join(BASE_DIR, JSON_FILE)
if DEBUG:
    REDIRECT_URI = "http://localhost:8000/events/gcallback"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
else:
    REDIRECT_URI = "https://events.vanderbiltstrings.com/events/gcallback"

WEBSITE = "https://events.vanderbiltstrings.com/events/"
WEBSITE_EXTRAS = "https://requests.vanderbiltstrings.com/extras/"
EMAIL_MAIN = ""
EMAIL_EVENTS = ""
EMAIL_RECORDS = ""
EMAIL_AUTO = "
FTP_ADDR = ''
FTP_URL '
PAYPAL_CLIENT_ID = ""
GOOGLE_CALENDAR_SRC = ""





HOLD_UNTIL = "Hold event until..."
HOLD_INDEFINITELY = "Hold event (indefinitely)"
SEND_HOLD = "Send Hold notice"

SEND_CONTRACT = "Send Contract request"
RECEIVE_CONTRACT = "Receive signed Contract"
RECEIPT_CONTRACT = "Send receipt for signed Contract"

SEND_DEPOSIT = "Send Deposit request"
RECEIVE_DEPOSIT = "Receive paid Deposit"
RECEIPT_DEPOSIT = "Send receipt for paid Deposit"

SEND_FINAL_PAYMENT = "Send Final Payment request"
RECEIVE_FINAL_PAYMENT = "Receive paid Final Payment"
RECEIPT_FINAL_PAYMENT = "Send receipt for paid Final Payment"

CHECK_MUSIC_LIST = "Check custom song(s) on Music List"

SEND_EXTRA_PAYMENT = "Send Extra Payment request"
RECEIVE_EXTRA_PAYMENT = "Receive Extra Payment"
RECEIPT_EXTRA_PAYMENT = "Send receipt for Extra Payment"

INVITE_MUSICIANS = "Invite Musicians to play"
ALL_MUSICIANS_BOOKED = "Get all Musicians booked"

SEND_FINAL_CONFIRMATION = "Send Final Confirmation of event"
RECEIVE_FINAL_CONFIRMATION = "Receive OK to Final Confirmation"

SEND_MUSIC_LIST = "Send Music List request"
RECEIVE_MUSIC_LIST = "Receive the Music List"

SEND_FACT_SHEETS = "Send Fact Sheets"
ALL_FACT_SHEETS_CONFIRMED = "Get all to confirm Fact Sheets"


DAYS_SPLIT_1 = 45
DAYS_SPLIT_2 = 28
DAYS_SPLIT_3 = 14
DAYS_SPLIT_4 = 6
#  so:   [ 46+, 29-45, 15-28, 7-14, 0-6 ]

DAYS_CONTRACT_SEND = [0,0,0,0,0] #created + x
DAYS_CONTRACT_DUE = [14,7,3,2,1] #sent + x
DAYS_CONTRACT_RCPT = [5,4,1,1,1] #rcvd + x

DAYS_DEPOSIT_SEND = [0,0,0,0,0] #created + x
DAYS_DEPOSIT_DUE = [14,9,3,2,1] # sent + x
DAYS_DEPOSIT_RCPT= [5,4,1,1,1] #rcvd + x

DAYS_FINAL_SEND = [37,33,0,0,0] #event - x
#if created is 0-28 days away, use created + x

DAYS_FINAL_DUE = [28,26,5,3,1] #event - x
#if created is 0-28 days away, use sent + x

DAYS_FINAL_RCPT = [7,4,1,1,1] #rcvd + x

DAYS_EXTRA_SEND = [27,20,2,0,0] #event - x
#if created is 0-28 days away, use created + x

DAYS_EXTRA_DUE = [8,6,4,2,1] #sent + x
DAYS_EXTRA_RCPT = [7,4,1,1,1] #rcvd + x

DAYS_MUSICIANS_SEND = [22,21,11,6,3] #event - x
DAYS_MUSICIANS_DUE = [8,6,4,2,1] #sent + x
DAYS_CONFIRMATION_SEND = [23,21,7,3,2] #event - x
DAYS_CONFIRMATION_DUE = [17,14,5,1,1] #event - x
#if created is 0-14 days away, use sent + x

DAYS_FACT_SHEETS_SEND = [6,5,4,3,2] #event - x
DAYS_FACT_SHEETS_DUE = [2,2,2,1,0] #event - x
DAYS_MUSIC_LIST_SEND = [60,26,11,7,3] #event - x
DAYS_MUSIC_LIST_DUE = [28,21,7,4,2] #event - x



DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'





#TEMPLATE_CONTEXT_PROCESSORS = {
#    'events.context_processors.global_settings',
#}





# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())


DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

