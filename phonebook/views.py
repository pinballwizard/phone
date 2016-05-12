from django.shortcuts import render, redirect
from django import forms
from django.db.models import Q
from django.http import HttpResponse
import configparser
from django.db import connections
from phonebook.models import User, ExtendedNumber
from operator import itemgetter, attrgetter
import paramiko


def client_exec(command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.16.1.45', 22, 'itadmin', 'G2x?bhlo')
    (stdin, stdout, stderr) = client.exec_command(command)
    output = stdout.read()
    client.close()
    return output

def get_transport():
    transport = paramiko.Transport(("172.16.1.45",22))
    transport.connect(username='itadmin', password='G2x?bhlo')
    return transport


def read_file(remote_file):
    transport = get_transport()
    sftp = paramiko.SFTPClient.from_transport(transport)
    with sftp.file(remote_file, mode='r') as f:
        infile = f.read()
    sftp.close()
    transport.close()
    return infile.decode('utf-8')


def write_in_file(remote_file, text):
    transport = get_transport()
    sftp = paramiko.SFTPClient.from_transport(transport)
    with sftp.file(remote_file, mode='r') as f:
        f.write(text)
    sftp.close()
    transport.close()


sip_reload = 'sudo asterisk -rx "sip reload"'
reload_phoneprov = 'sudo asterisk -rx "module reload res_phoneprov"'
notify = lambda user: 'sudo asterisk -rx "sip notify yealink-check {0}"'.format(user.number)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='')
    search.widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'search', 'placeholder':'Введите запрос'})


def config_parse():
    f = read_file('/etc/asterisk/users.conf')
    config = configparser.ConfigParser()
    config.read_string(f)
    for user in config.sections():
        if config.has_option(user, 'fullname') and config.has_option(user, 'cid_number') and config.has_option(user, 'macaddress'):
            User.objects.update_or_create(
                number=config.get(user, 'cid_number'),
                defaults={
                    'last_name': config.get(user,'fullname'),
                    'mac_adress': config.get(user, 'macaddress')
                }
            )
        else:
            print("nothing to save for {0}".format(user))


# def user_add(request, user):
#     config = configparser.ConfigParser()
#     if not config.has_section(user.number):
#         config.add_section(user.number)
#     config.set(user.fullname, user.last_name)
#     config.set(user.cid_number, user.cid_number)
#     config.set(user.macadress, user.macadress)
#     # config.write()


def user_panel_parse():
    command = 'ls /usr/share/asterisk/phoneprov/'
    configs = client_exec(command).decode('utf-8').split()
    configs.remove('000000000000.cfg')
    [configs.remove(config) for config in configs if config.startswith('y')]
    [configs.remove(config) for config in configs if config.startswith('y')]
    [configs.remove(config) for config in configs if config.startswith('y')]
    m = [x.replace('.cfg','') for x in configs]
    User.objects.filter(mac_adress__in=m).update(panel=True)
    User.objects.exclude(mac_adress__in=m).update(panel=False)


def ext_panel_parse():
    for user in User.objects.filter(panel=True, mac_adress__isnull=False):
        remotef = '/usr/share/asterisk/phoneprov/{0}.cfg'.format(user.mac_adress)
        print(user.mac_adress)
        file = read_file(remotef)
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
                name = EN[module][key]['name']
                number = EN[module][key]['number']
                try:
                    user.extendednumber_set.update_or_create(
                        key=key,
                        defaults={
                            'module': module,
                            'name': name,
                            'number': number
                        }
                    )
                except:
                    print("Extended number {0} {1} already exist".format(name, number))


def refresh(request):
    config_parse()
    user_panel_parse()
    ext_panel_parse()
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


def call_stats(request):
    cursor = connections['asterisk'].cursor()
    users = User.objects.all()
    for user in users:
        cursor.execute("SELECT duration FROM cdr WHERE src={0}".format(user.number))
        s = 0
        for n in cursor.fetchall():
            s += n[0]
        user.call_duration = int(s/60)
    data = {
        'users': users
    }
    return render(request, 'phonebook/callstats.html', data)