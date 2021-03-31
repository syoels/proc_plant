import pymel.core as pm
import random
import math
import numpy as np

from proc_plant.math_utils import mapFromTo
from consts import STEM_MTL_NAME, SPIKES_MTL_NAME, SUBDIV_LINEAR, \
    BIND_METHOD_CLOSEST_CONSIDER_SKELETON, SKIN_METHOD_DUAL_QUATERNION
from proc_plant.maya_utils import try_deleting, assign_mtl_from_resources
from proc_plant.math_utils import angle_vect2d

class Breed(object):
    
    def __init__(self, breed_name, plant_height=200, pole_radius=1.5, cones_num=1000, cones_to_complete_circle=150,
                 jnts_num=100, min_height=1.5, max_height=6, min_radius=0.4, max_radius=0.7,
                 min_rotation=0.0, max_rotation=30.0, rotation_range=10, delete_joints=True):
        self.instances = {}
        self.breed_name = breed_name
        self.pole_name = "pole"
        self.plant_height = plant_height
        self.pole_radius = pole_radius
        self.cones_num = cones_num
        self.cones_to_complete_circle = cones_to_complete_circle
        self.jnts_num = jnts_num
        self.min_height = min_height
        self.max_height = max_height
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_rotation = min_rotation
        self.max_rotation = max_rotation
        self.rotation_range = rotation_range
        self.delete_joints = delete_joints

        print("Cleaning old plants leftovers...")
        clear_all_breeds_leftovers()

        self.cones_height = self.plant_height * 0.9
        self.height_step = self.cones_height / self.cones_num
        self.xz_step = self.cones_to_complete_circle / 1.0
        self.joint_height_step = float(self.plant_height) / self.jnts_num

    # ======================================================================
    #                             PRIVATE METHODS
    # ======================================================================
    def _assert_prequisites_completed(self, instance_name, stage):
        """
        use this to make sure you are creating partsa of the plant in the proper order.
        for example, you cant create the cones without creating the stem.
        :param instance_name: name of an instance you created (using <some Breed>.draw_breed_instance)
        :param stage: a stage in the creation process. one of <stages> defined inside this function
        """
        stages = ['stem', 'cones', 'mtl', 'joints', 'done']
        assert stage in stages
        stage_idx = stages.index(stage)
        for stage in stages[:stage_idx]:
            assert self.instances[instance_name]['creation_steps_completed'][stage]

    def _mark_stage_completed(self, instance_name, stage):
        """
        use this to mark that one of the creation stages is completed.
        :param instance_name: name of an instance you created (using <some Breed>.draw_breed_instance)
        :param stage: a stage in the creation process. one of <stages> defined inside this function
        :return:
        """
        stages = ['stem', 'cones', 'mtl', 'joints', 'done']
        assert stage in stages
        self.instances[instance_name]['creation_steps_completed'][stage] = True

    def _create_instance_pole(self, instance_name):
        # Create pole
        c = pm.polyCylinder(
            name=self.pole_name, height=self.plant_height, radius=self.pole_radius, subdivisionsHeight=20)
        pm.move(self.pole_name, [0, self.plant_height / 2.0, 0])
        self._mark_stage_completed(instance_name, "stem")
        return c

    def _create_instance_cones(self, instance_name):
        self._assert_prequisites_completed(instance_name, "cones")

        xz_angle_step_rad = (2 * np.pi) / self.cones_to_complete_circle
        for i in range(self.cones_num):
            # try omitting cone
            spawn_chance = (i / float(self.cones_num)) * random.uniform(0.9, 0.99)
            should_drop = random.random() < spawn_chance
            if should_drop:
                continue
            cone_name = "cone_%d" % i
            # random radius & ratio
            height = random.uniform(self.min_height, self.max_height)
            radius = random.uniform(self.min_radius, self.max_radius)

            # position & rotation
            cone_height = i * self.height_step
            xz_index = i % self.cones_to_complete_circle
            xz_angle = xz_index * xz_angle_step_rad

            x = math.sin(xz_angle) * (self.pole_radius + height / 3.0)
            z = math.cos(xz_angle) * (self.pole_radius + height / 3.0)
            y = cone_height + (random.random() - 0.5) / 2.0
            y_rot = angle_vect2d([x, z])

            # spawn cone and move/rotate
            cone = pm.polyCone(constructionHistory=True,
                               radius=radius,
                               height=height,
                               sx=12,
                               sy=2,
                               name=cone_name)

            pm.move(cone_name, [x, y, z])
            pm.rotate(cone_name, [90, y_rot, 0])
        self._mark_stage_completed(instance_name, "cones")

    def _assign_instance_material(self, instance_name):
        self._assert_prequisites_completed(instance_name, "mtl")

        assign_mtl_from_resources(["pole"], STEM_MTL_NAME)
        assign_mtl_from_resources(["cone_*"], SPIKES_MTL_NAME, displacement_kw={'subdiv_type': SUBDIV_LINEAR})
        plant = pm.polyUnite("cone_*", "pole", n="plant")
        self.instances[instance_name]['mesh'] = plant
        pm.delete(plant, constructionHistory=True)

        self._mark_stage_completed(instance_name, "mtl")

    def _create_instance_joints(self, instance_name):
        self._assert_prequisites_completed(instance_name, "joints")

        pm.select(deselect=True)
        jnt_prefix = '%s_%s_jnt' % (self.breed_name, instance_name)
        for i in range(self.jnts_num):
            jnt_name = '%s_%s' % (jnt_prefix, str(i))
            jnt_position = [0, i * self.joint_height_step, 0]
            jnt = pm.joint(name=jnt_name, position=jnt_position)
            self.instances[instance_name]['jnts'] += [jnt]
        pm.select("%s_%s_jnt_*" % (self.breed_name, instance_name))
        pm.select("plant", add=True)

        # pm.bindSkin()
        pm.skinCluster(tsb=True,
                       bindMethod=BIND_METHOD_CLOSEST_CONSIDER_SKELETON, heatmapFalloff=0.64,
                       skinMethod=SKIN_METHOD_DUAL_QUATERNION,
                       smoothWeights=0.5)

        jnt_name_prefix = '%s_%s_jnt' % (self.breed_name, instance_name)
        for i in range(self.jnts_num):
            jnt_name = '%s_%s' % (jnt_name_prefix, str(i))
            most_likely_rotation = mapFromTo(i, 0, self.jnts_num, self.min_rotation, self.max_rotation)
            rot_x = np.random.normal(most_likely_rotation, self.rotation_range)
            rot_y = np.random.normal(most_likely_rotation, self.rotation_range)
            rot_z = np.random.normal(most_likely_rotation, self.rotation_range)
            rotation = [rot_x, rot_y, rot_z]
            pm.rotate(jnt_name, rotation)

            # smaller towards edge
            if i > 0.75 * self.jnts_num:
                pm.scale(jnt_name, [0.2, 0.2, 0.2])


        if self.delete_joints:
            pm.delete("plant", constructionHistory=True)
            try_deleting(jnt_name_prefix + '*')

        self._mark_stage_completed(instance_name, "joints")

    @staticmethod
    def _get_new_instance_dict():
        return {
            'mesh': None,
            'jnts': [],
            'creation_steps_completed': {
                'stem': False,
                'cones': False,
                'mtl': False,
                'joints': False,
                'done': False
            }
        }

    # ======================================================================
    #                          PUBLIC METHODS
    # ======================================================================
    def draw_breed_instance(self, instance_name=""):

        self.clear_instance_leftovers(instance_name)
        self.instances[instance_name] = self._get_new_instance_dict()

        print("Creating stem...")
        c = self._create_instance_pole(instance_name)

        print("Adding cones...")
        self._create_instance_cones(instance_name)

        # assign plant material
        print("Assigning material...")
        self._assign_instance_material(instance_name)

        print("Creating joints & skin...")
        self._create_instance_joints(instance_name)

        print("Finishing up...")
        full_instance_name = "%s_%s" % (self.breed_name, instance_name)
        pm.rename("plant", full_instance_name)

        self._mark_stage_completed(instance_name, "done")

        print("%s Created!" % full_instance_name)

    def clear_all_breed_leftovers(self):
        """
        delete mesh and joints from all instances
        """
        for instance_name in self.instances:
            self.clear_instance_leftovers(instance_name)

    def clear_instance_leftovers(self, instance_name):
        """
        delete all leftovers from specific insrtance
        :param instance_name:
        """
        if instance_name not in self.instances:
            return
        jnts = self.intances[instance_name]['jnts']
        mesh = self.instances[instance_name]['mesh']
        pm.delete(mesh)
        for jnt in jnts:
            pm.delete(jnt)


# ======================================================================
#                       PUBLIC STATIC METHODS
# ======================================================================
def clear_all_breeds_leftovers():
    try_deleting(["pole*", "cone_*", "plant", "pole"])


def create_sample_breed_and_draw_multiple_instances(breed_name="spikey", n=2):
    kwargs = get_sample_breed_kwargs()
    kwargs['breed_name'] = breed_name
    breed = Breed(**kwargs)
    for i in range(n):
        breed.draw_breed_instance(instance_name=i)


def get_sample_breed_kwargs():
    return {
        'breed_name': 'sample_breed',
        'plant_height': np.random.normal(120, 20),
        'pole_radius': np.random.normal(1.2, 0.25),
        'cones_num': int(np.random.normal(500, 100)),
        'cones_to_complete_circle': int(np.random.normal(120, 20)),
        'jnts_num': 60,
        'min_height': np.random.normal(1.5, 1.0),
        'max_height': np.random.normal(4, 1.0),
        'min_radius': np.random.normal(0.3, 0.1),
        'max_radius': np.random.normal(0.5, 0.1),
        'min_rotation': np.random.normal(0.0, 3.0),
        'max_rotation': np.random.normal(15.0, 1.0),
        'rotation_range': max(np.random.normal(10.0, 4.0), 0),
        'delete_joints': False
    }

