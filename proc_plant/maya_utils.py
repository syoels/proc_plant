import os
import pymel.core as pm
from proc_plant.general_utils import get_project_root_dir
from proc_plant.consts import MTL_NS, SUBDIV_CATCLARK


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


def assign_mtl_from_resources(obj_names, mtl_name, include_displacement=True):
    if "." in mtl_name:
        mtl_name = mtl_name.split(".")[-2]

    mtl_name = "%s:%s" % (MTL_NS, mtl_name)

    if not pm.objExists(mtl_name):
        base_dir = get_project_root_dir()
        mtl_path = os.path.join(base_dir, "resources", "%s.ma" % mtl_name)
        print('loading mtl from %s' % mtl_path)
        pm.importFile(mtl_path, namespace=MTL_NS)

    mtl = pm.PyNode(mtl_name)

    print("Assigning shader...")
    for name in obj_names:
        sg = pm.PyNode(name).shadingGroups()[0]
        if include_displacement:
            set_arnold_displacement_attrs(name)
        # Connect the output of the material to the input on the shading group
        pm.connectAttr((mtl.name() + ".outColor"), (sg.name() + ".surfaceShader"), force=True)


def set_arnold_displacement_attrs(obj_name, subdiv_type=SUBDIV_CATCLARK, ai_subdiv_iterations=3, should_auto_bump=True):
    """
    Enable displacement attributes for <object_name>
    See https://docs.arnoldrenderer.com/display/A5AFMUG/Subdivision+Settings
    :param obj_name: obect name. function will find obj's associated shape and change some params there.
    :param subdiv_type: type of subdivision algorithm
    :param ai_subdiv_iterations: number of subdivisions
    :param should_auto_bump: should a bump map be auto generated by the displacement map
    """
    obj_shape = pm.listRelatives(obj_name, type='shape')[0]
    obj_shape.aiSubdivIterations.set(ai_subdiv_iterations)
    obj_shape.aiSubdivType.set(subdiv_type)
    obj_shape.aiDispAutobump.set(should_auto_bump)