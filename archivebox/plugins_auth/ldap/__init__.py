__package__ = 'plugins_auth.ldap'
__label__ = 'ldap'
__version__ = '2024.10.14'
__author__ = 'Nick Sweeting'
__homepage__ = 'https://github.com/django-auth-ldap/django-auth-ldap'
# __dependencies__ = ['pip']

import abx


@abx.hookimpl
def get_PLUGIN():
    return {
        'ldap': {
            'PACKAGE': __package__,
            'LABEL': __label__,
            'VERSION': __version__,
            'AUTHOR': __author__,
            'HOMEPAGE': __homepage__,
            # 'DEPENDENCIES': __dependencies__,
        }
    }

@abx.hookimpl
def get_CONFIG():
    from .config import LDAP_CONFIG
    
    return {
        'ldap': LDAP_CONFIG
    }

@abx.hookimpl
def get_BINARIES():
    from .binaries import LDAP_BINARY
    
    return {
        'ldap': LDAP_BINARY,
    }


def create_superuser_from_ldap_user(sender, user=None, ldap_user=None, **kwargs):
    from django.conf import settings
    
    if user is None:
        return                        # not authenticated at all
    
    if not user.id and settings.CONFIGS.ldap.LDAP_CREATE_SUPERUSER:
        user.is_superuser = True      # authenticated via LDAP, but user is not set up in DB yet

    user.is_staff = True
    print(f'[!] WARNING: Creating new user {user} based on LDAP user {ldap_user} (is_staff={user.is_staff}, is_superuser={user.is_superuser})')


@abx.hookimpl
def ready():
    from django.conf import settings
    
    if settings.CONFIGS.ldap.LDAP_ENABLED:
        import django_auth_ldap.backend
        django_auth_ldap.backend.populate_user.connect(create_superuser_from_ldap_user)
    