from django.shortcuts import render
from django.http import HttpResponse
from socket import gethostname
from getpass import getuser

# Create your views here.
def home(request):
    hostnm = gethostname()
    gearnm = getuser()
    return render(request, "homepage.html", {'hostnm':hostnm, "gearnm":gearnm})