#!/usr/bin/python
# -*- coding: utf-8 -*-

from provy.core import Role, AskFor
from provy.more.debian import NginxRole, UserRole
from provy.more.debian import GitRole, MySQLRole
from provy.more.debian import SupervisorRole, DjangoRole


class DjangoWebSite(Role):
    def provision(self):
        with self.using(UserRole) as role:
            role.ensure_user('djangotutorial', identified_by='pass', is_admin=True)

        with self.using(GitRole) as role:
            role.ensure_repository(repo='git://github.com/heynemann/django-tutorial.git',
                                   path='/home/djangotutorial/django-tutorial',
                                   branch="master",
                                   owner='djangotutorial')

        self.ensure_dir('/home/djangotutorial/logs', sudo=True, owner='djangotutorial')

        with self.using(MySQLRole) as role:
            role.ensure_user(username=self.context['mysql_user'],
                             login_from="%",
                             identified_by=self.context['mysql_password'])
            role.ensure_database(self.context['mysql_database'])
            role.ensure_grant('ALL PRIVILEGES', on=self.context['mysql_database'], username=self.context['mysql_user'], login_from='%')

        with self.using(SupervisorRole) as role:
            role.config(
                config_file_directory='/home/djangotutorial',
                log_folder='/home/djangotutorial/logs',
                user='djangotutorial'
            )

            with self.using(DjangoRole) as role:
                with role.create_site('website') as site:
                    site.settings_path = '/home/djangotutorial/django-tutorial/mysite/settings.py'
                    site.threads = 2
                    site.processes = 4
                    site.user = 'djangotutorial'
                    site.pid_file_path = '/home/djangotutorial'
                    site.log_file_path = '/home/djangotutorial/logs'
                    site.settings = {
                        'DATABASES["default"]["NAME"]':
                            self.context['mysql_database'],
                        'DATABASES["default"]["USER"]':
                            self.context['mysql_user'],
                        'DATABASES["default"]["PASSWORD"]': 
                            self.context['mysql_password']
                    }

        with self.using(NginxRole) as role:
            role.ensure_conf(conf_template='nginx.conf')
            role.ensure_site_disabled('default')
            role.create_site(site='django-tutorial', template='django-tutorial')
            role.ensure_site_enabled('django-tutorial')


servers = {
    'web': {
        'address': '33.33.33.33',
        'user': 'vagrant',
        'roles': [DjangoWebSite],
        'options': {
            'mysql_root_pass': 'pass',
            'mysql_user': 'djangotutorial',
            'mysql_password': AskFor('mysql_password', 'Please enter the password for the mysql djangotutorial user'),
            'mysql_database': 'django_tutorial'
        }
    }
}
