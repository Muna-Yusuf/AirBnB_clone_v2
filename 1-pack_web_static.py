#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents....
    of the web_static folder of your AirBnB Clone repo,...
    using the function do_pack.
"""


from fabric.api import *
from datetime import datetime
import os


def do_pack():
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
