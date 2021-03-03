import os
import pymel.core as pm
from proc_plant.general_utils import get_project_root_dir
from proc_plant.consts import MTL_NS


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


def assign_mtl_from_resources(obj_names, mtl_name):
    if "." in mtl_name:
        mtl_name = mtl_name.split(".")[-2]

    if not pm.objExists(mtl_name):
        base_dir = get_project_root_dir()
        mtl_path = os.path.join(base_dir, "resources", "%s.ma" % mtl_name)
        print('loading mtl from %s' % mtl_path)
        pm.importFile(mtl_path, namespace=MTL_NS)

    mtl_name = "%s:%s" % (MTL_NS, mtl_name)
    mtl = pm.PyNode(mtl_name)

    print("Assigning shader...")
    for i, name in enumerate(obj_names):
        add = i != 0
        pm.select(name, visible=True, add=add)
    lst = pm.ls(sl=True)

    for name in lst:
        # Create a blank shading group
        sg = pm.PyNode(name).shadingGroups()[0]
        # Connect the output of the material to the input on the shading group
        pm.connectAttr((mtl.name() + ".outColor"), (sg.name() + ".surfaceShader"), force=True)