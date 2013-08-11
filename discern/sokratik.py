"""
sokratik config for discern,, uses postgres and low cost aws settings. no theming is involved here
interfaces with config repo integrated into bitbucket
"""

__author__ = 'vulcan'

from settings import *
import json
from os.path import expanduser

HOME_FOLDER = path(expanduser("~"))
CONFIG_ROOT = HOME_FOLDER / "sokratik-infra/json-configs"
# specified as an environment variable.  Typically this is set
# in the service's upstart script and corresponds exactly to the service name.
# Service variants apply config differences via env and auth JSON files,
# the names of which correspond to the variant.
SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', "discern")

# when not variant is specified we attempt to load an unvaried
# config set.
CONFIG_PREFIX = ""

if SERVICE_VARIANT:
    CONFIG_PREFIX = SERVICE_VARIANT + "."

with open(CONFIG_ROOT / CONFIG_PREFIX + "env.json") as env_file:
    ENV_TOKENS = json.load(env_file)

CACHES = ENV_TOKENS.get('CACHES', CACHES)
TIME_ZONE = ENV_TOKENS.get('TIME_ZONE', TIME_ZONE)
ELB_HOSTNAME = ENV_TOKENS.get('ELB_HOSTNAME', None)
BROKER_URL = ENV_TOKENS.get('BROKER_URL', BROKER_URL)
CELERY_RESULT_BACKEND = ENV_TOKENS.get('CELERY_RESULT_BACKEND', CELERY_RESULT_BACKEND)
USE_S3_TO_STORE_MODELS = ENV_TOKENS.get('USE_S3_TO_STORE_MODELS', USE_S3_TO_STORE_MODELS)
S3_BUCKETNAME = ENV_TOKENS.get('S3_BUCKETNAME', S3_BUCKETNAME)
ADMINS = (
    ("discern-admin", "sokratk-admin@sokratik.com"),
)

MANAGERS = ADMINS

ELB_HOSTNAME = ENV_TOKENS.get('ELB_HOSTNAME', None)

DNS_HOSTNAME = ENV_TOKENS.get('DNS_HOSTNAME', None)

STATIC_ROOT = ENV_TOKENS.get('STATIC_ROOT')

EMAIL_BACKEND = ENV_TOKENS.get('EMAIL_BACKEND', EMAIL_BACKEND)

DEFAULT_FROM_EMAIL = ENV_TOKENS.get('DEFAULT_FROM_EMAIL')


ACCOUNT_EMAIL_VERIFICATION = ENV_TOKENS.get('ACCOUNT_EMAIL_VERIFICATION', ACCOUNT_EMAIL_VERIFICATION)
if ELB_HOSTNAME is not None:
    ALLOWED_HOSTS += [ELB_HOSTNAME]

if DNS_HOSTNAME is not None:
    ALLOWED_HOSTS += [DNS_HOSTNAME]


with open(CONFIG_ROOT / CONFIG_PREFIX + "auth.json") as auth_file:
    AUTH_TOKENS = json.load(auth_file)

DATABASES = AUTH_TOKENS.get('DATABASES', DATABASES)
ML_MODEL_PATH = os.path.join(HOME_FOLDER, ENV_TOKENS.get('ML_MODEL_PATH'))

AWS_ACCESS_KEY_ID = AUTH_TOKENS.get('AWS_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID)
AWS_SECRET_ACCESS_KEY = AUTH_TOKENS.get('AWS_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY)
SECRET_KEY = AUTH_TOKENS.get('SECRET_KEY')

AWS_SES_REGION_NAME = ENV_TOKENS.get('AWS_SES_REGION_NAME', 'us-east-1')
if AWS_SES_REGION_NAME is not None:
    AWS_SES_REGION_ENDPOINT = 'email.{0}.amazonaws.com'.format(AWS_SES_REGION_NAME)

#Set this for django-analytical.  Because django-analytical enables the service if the key exists,
#ensure that the settings value is only created if the key exists in the deployment settings.
ga_key = AUTH_TOKENS.get("GOOGLE_ANALYTICS_PROPERTY_ID", "")
if len(ga_key) > 1:
    GOOGLE_ANALYTICS_PROPERTY_ID = ga_key

