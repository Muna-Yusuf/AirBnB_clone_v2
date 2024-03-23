#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the...
    contents of the web_static folder of your AirBnB Clone repo,
    using the function do_pack.
"""

from fabric.api import put, run, env
from datetime import datetime
from os.path import exists

env.hosts = ["54.146.92.3", "34.207.62.58"]


def do_pack():
    """ Prototype: def do_pack()."""
    time_now = datetime.now()
    local("mkdir -p versions")

    tn = time_now.strftime("%Y%m%d%H%M%S")
    arc = "versions/web_static_" + tn + "." + "tgz"
    pri = local(f"tar -cvzf {arc} web_static")
    size_f = os.path.getsize(arc)
    print(f"web_static packed: {arc} -> {size_f}Bytes")
    if pri is not None:
        return arc
    else:
        return None


def do_deploy(archive_path):
    """ Prototype: def do_deploy(archive_path)."""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('sudo rm /tmp/{}'.format(file_n))
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('sudo rm -rf {}{}/web_static'.format(path, no_ext))
        run('sudo rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False
