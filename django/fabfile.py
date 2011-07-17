#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is used to deploy new versions of the application

from fabric.api import run, sudo, env, cd

env.hosts = ['33.33.33.33']
env.user = 'vagrant'

def deploy():
    with cd('/home/djangotutorial/django-tutorial'):
        sudo('su djangotutorial -c "git pull origin master"')
        run('cd mysite && export PYTHONPATH=. && export DJANGO_SETTINGS_MODULE=local_settings && django-admin.py syncdb')
        sudo('cd mysite && export PYTHONPATH=. && export DJANGO_SETTINGS_MODULE=local_settings && django-admin.py collectstatic --noinput')
        sudo('/etc/init.d/supervisord restart')
