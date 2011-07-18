#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is used to deploy new versions of the application

from fabric.api import run, env, cd, sudo

def local():
    env.hosts = ['33.33.33.33']
    env.user = 'vagrant'

def prod():
    env.hosts = ['ec2-50-18-84-237.us-west-1.compute.amazonaws.com']
    env.user = 'ubuntu'

def deploy():
    with cd('/home/djangotutorial/django-tutorial'):
        sudo('git pull origin master')

    with cd('/home/djangotutorial/django-tutorial/mysite'):
        run('export PYTHONPATH=. && export DJANGO_SETTINGS_MODULE=local_settings && django-admin.py syncdb')
        sudo('export PYTHONPATH=. && export DJANGO_SETTINGS_MODULE=local_settings && django-admin.py collectstatic --noinput')

    sudo('/etc/init.d/supervisord restart')
