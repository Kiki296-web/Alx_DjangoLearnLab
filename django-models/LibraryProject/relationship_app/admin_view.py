from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .utils import is_admin
from django.shortcuts import render

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html')