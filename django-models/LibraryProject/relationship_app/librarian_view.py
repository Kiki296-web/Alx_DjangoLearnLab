from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .utils import is_librarian

@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Welcome to the Librarian Dashboard!")