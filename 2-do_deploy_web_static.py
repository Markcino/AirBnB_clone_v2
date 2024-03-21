#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env, sudo
from os.path import exists
env.hosts = ['100.25.109.78', '34.229.69.154']

def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        sudo('mkdir -p {}{}/'.format(path, no_ext))
        sudo('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        sudo('rm /tmp/{}'.format(file_n))
        sudo('rsync -a {0}{1}/web_static/ {0}{1}/'.format(path, no_ext))
        sudo('rm -rf {}{}/web_static'.format(path, no_ext))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
