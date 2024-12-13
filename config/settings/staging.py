from .production import *  # noqa

INSTALLED_APPS += ["bandit"]
EMAIL_BACKEND = "bandit.backends.smtp.HijackSMTPBackend"
BANDIT_EMAIL = env.list("DJANGO_BANDIT_RCPTS", default=["support@sinnwerkstatt.com"])
BANDIT_WHITELIST = env.list("DJANGO_BANDIT_WHITELIST", default=["sinnwerkstatt.com"])
