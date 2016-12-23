import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vpwt%jzdw_-l7^^!v5bai(suf8&9)7fxx(e%c^dw18j!%9^h()'


PUSH_NOTIFICATIONS_SETTINGS = {
        "GCM_API_KEY": "[your api key]",
        "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
        "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
        "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
