from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .utils import is_member

@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Welcome to the Member Dashboard!")