from .base import *
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
ALLOWED_HOSTS += ['0.0.0.0']
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
