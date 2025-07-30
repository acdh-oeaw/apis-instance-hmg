from apis_acdhch_default_settings.settings import *  # noqa: F401, F403
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEBUG = True
APIS_BASE_URI = "https://hgm.acdh-dev.oeaw.ac.at/"
ROOT_URLCONF = "apis_ontology.urls"

MIDDLEWARE += [
    "simple_history.middleware.HistoryRequestMiddleware",
]
CSRF_TRUSTED_ORIGINS = [
    "https://hgm.acdh.oeaw.ac.at",
    "https://hgm.acdh-dev.oeaw.ac.at",
]
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
APIS_ANON_VIEWS_ALLOWED = False
EXPORT_FORMATS = ("xslx", "json")

EXTRA_APPS = [
    "django.contrib.postgres",
    "django_interval",
    "apis_core.documentation",
]

for app in EXTRA_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)


DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5-responsive.html"
DJANGO_TABLES2_TABLE_ATTRS = {
    "class": "table table-striped table-hover",
}

LANGUAGE_CODE = "de"  # or your default
LANGUAGES = [
    ("en", "English"),
    ("de", "German"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]
