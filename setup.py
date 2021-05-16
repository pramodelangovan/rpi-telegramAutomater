import os
import sys
from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DJANGO_PATH = os.path.join(BASE_DIR, "telegram")

sys.path.append(DJANGO_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE",  "telegram.settings")
sys.path.append(os.path.join(DJANGO_PATH, "teleModel"))

application = get_wsgi_application()
