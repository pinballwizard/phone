from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import configparser
from phonebook.models import User


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)
    search.widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'search'})


def config_reload(request):
    # file = "/etc/asterisk/users.conf"
    file = "/home/pinballwizard/users.conf"
    config = configparser.ConfigParser()
    config.read(file)
    for user in config.sections():
        try:
            if User.objects.filter(number=user).exists():
                us = User.objects.get(number=user)
                us.number=config.get(user,'cid_number')
                us.last_name=config.get(user,'fullname')
                us.mac_adress=config.get(user,'macaddress')
                us.save()
            else:
                u = User()
                u.last_name=config.get(user,'fullname')
                u.number=config.get(user,'cid_number')
                u.mac_adress=config.get(user,'macaddress')
                u.save()
        except:
            print("User %s haven't filed fullname or cid_number" % user)
    return redirect(phonebook_page)


def phonebook_page(request):
    data = {
        'search_form': SearchForm(),
        'users': User.objects.order_by('number')
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