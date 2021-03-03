import os
import sys
import pydevd
import pydevd_pycharm
from proc_plant.consts import PYDEVD_EGG

def get_project_root_dir():
    """
    :return: path to proc_plant package
    """
    return os.path.dirname(os.path.realpath(__file__))


def connect_to_debugger():
    """
    If you want to debug your code via PyCharm:
    1. Click "Debug"
    2. Run this ONCE early on in any code that you run from within the Maya python tab.
    Based on https://matiascodesal.com/blog/how-to-use-pycharms-remote-debugging-with-maya/
    """
    # This should be the path your PyCharm installation

    if PYDEVD_EGG not in sys.path:
        sys.path.append(PYDEVD_EGG)

    # This clears out any previous connection in case you restarted the debugger from PyCharm
    pydevd.stoptrace()
    # 9001 matches the port number that I specified in my configuration
    pydevd_pycharm.settrace('localhost', port=9001, stdoutToServer=True, stderrToServer=True, suspend=False)
