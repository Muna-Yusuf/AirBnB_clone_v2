#!/usr/bin/python3
""" Fabric script (based on the file 3-deploy_web_static.py)...
    that deletes out-of-date archives, using the function do_clean.
"""


from fabric.api import *
from datetime import datetime
import os

env.hosts = ["54.146.92.3", "54.160.116.131"]


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
    try:
        if not os.path.exists(archive_path):
            return False
        ext_fn = os.path.basename(archive_path)
        ext_no = os.path.splitext(ext_fn)
        ext = ext_no
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run(f"rm -rf {dpath}{ext_fn}/")
        run(f"mkdir -p {dpath}{ext_fn}/")
        run(f"tar -xzf /tmp/{ext_fn} -C {dpath}{ext_no}")
        run(f"rm /tmp/{ext_fn}")
        run(f"mv {0}{1}/web_static/*{0}{1}/".format(dpath, ext_no))
        run(f"rm -rf {dpath}{ext_no}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {dpath}{ext_no}/ /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """ Prototype: def deploy()."""
    path = do_deploy()
    if path is None:
        return False
    return do_deploy(path)


def do_clean(number=0):
    """ Prototype: def do_clean(number=0)."""
    if int(number) == 0:
        number = 1
    number = int(number) + 1
    remove_local(number)
    path = "/data/web_static/releases/*"
    run("ls -dt {} | tail -n +{} | sudo xargs rm -fr".format(path, number))
