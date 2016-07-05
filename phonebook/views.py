import configparser
import re
import paramiko
import logging
import xml.etree.ElementTree as ET
import ldap
import bonsai
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
    return output.decode('utf-8')


def read_file(remote_file):
    with ssh_client() as client:
        with client.open_sftp() as sftp:
            with sftp.file(remote_file, mode='r') as f:
                return f.read().decode('utf-8')


def write_in_file(remote_file, text):
    with ssh_client() as client:
        with client.open_sftp() as sftp:
            with sftp.file(remote_file, mode='w+') as f:
                f.write(text)


sip_reload = 'sudo asterisk -rx "sip reload"'
reload_phoneprov = 'sudo asterisk -rx "module reload res_phoneprov"'
notify = lambda user: 'sudo asterisk -rx "sip notify yealink-check {0}"'.format(user.number)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='')
    search.widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'search', 'placeholder':'Введите запрос'})


# def ldap_search():
#     client = bonsai.LDAPClient("ldap://dc0.ksk.loc")
#     # client.set_credentials("SIMPLE", ("cn=adminkrek3,cn=Users,dc=ksk,dc=loc", "G2x?bhlo"))
#     conn = client.connect()
#     # result = conn.search("OU=Address Book,DC=ksk,DC=loc", 1, "(objectClass=group)", ["cn", "member"])
#     result = conn.search("OU=Address Book,DC=ksk,DC=loc", 1, "(cn=*)")
#     for r in result[1]['member']:
#         print(r)
#         en = bonsai.LDAPEntry(r)
#         print(en.dn)

def ldap_search():
    ad = ldap.initialize("ldap://dc0.ksk.loc")
    ad.simple_bind_s("cn=adminkrek3,cn=Users,dc=ksk,dc=loc", "G2x?bhlo")
    result = ad.search_s("OU=Address Book,DC=ksk,DC=loc", 1, "(cn=*)", ["cn", "member"])
    print(result)
    # client.set_credentials("SIMPLE", ("cn=adminkrek3,cn=Users,dc=ksk,dc=loc", "G2x?bhlo"))
    # conn = client.connect()
    # result = conn.search("OU=Address Book,DC=ksk,DC=loc", 1, "(objectClass=group)", ["cn", "member"])
    # result = conn.search("OU=Address Book,DC=ksk,DC=loc", 1, "(cn=*)")
    # for r in result[1]['member']:
    #     print(r)
    #     en = bonsai.LDAPEntry(r)
    #     print(en.dn)

def config_parse():
    f = read_file('/etc/asterisk/users.conf')
    config = configparser.ConfigParser()
    config.read_string(f)
    [user.delete() for user in User.objects.all() if user.number not in config.sections()]
    for user in config.sections():
        if config.has_option(user, 'fullname') and config.has_option(user, 'cid_number') and config.has_option(user, 'macaddress'):
            cid_number = config.get(user, 'cid_number')
            if re.match(r'25..', cid_number):
                company = User.COMPANY[1][0]
            elif re.match(r'27..', cid_number):
                company = User.COMPANY[2][0]
            else:
                company = User.COMPANY[0][0]
            User.objects.update_or_create(
                number=cid_number,
                defaults={
                    'last_name': config.get(user,'fullname'),
                    'mac_adress': config.get(user, 'macaddress'),
                    'company': company,
                    'department': 'general'
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
    configs = client_exec(command).split()
    logger.debug(configs)
    reg = re.compile(r'(?P<mac>\w{12}).cfg')
    configs = [m.group('mac') for m in map(reg.match, configs) if m]
    logger.debug(configs)
    User.objects.filter(mac_adress__in=configs).update(panel=True)
    User.objects.exclude(mac_adress__in=configs).update(panel=False)


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


def company_phonebook_create():
    # company_list = User.COMPANY
    place = User.DEPARTMENTS
    print(place)
    for company in place:
        menu = ET.Element('YealinkIPPhoneMenu')
        title = ET.SubElement(menu, 'Title')
        title.text = company[1]
        for department in company:
            item = ET.SubElement(menu, 'MenuItem')
            name = ET.SubElement(item, 'Name')
            name.text = department[1]
            url = ET.SubElement(item, 'URL')
            url.text = department_phonebook_create(department=department[0], company=company[0])
        tree = ET.ElementTree(element=menu)
        filename = '{0}.xml'.format(company[0])
        file = '/usr/share/asterisk/phoneprov/phonebook/{0}'.format(filename)
        with ssh_client() as client:
            with client.open_sftp() as sftp:
                with sftp.file(file, mode='w+') as f:
                    tree.write(f, encoding='utf-8', method='xml')


def department_phonebook_create(department, company):
    persons = User.objects.filter(department=department, company=company)
    menu = ET.Element('YealinkIPPhoneDirectory')
    for person in persons:
        entry = ET.SubElement(menu, 'DirectoryEntry')
        name = ET.SubElement(entry, 'Name')
        name.text = person.last_name
        telephone = ET.SubElement(entry, 'Telephone')
        telephone.text = person.number
    tree = ET.ElementTree(element=menu)
    filename = '{0}_{1}.xml'.format(company, department)
    file = '/usr/share/asterisk/phoneprov/phonebook/{0}'.format(filename)
    with ssh_client() as client:
        with client.open_sftp() as sftp:
            with sftp.file(file, mode='w') as f:
                tree.write(f, encoding='utf-8', method='xml')
    return 'http://172.16.81.2:8088/phoneprov/phonebook/{0}'.format(filename)


def company_phonebook_response(request, company_name):
    company = User.objects.filter(company=company_name).values('department').distinct()
    data = {
        'company_name': company_name,
        'company': company,
    }
    return render(request, 'phonebook/phonebook_menu.xml', data, content_type="text/xml")


def department_phonebook_response(request, company_name, department_name):
    data = {
        'users': User.objects.filter(department=department_name, company=company_name)
    }
    return render(request, 'phonebook/phonebook_department.xml', data, content_type="text/xml")


def phone_config(request, mac):
    data = {
        'user': User.objects.get(mac_adress=mac),
    }
    return render(request, 'phonebook/phone/default.cfg', data, content_type="text/plain")


def phone_default_config(request, name):
    data = {
        # ''
    }
    return render(request, 'phonebook/phone/y{0}.cfg'.format(name), data, content_type="text/plain")


def refresh(request):
    # User.objects.all().update(name=None)
    # config_parse()
    # ldap_search()
    # user_panel_parse()
    # ext_panel_parse()
    # mobilephone_parse()
    company_phonebook_create()
    return redirect('phonebook:phonebook')