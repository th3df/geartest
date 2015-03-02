import psutil
import getpass
from django.shortcuts import render, redirect
from django.http import HttpResponse
from memoryconsumer.models import Memloadstat, Experiment
from memoryconsumer.eatmemory import random_element

# Create your views here.
def memcon_home(request):
    return render(request, "memoryconsumer.html")
        
def exp_page(request, exp_id):
    exp_ = Experiment.objects.get(id=exp_id)
    return render(request, "exp_page.html", {'exp': exp_})
    
def new_page(request):
    exp_ = Experiment.objects.create()
    current_memload = int(request.POST["mem_load_text"])
    
    avail_mem_before = int(psutil.virtual_memory().available / 2**20)
    huge_array =[]
    for j in range(current_memload): huge_array.append(random_element())
    avail_mem_after = int(psutil.virtual_memory().available / 2**20)   
    current_availdelta = avail_mem_before - avail_mem_after
    
    current_gear = getpass.getuser()
    
    Memloadstat.objects.create(
        gearID = current_gear,
        memload = current_memload, 
        availmem = avail_mem_after,
        availdelta = current_availdelta, 
        exp = exp_ )
    return redirect('/memoryconsumer/exp_page/%d/' % (exp_.id,))
    
def add_memloadstat(request, exp_id):
    exp_ = Experiment.objects.get(id=exp_id)
    current_memload = int(request.POST["mem_load_text"])
    
    avail_mem_before = int(psutil.virtual_memory().available / 2**20)
    huge_array =[]
    for j in range(current_memload): huge_array.append(random_element())
    avail_mem_after = int(psutil.virtual_memory().available / 2**20)   
    current_availdelta = avail_mem_before - avail_mem_after
    
    current_gear = getpass.getuser()
    
    Memloadstat.objects.create( 
        gearID = current_gear,
        memload = current_memload, 
        availmem = avail_mem_after, 
        availdelta = current_availdelta, 
        exp = exp_ )
        
    return redirect('/memoryconsumer/exp_page/%d/' % (exp_.id,))