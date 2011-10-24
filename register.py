#!/usr/bin/env python
# coding=utf-8
import getpass, sys
from xmlrpclib import ServerProxy

def register(rpc):
    uid = getpass.getuser()
    username = raw_input(u"Dein Spline-Username [%s]: " % uid)
    username = uid if username == '' else username
    spline_password = getpass.getpass('Dein LDAP-Passwort: ')
    irc_username = uid if username == '' else username
    irc_password = 0
    irc_password2 = 1
    while irc_password != irc_password2:
        irc_password = getpass.getpass(u'Waehle ein Passwort um dich beim Bot zu identifizieren: ')
        irc_password2 = getpass.getpass('Wiederholung: ')
        if irc_password != irc_password2:
            print u"Passwoerter stimmen nicht ueberein."
    print "Willst du per Mail (%s@spline.inf.fu-berlin.de) informiert werden, wenn du einen Post schreibst? [y/N] " % username,
    get_mail_char = sys.stdin.read(1)
    if get_mail_char.lower() == 'y':
        get_mail = True
    else:
        get_mail = False
    success = rpc.add_user(username, spline_password, irc_password, get_mail)
    if success:
        print "Anmeldung erfolgreich."
    else:
        print "Anmeldung fehlgeschlagen. Spline-Credentials falsch?"

def change_pw(rpc):
    uid = getpass.getuser()
    username = raw_input(u"Username [%s]: " % uid)
    username = uid if username == '' else username
    password = getpass.getpass('Altes Passwort: ')
    while new_password != new_password2:
        new_password = getpass.getpass(u'Neues Passwort: ')
        new_password2 = getpass.getpass('Wiederholung: ')
        if new_password != new_password2:
            print u"Eingaben stimmen nicht ueberein."
    rpc.set_new_password(username,password,new_password)
    print "Passwort geändert!"

def toggle_mail(rpc):
    uid = getpass.getuser()
    username = raw_input(u"Username [%s]: " % uid)
    username = uid if username == '' else username
    password = getpass.getpass('Passwort: ')
    gets_mail = rpc.toggle_gets_mail(username, password)
    if gets_mail:
        print "Du erhaelst nun Informationen über deine Posts per E-Mail."
    else:
        print "E-Mail-Information deaktiviert."

def usage(prog_name):
    print >> sys.stderr, "Usage: %s server { register | change_pw | toggle_mail }" % prog_name

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage(sys.argv[0])
    calls = {
        'register': register,
        'change_pw': change_pw,
        'toggle_mail': toggle_mail,
    }
    rpc = ServerProxy(sys.argv[1])
    try:
        calls[sys.argv[2]](rpc)
    except KeyError:
        usage(sys.argv[0])