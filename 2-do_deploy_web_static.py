#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the...
    contents of the web_static folder of your AirBnB Clone repo,
    using the function do_pack.
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
