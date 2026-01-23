from .utils import get_profile

def profile(request):
    return {'has_profile': get_profile()}