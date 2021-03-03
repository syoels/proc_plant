import pymel.core as pm
import random
import math
import numpy as np

from proc_plant.math_utils import mapFromTo
from consts import MTL_NAME
from proc_plant.maya_utils import try_deleting, assign_mtl_from_resources


class Plant(object):
    
    def __init__(self, name, plant_height=200, pole_radius=1.5, cones_num=1000, cones_to_complete_circle=150,
                 jnts_num=100, min_height_ratio=1.5, max_height_ratio=6, min_radius=0.4, max_radius=0.7,
                 min_rotation=0.0, max_rotation=30.0, rotation_range=10, delete_joints=True):
        self.name = name
        self.pole_name = "pole"
        self.plant_height = plant_height
        self.pole_radius = pole_radius
        self.cones_num = cones_num
        self.cones_to_complete_circle = cones_to_complete_circle
        self.jnts_num = jnts_num
        self.min_height_ratio = min_height_ratio
        self.max_height_ratio = max_height_ratio
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_rotation = min_rotation
        self.max_rotation = max_rotation
        self.rotation_range = rotation_range
        self.delete_joints = delete_joints

        print("Cleaning old plants leftovers...")
        try_deleting(["cone_*", "plant", "pole", "Cant delete pole", "plant_jnt_*"])

        self.cones_height = self.plant_height * 0.9
        self.height_step = self.cones_height / self.cones_num
        self.xz_step = self.cones_to_complete_circle / 1.0
        self.joint_height_step = float(self.plant_height) / self.jnts_num

    def draw_plant(self):
        # Create pole
        print("Creating stem...")
        c = pm.polyCylinder(
            name=self.pole_name, height=self.plant_height, radius=self.pole_radius, subdivisionsHeight=20)
        pm.move(self.pole_name, [0, self.plant_height / 2.0, 0])

        print("Adding cones...")
        for i in range(self.cones_num):

            # try omitting cone
            spawn_chance = (i / float(self.cones_num)) * random.uniform(0.9, 0.999)
            should_drop = random.random() < spawn_chance
            if should_drop:
                continue

            cone_name = "cone_%d" % i

            # position & rotation
            cone_height = i * self.height_step
            xz_index = i % self.cones_to_complete_circle
            x = math.sin(xz_index * self.xz_step) * self.pole_radius
            z = math.cos(xz_index * self.xz_step) * self.pole_radius
            y = cone_height + (random.random() - 0.5) / 2.0
            y_rotation = math.degrees(math.atan2(x, z)) - 90

            # random radius & ratio
            height_ratio = random.uniform(self.min_height_ratio, self.max_height_ratio)
            radius = random.uniform(self.min_radius, self.max_radius)

            # spawn cone and move/rotate
            cone = pm.cone(constructionHistory=True,
                           radius=radius,
                           heightRatio=height_ratio,
                           polygon=True,
                           name=cone_name)

            pm.move(cone_name, [x, y, z])
            pm.rotate(cone_name, [0, y_rotation, 0])

        # assign plant material
        plant = pm.polyUnite("cone_*", "pole", n="plant")
        assign_mtl_from_resources(["plant"], MTL_NAME)
        pm.delete(plant, constructionHistory=True)

        print("Creating joints & skin...")
        pm.select(deselect=True)
        for i in range(self.jnts_num):
            jnt_name = 'plant_jnt_%s' % str(i)
            jnt_position = [0, i * self.joint_height_step, 0]
            jnt = pm.joint(name=jnt_name, position=jnt_position, zso=True, oj='xyz')

        pm.select("plant_jnt*")
        pm.select("plant", add=True)
        pm.bindSkin()

        for i in range(self.jnts_num):
            jnt_name = 'plant_jnt_%s' % str(i)
            most_likely_rotation = mapFromTo(i, 0, self.jnts_num, self.min_rotation, self.max_rotation)
            rot_x = np.random.normal(most_likely_rotation, self.rotation_range)
            rot_y = np.random.normal(most_likely_rotation, self.rotation_range)
            rot_z = np.random.normal(most_likely_rotation, self.rotation_range)
            rotation = [rot_x, rot_y, rot_z]
            pm.rotate(jnt_name, rotation)

        print("Finishing up...")
        if self.delete_joints:
            pm.delete("plant", constructionHistory=True)
            try_deleting("plant_jnt_*")
        pm.rename("plant", self.name)
        print("%s Created!" % self.name)


def draw_plants(n=2):
    for i in range(n):
        plant_height = np.random.normal(150, 50)
        pole_radius = np.random.normal(1.2, 0.25)
        cones_num = int(np.random.normal(800, 100))
        cones_to_complete_circle = int(np.random.normal(120, 20))
        jnts_num = int(plant_height // 2)
        min_height_ratio = np.random.normal(1.5, 1.0)
        max_height_ratio = np.random.normal(7, 4.0)
        min_radius = np.random.normal(0.4, 0.1)
        max_radius = np.random.normal(0.7, 0.1)
        min_rotation = np.random.normal(0.0, 10.0)
        max_rotation = np.random.normal(25.0, 1.0)
        rotation_range = np.random.normal(15.0, 10.0)

        plant = Plant("spikey", plant_height=plant_height, pole_radius=pole_radius, cones_num=cones_num,
                      cones_to_complete_circle=cones_to_complete_circle, jnts_num=jnts_num,
                      min_height_ratio=min_height_ratio, max_height_ratio=max_height_ratio, min_radius=min_radius,
                      max_radius=max_radius, min_rotation=min_rotation, max_rotation=max_rotation,
                      rotation_range=rotation_range)
        plant.draw_plant()
