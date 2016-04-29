from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import configparser
from phonebook.models import User, ExtendedNumber
import paramiko


def get_file(remote_file):
    host = "172.16.1.45"
    port = 22
    transport = paramiko.Transport((host,port))
    transport.connect(username='itadmin', password='G2x?bhlo')
    sftp = paramiko.SFTPClient.from_transport(transport)
    with sftp.file(remote_file, mode='r') as f:
        infile = f.read()
    sftp.close()
    transport.close()
    return infile.decode('utf-8')


def put_file(local_file, remote_file):
    host = "172.16.1.45"
    port = 22
    transport = paramiko.Transport((host,port))
    transport.connect(username='itadmin', password='G2x?bhlo')
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_file, remote_file)
    sftp.close()
    transport.close()


def notify(user):
    com = 'sudo asterisk -rx "sip notify yealink-check {0}"'.format(user.number)
    print(com)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='')
    search.widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'search', 'placeholder':'Введите запрос'})


def config_parse(request):
    f = get_file('/etc/asterisk/users.conf')
    config = configparser.ConfigParser()
    config.read_string(f)
    for user in config.sections():
        if config.has_option(user, 'fullname') and config.has_option(user, 'cid_number') and config.has_option(user, 'macaddress'):
            User.objects.get_or_create(last_name=config.get(user,'fullname'),
                                       number=config.get(user,'cid_number'),
                                       mac_adress=config.get(user, 'macaddress'))
        else:
            print("nothing to save for {0}".format(user))
    return redirect(phonebook_page)


# def user_add(request, user):
#     config = configparser.ConfigParser()
#     if not config.has_section(user.number):
#         config.add_section(user.number)
#     config.set(user.fullname, user.last_name)
#     config.set(user.cid_number, user.cid_number)
#     config.set(user.macadress, user.macadress)
#     # config.write()

# def ext_panel_user_exist(request):



def ext_panel_parse(request):
    for user in User.objects.filter(panel=True, mac_adress__isnull=False):
        remotef = '/usr/share/asterisk/phoneprov/{0}.cfg'.format(user.mac_adress)
        file = get_file(remotef)
        EN = {}
        for line in file.splitlines():
            if line.startswith('expansion_module'):
                sl = line.split('=')
                sl[0] = sl[0].strip()
                sl[1] = sl[1].strip()
                key = sl[0].split('.')[3]
                module = sl[0].split('.')[1]
                if module not in EN:
                    EN[module] = {}
                if key not in EN[module]:
                    EN[module][key] = {}
                if sl[0].endswith('value') and sl[1] is not None:
                    EN[module][key]['number'] = sl[1]
                if sl[0].endswith('label') and sl[1] is not None:
                    EN[module][key]['name'] = sl[1]
        for module in EN:
            for key in EN[module]:
                E = ExtendedNumber()
                E.module = module
                E.key = key
                E.name = EN[module][key]['name']
                E.number = EN[module][key]['number']
                try:
                    user.extendednumber_set.get_or_create(E)
                except:
                    print("Extended number {0} {1} already exist".format(E.name, E.number))
    return redirect(phonebook_page)


def phonebook_page(request):
    data = {
        'search_form': SearchForm(),
        'users': User.objects.order_by('number'),
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