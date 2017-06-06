from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.views.generic import View
from .forms import UserForm, CategoryForm, EntryForm
from .models import Entry
from .models import MainCategory
from django.contrib.auth import logout
import datetime

def home(request):

    if not request.user.is_authenticated():
        return render(request, 'proj/login.html')
    allEntries = Entry.objects.filter(user=request.user)
    allCategories = MainCategory.objects.filter(user=request.user)
    balance = 0
    for i in allEntries:
        if i.type == "p":
            balance += i.value
        else:
            balance -= i.value
    for i in allCategories:
       catEntries = Entry.objects.filter(user=request.user, category=i)
       for j in catEntries:
           if j.type == "p":
               i.bal += j.value
           else:
               i.bal -= j.value
    context = {
        'allCategories': allCategories,
        'allEntries': allEntries,
        'balance': balance,
    }
    return render(request, 'proj/home.html', context)



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                allEntries = Entry.objects.filter(user=request.user)
                allCategories = MainCategory.objects.filter(user=request.user)
                balance = 0
                for i in allEntries:
                    if i.type == "p":
                        balance += i.value
                    else:
                        balance -= i.value
                for i in allCategories:
                   catEntries = Entry.objects.filter(user=request.user, category=i)
                   for j in catEntries:
                       if j.type == "p":
                           i.bal += j.value
                       else:
                         i.bal -= j.value
                context = {
                    'allCategories': allCategories,
                    'allEntries': allEntries,
                    'balance': balance,
                }
                return render(request, 'proj/home.html', context)
    context = {
        "form": form,
    }
    return render(request, 'proj/register.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                allEntries = Entry.objects.filter(user=request.user)
                allCategories = MainCategory.objects.filter(user=request.user)
                balance = 0
                for i in allEntries:
                    if i.type == "p":
                        balance += i.value
                    else:
                        balance -= i.value
                for i in allCategories:
                   catEntries = Entry.objects.filter(user=request.user, category=i)
                   for j in catEntries:
                       if j.type == "p":
                           i.bal += j.value
                       else:
                         i.bal -= j.value
                context = {
                    'allCategories': allCategories,
                    'allEntries': allEntries,
                    'balance': balance,
                }
                return render(request, 'proj/home.html', context)
            else:
                return render(request, 'proj/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'proj/login.html', {'error_message': 'Invalid login'})
    return render(request, 'proj/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'proj/login.html', context)

def create_category(request):
    if not request.user.is_authenticated():
        return render(request, 'proj/login.html')
    else:
        form = CategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            allEntries = Entry.objects.filter(user=request.user)
            allCategories = MainCategory.objects.filter(user=request.user)
            balance = 0
            for i in allEntries:
                if i.type == "p":
                    balance += i.value
                else:
                    balance -= i.value
            for i in allCategories:
                   catEntries = Entry.objects.filter(user=request.user, category=i)
                   for j in catEntries:
                       if j.type == "p":
                           i.bal += j.value
                       else:
                         i.bal -= j.value
            context = {
                'allCategories': allCategories,
                'allEntries': allEntries,
                 'balance': balance,
            }
            return render(request, 'proj/home.html', context)
        context = {
            "form": form,
        }
        return render(request, 'proj/create_category.html', context)

def create_entry(request, category_id):
    form = EntryForm(request.POST or None, request.FILES or None)
    category = get_object_or_404(MainCategory, pk=category_id)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.date = datetime.datetime.today()
        entry.category = category
        entry.user = request.user
        entry.save()
        allEntries = Entry.objects.filter(user=request.user)
        allCategories = MainCategory.objects.filter(user=request.user)
        balance = 0
        for i in allEntries:
                if i.type == "p":
                    balance += i.value
                else:
                    balance -= i.value
        for i in allCategories:
                   catEntries = Entry.objects.filter(user=request.user, category=i)
                   for j in catEntries:
                       if j.type == "p":
                           i.bal += j.value
                       else:
                         i.bal -= j.value
        context = {
               'allCategories': allCategories,
               'allEntries': allEntries,
               'balance': balance,
          }
        return render(request, 'proj/home.html', context)
    context = {
         "category": category,
         "form": form,
    }
    return render(request, 'proj/create_entry.html', context)

def entries (request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'proj/login.html')
    else:
        try:
            entries_ids = []
            for category in MainCategory.objects.filter(user=request.user):
                for entry in category.entry_set.all():
                    category_id = category.id
                    entries_ids.append(entry.pk)
            users_entries = Entry.objects.filter(pk__in=entries_ids)
            if filter_by == 'p':
                users_entries = users_entries.filter(type='p')
            else:
                if filter_by == 'w':
                    users_entries = users_entries.filter(type='w')
        except MainCategory.DoesNotExist:
            users_entries= []
        return render(request, 'proj/entries.html', {
            'category_id': category_id,
            'entries_list': users_entries,
            'filter_by': filter_by,
        })

def delete_category(request, category_id):
    category = MainCategory.objects.get(pk=category_id)
    category.delete()
    categories = MainCategory.objects.filter(user=request.user)
    return render(request, 'proj/home', {'category': categories})
