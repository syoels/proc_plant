import os
import pymel.core as pm
from proc_plant.general_utils import get_project_root_dir


def assign_mtl_from_resources(obj_names, mtl_name):

    if "." in mtl_name:
        mtl_name = mtl_name.split(".")[-2]

    if not pm.objExists(mtl_name):
        base_dir = get_project_root_dir()
        mtl_path = os.path.join(base_dir, "resources", "%s.fbx" % mtl_name)
        print('loading mtl from %s' % mtl_path)
        pm.importFile(mtl_path, namespace='')

    mtl = pm.PyNode(mtl_name)

    print("Assigning shader...")
    for i, name in enumerate(obj_names):
        add = i == 0
        pm.select(name, visible=True, add=add)
    lst = pm.ls(sl=1)

    for i in lst:
        # Create a blank shading group
        sg = pm.PyNode(name).shadingGroups()

        # Connect the output of the material to the input on the shading group
        pm.connectAttr((mtl + ".outColor"), (sg + ".surfaceShader"), force=True)


def assign_mtl_from_resources_alt(obj_names, mtl_name):
    if "." in mtl_name:
        mtl_name = mtl_name.split(".")[-2]

    if not pm.objExists(mtl_name):
        base_dir = get_project_root_dir()
        mtl_path = os.path.join(base_dir, "resources", "%s.fbx" % mtl_name)
        print('loading mtl from %s' % mtl_path)
        pm.importFile(mtl_path, namespace='')

    global mtl
    mtl = pm.PyNode(mtl_name)

    print("Assigning shader...")
    for i, name in enumerate(obj_names):
        print(1, name)
        add = i != 0
        pm.select(name, visible=True, add=add)
    global lst
    lst = pm.ls(sl=1)
    print(lst)

    for name in lst:
        # Create a blank shading group
        global sg
        sg = pm.PyNode(name).shadingGroups()[0]

        # Connect the output of the material to the input on the shading group
        pm.connectAttr((mtl.name() + ".outColor"), (sg.name() + ".surfaceShader"), force=True)

