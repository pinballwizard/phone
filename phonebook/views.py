import configparser
import re
import paramiko
import logging
from django import forms
from django.db import connections
from django.shortcuts import render, redirect

from phonebook.models import User


logger = logging.getLogger('phonebook')


def ssh_client():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.16.1.45', 22, 'itadmin', 'G2x?bhlo')
    return client


def client_exec(command):
    with ssh_client() as client:
        (stdin, stdout, stderr) = client.exec_command(command)
        output = stdout.read()
    return output


def read_file(remote_file):
    with ssh_client() as client:
        with client.open_sftp() as sftp:
            with sftp.file(remote_file, mode='r') as f:
                return f.read().decode('utf-8')


def write_in_file(remote_file, text):
    with ssh_client() as client:
        with client.open_sftp() as sftp:
            with sftp.file(remote_file, mode='r') as f:
                f.write(text)


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
    [user.delete() for user in User.objects.all() if user.number not in config.sections()]
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
            logger.info("Nothing to save for {0}".format(user))


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
        logger.info('Start parse file {0} for user {1}'.format(remotef, user.mac_adress))
        file = read_file(remotef)
        re_value = re.compile(r'expansion_module.(?P<module>\d+).key.(?P<key>\d+).value ?= ?(?P<result>\w+)')
        for match in re_value.finditer(file):
            re_dict = match.groupdict()
            module = re_dict['module']
            key = re_dict['key']
            number = re_dict['result']
            match2 = re.search(r'{0}.key.{1}.label ?= ?(?P<label>.+)'.format(module, key), file)
            if match2:
                re_dict_2 = match2.groupdict()
                name = re_dict_2['label']
                logger.debug('For {0} parsed {1} and {2}'.format(remotef, re_dict, re_dict_2))
                user.extendednumber_set.update_or_create(
                    key=key,
                    defaults={
                        'module': module,
                        'number': number,
                        'name': name
                    }
                )


def mobilephone_parse():
    filename = '/etc/asterisk/mobilephone.ael'
    file = read_file(filename)
    for n in re.finditer(r'_*(?P<number>\d{4}).*(?P<mobile>\d{11})', file):
        re_n = n.groupdict()
        mobile = re_n['mobile']
        number = re_n['number']
        logger.debug('For file {0} parsed user {1} with mobile => {2}'.format(filename, number, mobile))
        user = User.objects.filter(number=number)
        if user:
            user[0].mobile = mobile
            user[0].save()


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


def refresh(request):
    config_parse()
    user_panel_parse()
    ext_panel_parse()
    mobilephone_parse()
    return redirect('phonebook:phonebook')