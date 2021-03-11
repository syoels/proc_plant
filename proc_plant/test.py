from proc_plant.plant_gen import Breed, draw_breed_multiple_instances
from proc_plant.general_utils import connect_to_debugger


def test(with_pycharm_debug_socket=False):

    if with_pycharm_debug_socket:
        print('Connecting to PyCharm Debugger..')
        connect_to_debugger()

    b = Breed("my_cool_breed")
    b.draw_breed_instance(instance_name=1)
    draw_breed_multiple_instances(breed_name="another_breed", n=2)