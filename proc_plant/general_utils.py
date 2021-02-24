import pymel.core as pm
import os

def try_deleting(name):
    """
    delete all pre-existing nodes with <name>
    :param name: name of obj to delete, or list of names. can also include maya wildcards like "*"
    :return: True iff al delete operations were successful
    """
    if isinstance(name, list):
        all_succ = True
        for sub_name in name:
            print("iter %s" % sub_name)
            all_succ = all_succ and try_deleting(sub_name)
        return all_succ

    try:
        print("Trying to delete %s" % name)
        pm.select(name, visible=True, add=False)
        pm.delete()
        return True
    except:
        print("Cant delete %s" % name)
        return False


def get_project_root_dir():
    """
    :return: path to proc_plant package
    """
    return os.path.dirname(os.path.realpath(__file__))