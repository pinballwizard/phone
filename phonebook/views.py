from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import configparser
from phonebook.models import User


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)
    search.widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'search'})


def config_reload(request):
    file = "/etc/asterisk/users.conf"
    config = configparser.ConfigParser()
    config.read(file)
    for user in config.sections():
        try:
            u = User(last_name=config.get(user,'fullname'), number=config.get(user,'cid_number'))
            try:
                u.save()
            except:
                print("User %s already exist" % user)
        except:
            print("User %s haven't filed fullname or cid_number" % user)
    return redirect(phonebook_page)


def phonebook_page(request):
    data = {
        'search_form': SearchForm(),
        'users': User.objects.all()
    }
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_str = form.cleaned_data['search']
            q1 = User.objects.filter(last_name__icontains=search_str)
            q2 = User.objects.filter(number__icontains=search_str)
            q3 = User.objects.filter(mobile__icontains=search_str)
            queryset = q1 | q2 | q3
            data['users'] = queryset
            data['search_form'] = form
    return render(request, 'phonebook/phonebook.html', data)