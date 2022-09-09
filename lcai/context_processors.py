from django.conf import settings

def site_data(request):
    return {
        'PLAUSIBLE_SITE_DOMAIN': settings.PLAUSIBLE_SITE_DOMAIN,
    }