from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import configparser
from phonebook.models import User


def config_reload(request):
    file = "/home/pinballwizard/users.conf"
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
        'data': User.objects.all()
    }
    return render(request, 'phonebook/phonebook.html', data)