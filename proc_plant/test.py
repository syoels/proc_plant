from proc_plant.plant_gen import Breed, create_sample_breed_and_draw_multiple_instances, get_sample_breed_kwargs
from proc_plant.general_utils import connect_to_debugger


def test(with_pycharm_debug_socket=False):

    if with_pycharm_debug_socket:
        print('Connecting to PyCharm Debugger..')
        connect_to_debugger()

    b = Breed("my_cool_breed")
    b.draw_breed_instance(instance_name=1)
    create_sample_breed_and_draw_multiple_instances(breed_name="another_breed", n=2)


def test_short(with_pycharm_debug_socket=False):

    if with_pycharm_debug_socket:
        print('Connecting to PyCharm Debugger..')
        connect_to_debugger()

    breed_kw = get_sample_breed_kwargs()
    b = Breed(**breed_kw)
    b.draw_breed_instance(instance_name=1)
