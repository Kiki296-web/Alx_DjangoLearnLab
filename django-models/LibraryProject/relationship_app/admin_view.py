from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .utils import is_admin

@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Welcome to the Admin Dashboard!")