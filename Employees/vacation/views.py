from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Vacation
from .forms import VacationForm, CustomUserForm, CustomLoginForm
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import json
import collections
import datetime
from dateutil import rrule

def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)        
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['email'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = CustomUserForm()
    
    return render(request, 'vacation/signup.html', {'form': form})

def login(request):    
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            auth_login(request, user)
            return redirect('vacation_view')        
    else:
        form = CustomLoginForm()

    return render(request, 'vacation/login.html', {'form': form})

def vacation_view(request):
    rows = Vacation.objects.filter(employee=request.user)
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()        
        d['id'] = row.pk
        d['employee'] = row.employee.username
        d['description'] = row.description
        d['created_date'] = row.created_date.strftime("%B %d, %Y")
        d['from_date'] = row.from_date.strftime("%B %d, %Y")
        d['to_date'] = row.to_date.strftime("%B %d, %Y")
        
        a = datetime.datetime(row.from_date.year,row.from_date.month,row.from_date.day)
        b = datetime.datetime(row.to_date.year,row.to_date.month,row.to_date.day)

        diff_business_days = len(list(rrule.rrule(rrule.DAILY,
                                          dtstart=a,
                                          until=b - datetime.timedelta(days=1),
                                          byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR))))
        d['duration'] = diff_business_days
        objects_list.append(d)
     
    j = json.dumps(objects_list)    
    return render(request, 'vacation/vacation_view.html', {'jsdata': j})

@csrf_exempt
def vacation_add(request):
    if request.method == "POST":        
        form = VacationForm(request.POST)        
        if form.is_valid():            
            vacation = form.save(commit=False)            
            vacation.employee = request.user            
            vacation.save()
            
        rows = Vacation.objects.filter(employee=request.user)
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()    
            d['id'] = row.pk
            d['employee'] = row.employee.username
            d['description'] = row.description
            d['from_date'] = row.from_date.strftime("%B %d, %Y")
            d['to_date'] = row.to_date.strftime("%B %d, %Y")
            objects_list.append(d)
            
        j = json.dumps(objects_list)       
        return render(request, 'vacation/vacation_view.html', {'jsdata': j})

    else:
        form = VacationForm()
        return render(request, 'vacation/vacation_add.html', {'form': form})
    
def vacation_edit(request, pk):
    vacation = get_object_or_404(Vacation, pk=pk)
    if request.method == "POST":
        form = VacationForm(request.POST, instance=vacation)
        if form.is_valid():
            vacation = form.save(commit=False)
            vacation.employee = request.user
            vacation.save()
            return redirect('vacation_view')
    else:
        form = VacationForm(instance=vacation)
    return render(request, 'vacation/vacation_update.html', {'form': form, 'id': pk})

def logout(request):
    auth_logout(request)    
    return redirect('login')
